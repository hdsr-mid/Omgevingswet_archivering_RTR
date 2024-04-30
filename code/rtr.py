import os
from datetime import datetime
import requests
import argparse
import urllib.parse

from excel import ExcelHandler

class RTR:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
        self.args = self.parse_arguments()
        self.api_key = self.load_api_key(os.path.join(self.base_dir, 'code', f"{self.args.env}_API_key.txt"))
        self.headers = {'Accept': 'application/hal+json, application/xml', 'x-api-key': self.api_key}
        self.base_url = self.determine_base_url(self.args.env)
        self.urns = self.load_activities(os.path.join(self.base_dir, 'data', f"{self.args.env}_activiteiten_waterschapsverordening.txt"))
        self.sttr_url_by_name = {}
        self.excel_handler = ExcelHandler(self.base_dir, self.args.env, self.args.date)

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

    def log_activities(self):
        with requests.Session() as session:
            for row, activity in enumerate(self.urns, 2):
                self.process_activity(session, activity, row)
        if self.args.sttr: 
            self.log_sttr_files()
        self.excel_handler.close_workbook()

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
                object_type, last_changed = self.process_individual_object(session, urn_name, object)
                if object_type in {"Conclusie", "Melding", "Aanvraag vergunning", "Informatie"}:
                    index = ["Conclusie", "Melding", "Aanvraag vergunning", "Informatie"].index(object_type)
                    changes[index] = last_changed
        return changes

    def process_individual_object(self, session, urn_name, object):
        object_type = object["typering"]
        if object_type == "Indieningsvereisten":
            object_type = object["toestemming"]["waarde"]

        functional_structure_reference = object["functioneleStructuurRef"]
        last_changed = self.process_regelbeheerobject(session, urn_name, object_type, functional_structure_reference)
        return object_type, last_changed

    
    def process_regelbeheerobject(self, session, urn_name, object_type, functional_structure_reference):
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
        self.excel_handler.write_data_to_cells(row, data_to_write)

    def log_sttr_files(self):
        for key, url in self.sttr_url_by_name.items():
            identifier = url.split('/toepasbareRegels/')[1].split('/')[0]
            response = requests.get(url, headers=self.headers)
                         
            if response.status_code == 200:
                with open(os.path.join(self.base_dir, f'log/STTR_RegelBeheerObjecten/STTR_{identifier}_{key}.xml'), 'w', encoding='utf-8') as file:
                    file.write(response.text)
            else:
                print(f"Failed to download data from {url}, status code: {response.status_code}")

