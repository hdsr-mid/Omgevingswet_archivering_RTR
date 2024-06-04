import pandas as pd

excel = pd.read_excel(r"D:\HDSR\Github\waterschapsverordening_log_RTR_status\data\A1. Welke activiteiten zijn gewijzigd PROD.xlsx") 

urns = pd.DataFrame(excel, columns=["URN", "Bestuursorgaan"])

urn_per_bestuursorgaan = {}

#for urn in urns:

print(urns["Waterschap Limburg"])

#print(urns)