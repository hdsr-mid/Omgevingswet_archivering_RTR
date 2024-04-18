import os
import sys
from datetime import datetime
import requests
import xlsxwriter
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process some environment settings and actions.")
    parser.add_argument('--env', type=str, default="prod", choices=['prod', 'pre'],
                        help='Environment setting: prod (default) or pre.')
    parser.add_argument('--date', type=str, default=datetime.now().strftime("%d-%m-%Y"),
                        help='Date in the format dd-mm-yyyy, default is today\'s date.')
    parser.add_argument('--xml', action='store_true',
                        help='Flag to log sttr files if present.')
    args = parser.parse_args()
    return args

root = "D:\\HDSR\Github\waterschapsverordening_log_RTR_status"
args = parse_arguments()
environment = args.env
retrieval_date = args.date
activities_file = f"data/{environment}_activiteiten_waterschapsverordening.txt"
api_key_file = f"code/{environment}_API_key.txt"

class CallRTR:
    def __init__(self, root_directory, api_key_file, activities_file, retrieval_date):
        self.root_directory = root_directory
        os.chdir(self.root_directory)
        self.api_key = self.load_api_key(api_key_file)
        self.headers = {'Accept': 'application/hal+json, application/xml', 'x-api-key': self.api_key}
        self.activities_file = activities_file
        self.retrieval_date = retrieval_date
        self.base_url = self.determine_base_url(environment)
        self.urns = self.load_activities(activities_file)
        self.sttr_files = []
        self.setup_excel()

    @staticmethod
    def load_api_key(api_key_file):
        with open(api_key_file) as key_file:
            return key_file.read().strip()

    @staticmethod
    def load_activities(activities_file):
        urns = []
        with open(activities_file) as file:
            for line in file:
                activity = line.strip().split("\t")
                if len(activity) < 8:
                    urns.append(activity)
        return urns

    def setup_excel(self):
        document_name = f"waterschapsverordening_RTR_{environment}_status_{self.retrieval_date}.xlsx"
        self.workbook = xlsxwriter.Workbook(f"log/{document_name}")
        self.worksheet = self.workbook.add_worksheet()
        self.prepare_worksheet()
        
    def set_format(self, color, bold, text_wrap):
        return self.workbook.add_format({
            'bg_color': color,
            'text_wrap': text_wrap,
            'align': 'left',
            'valign': 'top',
            'bold': bold,
            'border': True,
        })

    def prepare_worksheet(self):
        headers = [
            "Activiteit                   ",
            "Uri",
            "Activiteiten Groep",
            "Regel",
            "Werkzaamheden",
            "Wijziging Conclusie",
            "Wijziging Melding",
            "Wijziging Aanvraag vergunning",
            "Wijziging Informatie",
        ]
        
        header_format = self.set_format('#DDDDDD', True, True)
        self.cell_format = self.set_format('white', False, False)
        self.worksheet.write_row('A1', headers, header_format)
        for i, header in enumerate(headers, 1):
            self.worksheet.set_column(i - 1, i - 1, max(10, len(header)) + 2)

    def log_activities_and_meta_data(self):
        with requests.Session() as session:
            for row, activity in enumerate(self.urns, 2):
                self.process_activity(session, activity, row)
        self.workbook.close()

    def process_activity(self, session, activity, row):
        name, _, uri, _, activity_group, rule_reference, _ = activity
        response_json = self.fetch_activity_data(session, uri)
        if response_json:
            self.log_activity_data(
                session, row, name, uri, activity_group, rule_reference, response_json
            )

    def fetch_activity_data(self, session, uri):
        url = self.compose_activity_url(uri)
        response = session.get(url, headers=self.headers)
        if response.ok:
            return response.json()
        print(f"Error fetching data for URI {uri}: {response.status_code}")
        return None

    @staticmethod
    def extract_werkzaamheden(data):
        werkzaamheden_list = []
        if "werkzaamheden" in data["_links"]:
            for werkzaamheid in data["_links"]["werkzaamheden"]:
                extracted_id = werkzaamheid["href"].split("/")[(-1)]
                werkzaamheden_list.append(extracted_id)
        return [', '.join(werkzaamheden_list)] if werkzaamheden_list else [""]

    def fetch_and_process_changes(self, session, data):
        changes = ["", "", "", ""]
        if "regelBeheerObjecten" in data:
            for object in data["regelBeheerObjecten"]:
                object_type = object["typering"]
                if object_type == "Indieningsvereisten":
                    object_type = object["toestemming"]["waarde"]
                functional_structure_reference = object["functioneleStructuurRef"]
                lastChanged = self.fetch_last_changed_date(session, functional_structure_reference)
                if object_type in {"Conclusie", "Melding", "Aanvraag vergunning", "Informatie"}:
                    index = ["Conclusie", "Melding", "Aanvraag vergunning", "Informatie"].index(
                        object_type
                    )
                    changes[index] = lastChanged
        return changes
    
    def append_sttr_file(self, data):
        try:
            sttr_bestand_href = data['_embedded']['toepasbareRegels'][0]['_links']['sttrBestand']['href']
            self.sttr_files.append(sttr_bestand_href)
        except KeyError as e:
            print(f"Data missing from {data} key: {e}")

    def fetch_last_changed_date(self, session, functional_structure_reference):
        url = self.compose_regel_beheer_object_url(functional_structure_reference)
        response = session.get(url, headers=self.headers)
        if response.ok:
            data = response.json()
            self.append_sttr_file(data)

            embedded = data.get('_embedded', {})
            applicable_rules = embedded.get('toepasbareRegels', [])
            if applicable_rules:
                return applicable_rules[0].get("laatsteWijzigingDatum", "")
        return ""

    @staticmethod
    def determine_base_url(env):
        if env == "prod":
            return "https://service.omgevingswet.overheid.nl/publiek/toepasbare-regels/api"
        if env == "pre":
            return "https://service.pre.omgevingswet.overheid.nl/publiek/toepasbare-regels/api"
        raise ValueError("Invalid environment specified")

    def compose_activity_url(self, uri):
        return f"{self.base_url}/rtrgegevens/v2/activiteiten/{uri}?datum={self.retrieval_date}"

    def compose_regel_beheer_object_url(self, functional_structure_reference):
        return f"{self.base_url}/toepasbareregelsuitvoerengegevens/v1/toepasbareRegels?functioneleStructuurRef={functional_structure_reference}&datum={self.retrieval_date}"

    def log_activity_data(self, session, row, name, uri, activity_group, rule_reference, data):
        werkzaamheden = self.extract_werkzaamheden(data)
        changes = self.fetch_and_process_changes(session, data)
        data_to_write = [name, uri, activity_group, rule_reference] + werkzaamheden + changes
        self.write_data_to_cells(row, data_to_write)

    @staticmethod
    def set_green_intensity(index):
        color = 'white'
        if index < 1:
            color = '#00FF00'
        elif index < 8:
            color = '#32CD32'
        elif index < 30:
            color = '#98FB98'
        elif index < 60:
            color = '#90EE90'
        else:
            color = '#F0FFF0'
        return color

    def write_data_to_cells(self, row, data_to_write):
        col = 0
        for content in data_to_write:
            try:
                content_date = datetime.strptime(content, "%d-%m-%Y %H:%M:%S")
                difference = datetime.now() - content_date
                color = self.set_green_intensity(difference.days)
                cell_format = self.set_format(color, False, False)
                self.worksheet.write(row - 1, col, content, cell_format)
            except ValueError:
                self.worksheet.write(row - 1, col, content, self.cell_format)
            col += 1

    def log_sttr_files(self):
        for url in self.sttr_files:
            identifier = url.split('/toepasbareRegels/')[1].split('/')[0]
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                print("ok")
                with open(f'log/sttr/sttr_file_{identifier}.xml', 'w', encoding='utf-8') as file:
                    file.write(response.text)
            else:
                print(f"Failed to download data from {url}, status code: {response.status_code}")

def main():
    rtr = CallRTR(root, api_key_file, activities_file, retrieval_date)
    rtr.log_activities_and_meta_data()

    if args.xml:
        rtr.log_sttr_files()

if __name__ == "__main__":
    main()