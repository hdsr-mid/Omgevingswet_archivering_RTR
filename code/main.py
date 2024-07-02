from rtr import RTR
from commands import ArgumentParser  

def main():
    args = ArgumentParser.parse_command_line_arguments()
    RTR(args).archive_activities()

if __name__ == "__main__":
    main()
