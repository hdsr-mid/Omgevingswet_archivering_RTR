Dit script automatiseert het ophalen en loggen van gegevens over waterschapsverordeningen vanuit een externe API. Het gebruikt deze gegevens om een Excel-bestand te genereren dat de status van verschillende activiteiten binnen de verordeningen weergeeft, afhankelijk van de omgeving ('prod' of 'pre') en de datum van ophaling. De kernpunten zijn:

    Omgevingsinstellingen: Het script gebruikt de opgegeven omgevingsparameter (productie of pre-productie) en datum om relevante gegevens op te halen. Deze parameters beïnvloeden de API-aanvragen en het gegenereerde Excel-document.
    API-sleutel en Activiteitenlijst: Het laadt een API-sleutel en een lijst van activiteiten uit tekstbestanden. Deze zijn essentieel voor het maken van verzoeken aan de API en het bepalen van welke gegevens moeten worden opgehaald.
    Excel Document Creatie: Het script initialiseert een Excel-werkboek en -blad waarin de opgehaalde gegevens zullen worden gelogd, met vooraf gedefinieerde kolomkoppen en celopmaak.
    Data Ophaling en Verwerking: Voor elke activiteit maakt het script een reeks API-verzoeken om gedetailleerde informatie over die activiteit te verzamelen, inclusief de laatste wijzigingsdatums van verschillende regelgerelateerde objecten.
    Resultaten Loggen: De verzamelde gegevens worden geformatteerd en in het Excel-bestand ingevoerd. Datums worden gebruikt om de achtergrondkleur van cellen te bepalen, wat een visuele indicatie geeft van hoe recent elke activiteit is gewijzigd.

Het eindresultaat is een gedetailleerd overzicht van de huidige status van waterschapsverordeningen, nuttig voor analyse en tracking van veranderingen over tijd.

- Voeg de productie en pre API-keys toe aan de files in de volgende folder, deze keys kun je aanvragen bij [Iplo](https://aandeslagmetdeomgevingswet.nl/ontwikkelaarsportaal/api-register/api/omgevingsdocument-toepasbaar-opvragen/).
```
code/prod_API_key.txt
code/pre_API_key.txt
```
- Open code/log_RTR_status_via_API.py en zorg dat je root directory gelijk is aan het pad van de github repository
- Om bij de juiste activiteiten aan te komen moet je het bestand 'prod_activiteiten_waterschapsverordening.txt' of 'pre_activiteiten_waterschapsverordening.txt' vullen met de gewenste activiteiten en bijbehorende meta data. Deze gegevens staan voor HDSR in het Match model onder frames, selecteer de gewenste activiteiten en plak ze in de bovengenoemde txt files.
[selecteer de gewenste activiteiten en plak ze in de bovengenoemde txt files.](./data/Match_activiteiten_frame.PNG)
- Tijdens het draaien van het script wordt automatisch de datum van vandaag gebruikt op de productie omgeving. Als je dat wilt aanpassen kan dat door argumenten aan het script toe te voegen.
```
# De productie omgeving van de pre RTR omgeving van vandaag
python.exe g:/Github/waterschapsverordening_log_RTR_status/code/log_RTR_status_via_API.py

# De pre omgeving van de pre RTR omgeving van vandaag
python.exe g:/Github/waterschapsverordening_log_RTR_status/code/log_RTR_status_via_API.py pre

# Een overzicht van de pre RTR omgeving op één februari 2024
python.exe g:/Github/waterschapsverordening_log_RTR_status/code/log_RTR_status_via_API.py pre 01-02-2024

# Een overzicht van de prod RTR omgeving op drie januari 2024
python.exe g:/Github/waterschapsverordening_log_RTR_status/code/log_RTR_status_via_API.py prod 03-01-2024
```
