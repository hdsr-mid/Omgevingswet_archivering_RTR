from rtr import RTR  

def main():
    rtr = RTR() 
    rtr.log_activities()

    if rtr.args.sttr: 
        rtr.log_sttr_files()

if __name__ == "__main__":
    main()
