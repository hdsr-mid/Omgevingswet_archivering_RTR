import os

class Vendor:
    def __init__(self, software, environment):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
        self.software = software
        self.environment = environment

        if self.software == "Match":
            activities_frame_file = os.path.join(self.base_dir, 'data', f"frames_{self.environment}_activiteiten.txt")
            self.urns = self.load_activities(activities_frame_file)

            geo_frame_file = os.path.join(self.base_dir, 'data', f"frames_geo_informatie.txt")
            self.variable_names_by_index = self.load_geo_variables(geo_frame_file)

    def load_activities(self, activities_frame_file):
        urns = []
        with open(activities_frame_file) as file:
            for line in file:
                activity = line.strip().split("\t")
                if len(activity) < 8:
                    urns.append(activity)
        return urns
    
    def load_geo_variables(self, geo_frame_file):
        variable_names_by_index = {}
        with open(geo_frame_file) as file:
            for line in file:
                parts = line.strip().split("\t")
                if len(parts) >= 2: 
                    line_number = parts[0].strip()
                    name = parts[1].strip()
                    variable_names_by_index[line_number] = name
        return variable_names_by_index

