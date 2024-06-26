from rtr import RTR

def main():
    bestuursorgaan = "Hoogheemraadschap De Stichtse Rijnlanden" # Wetterskip Fryslân / Waterschap Vechtstromen / Hoogheemraadschap De Stichtse Rijnlanden
    RTR(bestuursorgaan).archive_activities()

if __name__ == "__main__":
    main()
