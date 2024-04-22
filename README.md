Via dit script kunnen gegevens uit de RTR worden opgevraagd en lokaal worden opgeslagen. Denk daarbij aan het genereren van een Excel overzicht van activiteiten en hun bijbehorende data en DMN logica. 

Gebruik
```
python.exe code/log_RTR_status_via_API.py
```

Flags
```
--env prod/pre        # Selecteer de juiste omgeving,               standaard: prod
--date 01-01-2024     # Datum voor het tijdstip van de RTR,         standaard: vandaag
--sttr                # Sla per regelbeheerobject de DMN logica op  standaard: uit

voorbeeld: python.exe code/log_RTR_status_via_API.py --env pre --date 03-03-2024
voorbeeld: python.exe code/log_RTR_status_via_API.py --env prod --date 12-04-2024 --sttr
```

Setup
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
