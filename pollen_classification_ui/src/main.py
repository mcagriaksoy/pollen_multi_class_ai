############################################
# Mehmet Cagri Aksoy - 2024
# This is the main file for the pollen classification app.
# It loads the UI file, connects the button signals to their respective slots, and runs the app.
# The app allows the user to select an image file and classify it using a pre-trained model.
# The top 5 predicted classes and their probabilities are displayed in a QListWidget.
# The app uses an ONNX model to classify the images.
############################################

from shared import class_names_instance
from popup.popup import ProgressPopUp
from database.ops import bilgileriGetir, veritabaniGuncelleJson
from ai.ai import ClassifyThread, LoadModelThread, classify, load_img
from paths.paths import path_manager
from ui.ui import ui_manager
from os import listdir, path, remove, scandir
from numpy import float32, array, argsort

from PyQt6.QtWidgets import (
    QMessageBox,
    QMainWindow,
    QApplication,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import webbrowser
from PIL import Image, ImageFilter
#from folium import Map, Polygon
#from onnxruntime import InferenceSession

# Error message definition
ERROR = ""


# Load the pre-trained model
# Get current location

# If operating system is windows
dir_path = path.dirname("./")
class_dir = dir_path + "/../referans_polen/"
DATABASE_PATH = dir_path + "/../database/pollen_info.json"

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initialize the main window and load the UI file.
        Connect the button signals to their respective slots.
        """
        super(MainWindow, self).__init__()
       
        ui_manager.load_ui(self)
        self.ui = ui_manager.get_ui()

        self.selected_class_name = "Hata!"
        self.popup = None
        self.show_error_popup("Loading, please wait...")
        
        self.classifyButton.setEnabled(False)

        self.diskten_polen_yukle.clicked.connect(load_img)

        self.classify_thread = None
        self.classifyButton.clicked.connect(lambda: classify(self))

        self.pushButton_2.clicked.connect(self.clear)
        self.siniflandirma_sonuc_list.itemClicked.connect(self.display_predicted_image)
        self.listWidget_4.itemClicked.connect(self.show_locations)
        self.web_ara.clicked.connect(self.google_search)
        self.polen_arama_buton.clicked.connect(self.polen_listele)

        self.taksonomik_arama.clicked.connect(lambda: self.tabWidget.setCurrentIndex(1))
        self.taksonomik_arama.clicked.connect(lambda: self.toolBox.setCurrentIndex(0))
        self.resim_ile_arama.clicked.connect(lambda: self.tabWidget.setCurrentIndex(1))
        self.resim_ile_arama.clicked.connect(lambda: self.toolBox.setCurrentIndex(1))
        self.bolgeye_gore_arama.clicked.connect(lambda: self.tabWidget.setCurrentIndex(1))
        self.bolgeye_gore_arama.clicked.connect(lambda: self.toolBox.setCurrentIndex(2))
        self.detayli_arama.clicked.connect(lambda: self.tabWidget.setCurrentIndex(1))
        self.detayli_arama.clicked.connect(lambda: self.toolBox.setCurrentIndex(2)) # todo: change to 3

        self.veritabanina_kaydet.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
        self.veritabanina_kaydet.clicked.connect(lambda: bilgileriGetir(self, self.siniflandirma_sonuc_list.item(0).text()))
        
        self.veritabanina_gonder.clicked.connect(self.json_guncelle)

        # Show the UI!
        self.show()
        
        # If ERROR str is not empty show the error message

        if ERROR:
            # Create a message box, if okay clicked close the program
            self.show_error_popup(ERROR)

        else:
            popup = ProgressPopUp("Lütfen Bekleyiniz!\nGereken model dosyaları yükleniyor...\n")
            popup.show_popup()
            # Create an instance of the LoadModelThread
            self.m_thread = LoadModelThread()
            self.m_thread.finished.connect(popup.hide_popup)
            self.m_thread.start()

    def json_guncelle(self):
        """
        Update the database with the selected class.
        """
        sinif = self.bulunan_sinif.toPlainText()
        epitet = self.bulunan_epitet.toPlainText()
        location = self.ulke.currentText() + ", " + self.ulke.currentText() + ", " + self.ilce.currentText()
        shape = self.sekil.currentText()
        # Update the Json file
        veritabaniGuncelleJson(self, sinif, epitet, location, shape, DATABASE_PATH)

    
    def show_error_popup(self, error_message):
        popup = ProgressPopUp(error_message)
        popup.show_popup()

    def polen_listele(self):
        """List the pollen classes in the second tab"""
        # Clear the list
        self.mikroskop_1.clear()
        self.mikroskop_2.clear()
        self.mikroskop_3.clear()

        # Get the class names from comboboxes
        cins = self.comboBox_cins.currentText()
        epitet = self.comboBox_epitet.currentText()

        # Open the class directory
        class_name = cins + "_" + epitet
        class_path = class_dir + class_name
        # Check if the class directory exists
        if not path.exists(class_path):
            # Create a message box, if okay clicked close the program
            # create_popup("Hata", "Sınıf dizini bulunamadı. Lütfen tekrar deneyin.")
            return
        
        # Print the images on the labels
        #self.google_img.setPixmap(QPixmap(class_path + "/google.jpg"))

        # Show the mikroskop images search the all images in the directory
        mikroskop_files = listdir(class_path)
        #for i in range(0, len(mikroskop_files)):
        self.mikroskop_1.setPixmap(QPixmap(class_path + "/" + mikroskop_files[0]))
        #break

    def show_locations(self, item):
        """Show the location of the selected class on the map"""
        self.listWidget_2.clear()
        self.listWidget_2.addItem(polen_locations[selected_class_num])

    def show_global_map(self):
        """
        Show the global map in a web browser.
        """
        if "global_map.html" in listdir():
            webbrowser.open_new_tab("global_map.html")
            return
        m = Map(location=[39.9334, 32.8597], zoom_start=2)
        m.save("global_map.html")
        webbrowser.open_new_tab("global_map.html")

    def show_local_map(self):
        """
        Show the local map in a web browser.
        """
        if "local_map.html" in listdir():
            webbrowser.open_new_tab("local_map.html")
            return
        # Show turkey only!
        m = Map(location=[39.9334, 32.8597], zoom_start=6)
        polygon_coords = [[42, 26], [42, 45], [36, 45], [36, 26]]
        # Add a Polygon to the map
        Polygon(
            locations=polygon_coords,  # coordinates for the polygon (list of lists)
            color="blue",  # color of the polygon
            fill=True,  # fill the polygon with color
            fill_color="blue",  # color to fill the polygon
        ).add_to(m)
        m.save("local_map.html")

    def display_predicted_image(self, item):
        """
        Display the reference image of the selected class in the QListWidget.
        """
        try:
            self.selected_class_name = item.text().split(":")[0]
            image_dir = (
                dir_path + "/../referans_polen/" + self.selected_class_name + "/"
            )
            image_files = listdir(image_dir)
            image_path = path.join(image_dir, image_files[0])
            path_manager.set_path('image_path', image_path)

            # Print Original version
            self.label_3.setPixmap(QPixmap(image_path))

            # Print only edges
            img = Image.open(image_path)
            blur = img.filter(ImageFilter.GaussianBlur(3))
            edges = blur.filter(ImageFilter.CONTOUR)
            edges = edges.filter(ImageFilter.FIND_EDGES)
            edges = edges.filter(ImageFilter.MaxFilter(5))
            # revert black areas to white and white to black
            # edges = edges.point(lambda p: 255 - p)
            edges.save("edges.jpg")
            pixmap = QPixmap("edges.jpg")
            self.label_9.setPixmap(pixmap)
            # remove the edges image
            remove("edges.jpg")

            # Reverse the colors and print
            img = Image.open(image_path)
            img = img.convert("L")
            img = img.point(lambda p: 255 - p)
            img.save("reversed.jpg")
            pixmap = QPixmap("reversed.jpg")
            self.label_10.setPixmap(pixmap)
            # remove the reversed image
            remove("reversed.jpg")

        except Exception as e:
            print("Referans görüntüsü yüklenirken bir hata oluştu. Hata kodu:", e)
            self.label_9.setText("Referans görüntüsü yüklenirken bir hata oluştu.")

    def google_search(self):
        """Search the query in google"""
        if self.siniflandirma_sonuc_list.count() == 0:
            return

        url = "https://www.google.com/search?q=" + self.selected_class_name
        webbrowser.open_new_tab(url)

    def clear(self):
        """
        Clear the image, image name, and top 5 predicted classes from the UI.
        """
        self.siniflandirma_sonuc_list.clear()
        self.label_3.clear()
        self.label_9.clear()
        self.label_10.clear()
        self.label_2.clear()
        self.label.clear()

        self.classifyButton.setEnabled(False)
         #self.pushButton_5.setEnabled(False)
         #self.pushButton_6.setEnabled(False)

app = QApplication([])

window = MainWindow()
app.exec()
