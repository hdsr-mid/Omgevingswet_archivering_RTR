import os
from datetime import datetime
import requests
import xlsxwriter
import argparse
import urllib.parse

class RTR:
    def __init__(self):
        #os.chdir("D:\\HDSR\Github\waterschapsverordening_log_RTR_status")      # home
        os.chdir("G:\\Github\waterschapsverordening_log_RTR_status")            # work
        self.args = self.parse_arguments()
        self.api_key = self.load_api_key(f"code/{self.args.env}_API_key.txt")
        self.headers = {'Accept': 'application/hal+json, application/xml', 'x-api-key': self.api_key}
        self.base_url = self.determine_base_url(self.args.env)
        self.urns = self.load_activities(f"data/{self.args.env}_activiteiten_waterschapsverordening.txt")
        self.sttr_url_by_name = {}
        self.setup_excel()

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Process some environment settings and actions.")
        parser.add_argument('--env', type=str, default="prod", choices=['prod', 'pre'],
                            help='Environment setting: prod (default) or pre.')
        parser.add_argument('--date', type=str, default=datetime.now().strftime("%d-%m-%Y"),
                            help='Date in the format dd-mm-yyyy, default is today\'s date.')
        parser.add_argument('--sttr', action='store_true',
                            help='Flag to log sttr files in .xml if present.')
        args = parser.parse_args()
        return args

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
        document_name = f"waterschapsverordening_RTR_{self.args.env}_status_{self.args.date}.xlsx"
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

    def log_activities(self):
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
        urn_name = data["urn"].split(".")[-1]
        changes = ["", "", "", ""]
        
        if "regelBeheerObjecten" in data:
            for object in data["regelBeheerObjecten"]:
                object_type = object["typering"]
                if object_type == "Indieningsvereisten":
                    object_type = object["toestemming"]["waarde"]
                else:
                    object_type = "null"

                functional_structure_reference = object["functioneleStructuurRef"]
                lastChanged = self.process_regelbeheerobject(session, urn_name, object_type, functional_structure_reference)
                if object_type in {"Conclusie", "Melding", "Aanvraag vergunning", "Informatie"}:
                    index = ["Conclusie", "Melding", "Aanvraag vergunning", "Informatie"].index(
                        object_type
                    )
                    changes[index] = lastChanged
        return changes
    
    def process_regelbeheerobject(self, session, urn_name, object_type, functional_structure_reference):
        regelbeheerobject_exists = object_type != "null"
        if regelbeheerobject_exists:        
            url = self.compose_regel_beheer_object_url(functional_structure_reference)
            response = session.get(url, headers=self.headers)

            if response.ok:
                data = response.json()
                self.append_sttr_file(urn_name, object_type, data)
                last_changed = self.get_last_change_date(data)
                return last_changed

    def get_last_change_date(self, data):
        embedded = data.get('_embedded', {})
        applicable_rules = embedded.get('toepasbareRegels', [])
        if applicable_rules:
            return applicable_rules[0].get("laatsteWijzigingDatum", "")
        else:
            return ""
    
    def append_sttr_file(self, urn_name, regelbeheerobject_type, data):
        try:
            sttr_bestand_href = data['_embedded']['toepasbareRegels'][0]['_links']['sttrBestand']['href']
            
            if regelbeheerobject_type != "null":
                regelbeheerobject_name = urn_name + "_" + regelbeheerobject_type.replace(" ", "_")
                self.sttr_url_by_name[regelbeheerobject_name] = sttr_bestand_href
            
        except KeyError as e:
            identifier = self.extract_identifier(data)
            print(f"Data missing key: '{e}'. Regelbeheerobject: {identifier}")

    def extract_identifier(self, data):
        try:
            url = data.get('_links', {}).get('self', {}).get('href', "")
            functionele_structuur_ref = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get('functioneleStructuurRef', [''])[0]
            return functionele_structuur_ref.split('/')[-1]
        except Exception:
            return "Unknown"  

    @staticmethod
    def determine_base_url(env):
        if env == "prod":
            return "https://service.omgevingswet.overheid.nl/publiek/toepasbare-regels/api"
        if env == "pre":
            return "https://service.pre.omgevingswet.overheid.nl/publiek/toepasbare-regels/api"
        raise ValueError("Invalid environment specified")

    def compose_activity_url(self, uri):
        return f"{self.base_url}/rtrgegevens/v2/activiteiten/{uri}?datum={self.args.date}"

    def compose_regel_beheer_object_url(self, functional_structure_reference):
        return f"{self.base_url}/toepasbareregelsuitvoerengegevens/v1/toepasbareRegels?functioneleStructuurRef={functional_structure_reference}&datum={self.args.date}"

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
        for key, url in self.sttr_url_by_name.items():
            identifier = url.split('/toepasbareRegels/')[1].split('/')[0]
            response = requests.get(url, headers=self.headers)
                         
            if response.status_code == 200:
                with open(f'log/STTR_RegelBeheerObjecten/STTR_{identifier}_{key}.xml', 'w', encoding='utf-8') as file:
                    file.write(response.text)
            else:
                print(f"Failed to download data from {url}, status code: {response.status_code}")

def main():
    rtr = RTR()
    rtr.log_activities()

    if rtr.args.sttr:
        rtr.log_sttr_files()

if __name__ == "__main__":
    main()