import requests
import os

class STTRService:
    def __init__(self, identifier=70356, api_key=''):
        self.identifier = identifier
        self.api_key = api_key
        self.headers = {'Accept': 'application/xml, application/json', 'x-api-key': self.api_key}

    def compose_sttr_url(self):
        return f"https://service.omgevingswet.overheid.nl/publiek/toepasbare-regels/api/toepasbareregelsuitvoerengegevens/v1/toepasbareRegels/{self.identifier}/sttrBestand"

    def call_sttr_url(self):
        url = self.compose_sttr_url()
        response = requests.get(url, headers=self.headers)
        return response

def main():
    root_directory = "D:\\HDSR\\Github\\waterschapsverordening_log_RTR_status"
    os.chdir(root_directory)
    
    api_key_path = "code/prod_API_key.txt"
    with open(api_key_path, 'r') as file:
        api_key = file.read().strip()
    
    sttr_service = STTRService(api_key=api_key)
    response = sttr_service.call_sttr_url()
    print(response.text)

if __name__ == "__main__":
    main()
