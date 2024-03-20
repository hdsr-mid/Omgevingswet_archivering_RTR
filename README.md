Python script om de status van de Registratie Toepasbare Regels naar .xlsx formaat te schrijven. 

- Voeg de productie en pre API-keys toe aan de files in de volgende folder, deze keys kun je aanvragen bij [Iplo](https://aandeslagmetdeomgevingswet.nl/ontwikkelaarsportaal/api-register/api/omgevingsdocument-toepasbaar-opvragen/).
```
code/Prod_API-key.txt
code/Pre_API-key.txt
```
- Door de variabele 'enviroment' aan te passen naar "Prod" of "Pre" kan van omgeving worden gewisseld
```
enviroment      = "Pre"
```
- Open code/log_RTR_status_via_API.py en zorg dat je root directory gelijk is aan het pad van de github repository
- Om bij de juiste activiteiten aan te komen moet je het bestand 'Prod_Activiteiten_Waterschapsverordening.txt' of 'Pre_Activiteiten_Waterschapsverordening.txt' vullen met de gewenste activiteiten en bijbehorende meta data. Voor de activiteit stijger aanleggen ziet dat er bij HDSR zo uit:
```
steiger aanleggen	nl.imow-ws0636.activiteit.BeperkingengebiedAct	nl.imow-ws0636.activiteit.SteigerAanleggen	Zorgplicht	Beperkingengebiedactiviteit	4.8.1	HDSR
```
Deze gegevens staan voor HDSR in het Match model onder frames, selecteer de gewenste activiteiten en plak ze in de bovengenoemde txt files.
[](./data/ActiviteitenFrame.PNG)

- Automatisch wordt de huidige datum gebruikt voor het draaien van het script, in de RTR kun je ook terug in de tijd, of in de toekomst zoeken. Je kunt de variabele 'retrieval_date' aanpassen naar de gewenste datum bijvoorbeeld "01-01-2024".
```
retrieval_date = "01-01-2024"
```

