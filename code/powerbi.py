import pandas as pd

# Load the data from Excel files
urn_excel = pd.read_excel(r"D:\HDSR\Github\waterschapsverordening_log_RTR_status\data\A1. Welke activiteiten zijn gewijzigd PROD.xlsx")
location_excel = pd.read_excel(r"D:\HDSR\Github\waterschapsverordening_log_RTR_status\data\A2. Welke locaties worden er gebruikt PROD.xlsx")

# Extract relevant columns into DataFrames
urns = pd.DataFrame(urn_excel, columns=["Bestuursorgaan", "omschrijving", "URN"])
locations = pd.DataFrame(location_excel, columns=["Bestuursorgaan", "omschrijving", "noemer", "identificatie"])

# Sort the DataFrames by 'Bestuursorgaan'
urns_sorted = urns.sort_values(by="Bestuursorgaan")
locations_sorted = locations.sort_values(by="Bestuursorgaan")

# Ensure row-wise data stays intact by resetting the index
urns_sorted.reset_index(drop=True, inplace=True)
locations_sorted.reset_index(drop=True, inplace=True)

# Print the sorted DataFrames
print(urns_sorted)
print(locations_sorted)
