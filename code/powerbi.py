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
        identifiers = self.locations_sorted[self.locations_sorted["Bestuursorgaan"] == bestuursorgaan]["identificatie"]
        return identifiers.dropna().unique().tolist()

    def get_urns(self, bestuursorgaan):
        urns_list = self.urns_sorted[self.urns_sorted["Bestuursorgaan"] == bestuursorgaan]["URN"]
        return urns_list.dropna().unique().tolist()
    
if __name__ == "__main__":
    urn_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                 'data', 
                                 "A1. Welke activiteiten zijn gewijzigd PROD.xlsx")
    location_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                      'data', 
                                      "A2. Welke locaties worden er gebruikt PROD.xlsx")
    data = PowerBIData(urn_file_path, location_file_path)
    
    bestuursorgaan = "Wetterskip Fryslân"
    print(f'locaties for {bestuursorgaan}:')
    print(data.get_location_identifiers(bestuursorgaan))
    print()
    print(f'urns for {bestuursorgaan}:')
    print(data.get_urns(bestuursorgaan))
