
import os
import json

class ClassNames:
    def __init__(self, file_path):
        self.names_array = []
        self.load_class_names(file_path)

    def load_class_names(self, file_path):
        try:
            # Open and read the JSON file
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                pollens = data.get('pollens', [])

                # Extract cins_name and epitet_name from each pollen entry and save in array
                for i in range(len(pollens)):
                    cins_name = pollens[i].get('cins_name', '')
                    epitet_name = pollens[i].get('epitet_name', '')
                    self.names_array.append(f"{cins_name}_{epitet_name}")
            
        except Exception as e:
            self.ERROR = (
                "Sınıf isimleri okunurken bir hata oluştu. Lütfen tekrar deneyin. Hata kodu: "
                + str(e)
            )
    
    def get_class_names(self):
        return self.names_array
    
    def get_class_names(self, n):
        return self.names_array[n]


def bilgileriGetir(main_window, top_class):
    class_list = top_class.split("_")
    print(class_list)
    # Get the first element of the list
    sinif = class_list[0]
    epitet = class_list[1]

    main_window.bulunan_sinif.setText(sinif)
    main_window.bulunan_epitet.setText(epitet)

def veritabaniGuncelleJson(self, epitet, sinif, location, shape, json_file_path):
    # Update the JSON file. If the class does not exist, create it. Otherwise update the existing class.
    
    if not os.path.exists(json_file_path):
        with open(json_file_path, "w") as file:
            file.write("{}")
    
    with open(json_file_path, "r") as file:
        data = json.load(file)

        if sinif not in data:
            data[sinif] = {}
        
        if epitet not in data[sinif]:
            data[sinif][epitet] = {}

        data[sinif][epitet]["location"] = location
        data[sinif][epitet]["shape"] = shape
        
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)
