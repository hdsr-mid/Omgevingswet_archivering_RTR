import os
import pandas as pd

class PowerBIData:
    def __init__(self, urn_path, location_path):
        self.urn_path = urn_path
        self.location_path = location_path
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.urns_sorted = self._load_and_prepare_urn_data()
        self.locations_sorted = self._load_and_prepare_location_data()

    def _load_and_prepare_urn_data(self):
        urn_excel = pd.read_excel(self.urn_path)
        urns = pd.DataFrame(urn_excel, columns=["Bestuursorgaan", "omschrijving", "URN"])
        urns_sorted = urns.sort_values(by="Bestuursorgaan")
        urns_sorted.reset_index(drop=True, inplace=True)
        return urns_sorted

    def _load_and_prepare_location_data(self):
        location_excel = pd.read_excel(self.location_path)
        locations = pd.DataFrame(location_excel, columns=["Bestuursorgaan", "omschrijving", "noemer", "identificatie"])
        locations_sorted = locations.sort_values(by="Bestuursorgaan")
        locations_sorted.reset_index(drop=True, inplace=True)
        return locations_sorted

    def get_location_identifiers(self, bestuursorgaan):
        geo_names_by_index = {}
        filtered_locations = self.locations_sorted[self.locations_sorted["Bestuursorgaan"] == bestuursorgaan]
        
        for index, row in filtered_locations.iterrows():
            
            line_number = str(row["identificatie"]).strip()
            noemer = str(row["noemer"]).strip()
            print(':')
            print(row)
            print(noemer)
            print('.')
            
            if noemer != '\\N' and line_number not in geo_names_by_index:
                geo_names_by_index[line_number] = noemer
        
        return geo_names_by_index

    def get_urns(self, bestuursorgaan):
        urns = []
        filtered_urns = self.urns_sorted[self.urns_sorted["Bestuursorgaan"] == bestuursorgaan]
        for index, row in filtered_urns.iterrows():
            activity = [str(row["Bestuursorgaan"]), str(row["omschrijving"]), str(row["URN"])]
            urns.append(activity)
            print(activity)
        return urns

'''
if __name__ == "__main__":
    urn_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                 'data', 
                                 "A1. Welke activiteiten zijn gewijzigd PROD.xlsx")
    location_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                      'data', 
                                      "A3. Wie gebruikt welke locaties (in STTR) PROD.xlsx")
    data = PowerBIData(urn_file_path, location_file_path)
    
    bestuursorganen = ["Hoogheemraadschap De Stichtse Rijnlanden"] #"Wetterskip Fryslân", 
    
    for bestuursorgaan in bestuursorganen:
        print(f'Locations for {bestuursorgaan}:')
        locations = data.get_location_identifiers(bestuursorgaan)
        for k, v in locations.items():
            print(f"{k}: {v}")
        
        print()
        print(f'URNs for {bestuursorgaan}:')
        urns = data.get_urns(bestuursorgaan)
        for urn in urns:
            print(urn)
        print()
'''
