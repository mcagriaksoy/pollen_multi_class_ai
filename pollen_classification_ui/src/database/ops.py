
import os

class ClassNames:
    def __init__(self, file_path):
        self.class_names = {}
        self.polen_locations = {}
        self.load_class_names(file_path)

    def load_class_names(self, file_path):
        try:
            with open(file_path, "r") as file:
                if not file:
                    raise Exception(
                        "Veritabanı dosyası okunurken bir hata oluştu. Lütfen tekrar deneyin."
                    )
                for line in file:
                    parts = line.split(":")
                    self.class_names[int(parts[1])] = parts[0].strip()
                    self.polen_locations[int(parts[1])] = parts[2].strip()
        except Exception as e:
            self.ERROR = (
                "Sınıf isimleri okunurken bir hata oluştu. Lütfen tekrar deneyin. Hata kodu: "
                + str(e)
            )
    
    def get_class_names(self):
        return self.class_names
    
    def get_polen_locations(self):
        return self.polen_locations


def veritabani_guncelle(main_window, top_class):
    class_list = top_class.split("_")
    # Get the first element of the list
    sinif = class_list[0]
    epitet = class_list[1]

    main_window.bulunan_sinif.setText(sinif)
    main_window.bulunan_epitet.setText(epitet)