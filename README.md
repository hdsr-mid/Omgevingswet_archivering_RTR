# Archivering van de Registratie Toepasbare Regels voor alle Nederlandse overheden

Via deze scripts kunnen gegevens uit de RTR worden opgevraagd en lokaal worden gearchiveerd. Denk daarbij aan het genereren van een Excel overzicht van activiteiten en hun bijbehorende werkzaamheden en regelbeheerobjecten en het downloaden van de DMN logica uit de STTR. 

## Gebruik
```
--overheid                # Typ de juiste overheid . . . . . . . . . . . standaard: Hoogheemraadschap_De_Stichtse_Rijnlanden
--env prod/pre            # Selecteer de gewenste omgeving . . . . . . . standaard: prod
--date 01-01-2024         # Kies een datum . . . . . . . . . . . . . . . standaard: vandaag
--sttr                    # Archiveer de DMN logica per activiteit . . . standaard: uit
--location                # Archiveer werkingsgebieden per activiteit. . standaard: uit

voorbeeld: python.exe code/log_RTR_status_via_API.py -- overheid Waterschap_Vechtstromen
voorbeeld: python.exe code/log_RTR_status_via_API.py -- overheid Wetterskip_Fryslân --env pre --date 03-03-2024
voorbeeld: python.exe code/log_RTR_status_via_API.py -- overheid --env prod --date 12-04-2024 --sttr --location

De volgorde van de flags maakt niet uit, als een flag niet word aangeroepen gebruikt die zijn standaard waarde.
```

## Setup
Voeg de productie- en pre-omgeving API-keys toe aan de volgende bestanden, deze keys kun je aanvragen bij [Iplo](https://aandeslagmetdeomgevingswet.nl/ontwikkelaarsportaal/api-register/api/omgevingsdocument-toepasbaar-opvragen/).
```
data/prod_API_key.txt
data/pre_API_key.txt
```
# Install
Installeer de volgende Python dependencies.
```
pip install requests
pip install xlsxwriter
pip install pandas
pip install openpyxl
```