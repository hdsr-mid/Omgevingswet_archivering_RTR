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

voorbeeld: python.exe code/log_RTR_status_via_API.py
voorbeeld: python.exe code/log_RTR_status_via_API.py --env pre --date 03-03-2024
voorbeeld: python.exe code/log_RTR_status_via_API.py --env prod --date 12-04-2024 --sttr
```

Setup
- Voeg de productie en pre API-keys toe aan de files in de volgende folder, deze keys kun je aanvragen bij [Iplo](https://aandeslagmetdeomgevingswet.nl/ontwikkelaarsportaal/api-register/api/omgevingsdocument-toepasbaar-opvragen/).
```
code/prod_API_key.txt
code/pre_API_key.txt
```
- Om bij de juiste activiteiten aan te komen moet je het bestand 'prod_activiteiten_waterschapsverordening.txt' en/of 'pre_activiteiten_waterschapsverordening.txt' vullen met de gewenste activiteiten en bijbehorende meta data. Deze gegevens staan voor HDSR in het Match model onder frames, selecteer de gewenste activiteiten en plak ze in de bovengenoemde txt files.
[selecteer de gewenste activiteiten en plak ze in de bovengenoemde txt files.](./data/Match_activiteiten_frame.PNG)
