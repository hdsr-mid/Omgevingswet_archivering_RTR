import os
from datetime import datetime
import requests
import xlsxwriter

root            = "G:\\Github\waterschapsverordening_log_RTR_status"
enviroment      = "Pre"
api_key_file    = f"code/{enviroment}_API-key.txt"
activities_file = f"data/{enviroment}_Activiteiten_Waterschapsverordening.txt"
retrieval_date  = datetime.now().strftime("%d-%m-%Y")

class LogRTR:
    def __init__(self, root_directory, api_key_file, activities_file, retrieval_date):
        self.root_directory = root_directory
        os.chdir(self.root_directory)
        self.api_key          = self.load_api_key(api_key_file)
        self.headers          = {'Accept': 'application/hal+json', 'x-api-key': self.api_key}
        self.activities_file  = activities_file
        self.retrieval_date   = retrieval_date
        self.base_url         = self.determine_base_url(enviroment)
        self.urns             = self.load_activities(activities_file)
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
        document_name   = f"Waterschapsverordening_RTR_{enviroment}_status_{self.retrieval_date}.xlsx"
        self.workbook   = xlsxwriter.Workbook(f"log/{document_name}")
        self.worksheet  = self.workbook.add_worksheet()
        self.prepare_worksheet()

    def prepare_worksheet(self):
        header_format = self.workbook.add_format({
            'bg_color': '#DDDDDD',
            'text_wrap': True,
            'align': 'left',
            'valign': 'top',
            'bold': True,
            'border': True,
        })
        self.cell_format = self.workbook.add_format({
            'bg_color': 'white',
            'text_wrap': False,
            'align': 'left',
            'valign': 'top',
            'bold': False,
            'border': True,
        })
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
        self.worksheet.write_row('A1', headers, header_format)
        for i, header in enumerate(headers, 1):
            self.worksheet.set_column(i - 1, i - 1, max(10, len(header)) + 2)

    def retrieve_and_log_data(self):
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

    def fetch_last_changed_date(self, session, functional_structure_reference):
        url = self.compose_regel_beheer_object_url(functional_structure_reference)
        response = session.get(url, headers=self.headers)
        if response.ok:
            data = response.json()
            embedded = data.get('_embedded', {})
            toepasbare_regels = embedded.get('toepasbare_regels', [])
            if toepasbare_regels:
                return toepasbare_regels[0].get("laatsteWijzigingDatum", "")
        return ""

    @staticmethod
    def determine_base_url(env):
        if env == "Prod":
            return "https://service.omgevingswet.overheid.nl/publiek/toepasbare-regels/api"
        if env == "Pre":
            return "https://service.pre.omgevingswet.overheid.nl/publiek/toepasbare-regels/api"
        raise ValueError("Invalid environment specified")

    def compose_activity_url(self, uri):
        return f"{self.base_url}/rtrgegevens/v2/activiteiten/{uri}?datum={self.retrieval_date}"

    def compose_regel_beheer_object_url(self, functional_structure_reference):
        return f"{self.base_url}/toepasbareregelsuitvoerengegevens/v1/toepasbare_regels?functioneleStructuurRef={functional_structure_reference}&datum={self.retrieval_date}"

    def log_activity_data(self, session, row, name, uri, activity_group, rule_reference, data):
        werkzaamheden = self.extract_werkzaamheden(data)
        changes = self.fetch_and_process_changes(session, data)
        data_to_write = [name, uri, activity_group, rule_reference] + werkzaamheden + changes
        self.worksheet.write_row(row - 1, 0, data_to_write, self.cell_format)

        

def main():
    rtr = LogRTR(root, api_key_file, activities_file, retrieval_date)
    rtr.retrieve_and_log_data()

if __name__ == "__main__":
    main()