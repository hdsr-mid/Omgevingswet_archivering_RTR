import argparse
from datetime import datetime

class ArgumentParser:
    @staticmethod
    def parse_command_line_arguments():
        parser = argparse.ArgumentParser(description="Process some environment settings and actions.")
        parser.add_argument('--overheid', type=str, default="Hoogheemraadschap_De_Stichtse_Rijnlanden",
                            help='Overheid setting, default is "Hoogheemraadschap De Stichtse Rijnlanden".')
        parser.add_argument('--env', type=str, default="prod", choices=['prod', 'pre'],
                            help='Environment setting: prod (default) or pre.')
        parser.add_argument('--date', type=str, default=datetime.now().strftime("%d-%m-%Y"),
                            help='Date in the format dd-mm-yyyy, default is today\'s date.')
        parser.add_argument('--sttr', action='store_true',
                            help='Flag to archive STTR files in .xml')
        parser.add_argument('--location', action='store_true',
                            help='Flag to archive werkingsgebieden per activity to .txt')
        args = parser.parse_args()
        
        # Replace underscores with spaces in the overheid argument
        args.overheid = args.overheid.replace('_', ' ')
        return args
