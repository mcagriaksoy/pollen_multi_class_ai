from os import path
from database.ops import ClassNames

dir_path = path.dirname("./")

class_names_file = dir_path + "/../database/pollen_info.json"

# Create an instance of ClassNames
class_names_instance = ClassNames(class_names_file)
