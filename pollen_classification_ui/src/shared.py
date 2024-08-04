from os import path
from database.ops import ClassNames

dir_path = path.dirname("./")

class_names_file = dir_path + "/desteklenen_polenler.txt"

# Create an instance of ClassNames
class_names_instance = ClassNames(class_names_file)
