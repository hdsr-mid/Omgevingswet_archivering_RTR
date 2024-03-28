Dit script verzamelt en analyseert gegevens over waterschapsverordeningen door vanuit een externe API de status van diverse activiteiten op te halen, afhankelijk van een gespecificeerde omgeving ('prod' of 'pre') en datum. Het laadt een API-sleutel en een activiteitenlijst uit bestanden, maakt API-verzoeken om informatie over elke activiteit te verzamelen, en logt deze gegevens in een dynamisch gegenereerd Excel-bestand. Dit bestand bevat gedetailleerde informatie over de activiteiten, waaronder de laatste wijzigingsdatums, en gebruikt celkleuring om de recentheid van de gegevens visueel aan te duiden. Het resultaat is een uitgebreid en visueel inzichtelijk document dat dient als een overzicht van de huidige stand van zaken binnen waterschapsverordeningen, nuttig voor zowel analyse als het volgen van veranderingen over tijd.

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
