# Archivering van de RTR voor de Waterschapsverorderning

Via dit script kunnen gegevens uit de RTR worden opgevraagd en lokaal worden gearchiveerd. Denk daarbij aan het genereren van een Excel overzicht van activiteiten en hun bijbehorende werkzaamheden en regelbeheerobjecten en het downloaden van de DMN logica uit de STTR. 

## Gebruik
```
--env prod/pre             # Selecteer de gewenste omgeving . . . . . . . standaard: prod
--date 01-01-2024          # Kies een datum . . . . . . . . . . . . . . . standaard: vandaag
--sttr                     # Archiveer de DMN logica per activiteit . . . standaard: uit

voorbeeld: python.exe code/log_RTR_status_via_API.py
voorbeeld: python.exe code/log_RTR_status_via_API.py --env pre --date 03-03-2024
voorbeeld: python.exe code/log_RTR_status_via_API.py --env prod --date 12-04-2024 --sttr

De volgorde van de flags maakt niet uit, als een flag niet word aangeroepen gebruikt die zijn standaard waarde.
```

## Setup
Voeg de productie- en pre-omgeving API-keys toe aan de volgende bestanden, deze keys kun je aanvragen bij [Iplo](https://aandeslagmetdeomgevingswet.nl/ontwikkelaarsportaal/api-register/api/omgevingsdocument-toepasbaar-opvragen/).
```
code/prod_API_key.txt
code/pre_API_key.txt
```
Vul de volgende bestanden met de meta data van de activiteiten.
```
data/prod_activiteiten_waterschapsverordening.txt
data/pre_activiteiten_waterschapsverordening.txt
```
Een voorbeeld van de activiteit 'burg aanleggen' op de pre omgeving bij HDSR ziet er zo uit:
```
brug aanleggen	nl.imow-ws0636.activiteit.BeperkingengebiedActT5	nl.imow-ws0636.activiteit.BrugAanleggenT5	Zorgplicht	Beperkingengebiedactiviteit	4.7.1	HDSRT5
```
Deze gegevens staan voor HDSR in het Match model onder frames, [selecteer de gewenste activiteiten](./data/Match_activiteiten_frame.PNG) en plak ze in de bovengenoemde txt files.

