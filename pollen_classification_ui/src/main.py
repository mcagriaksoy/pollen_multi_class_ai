############################################
# Mehmet Cagri Aksoy - 2024
# This is the main file for the pollen classification app.
# It loads the UI file, connects the button signals to their respective slots, and runs the app.
# The app allows the user to select an image file and classify it using a pre-trained model.
# The top 5 predicted classes and their probabilities are displayed in a QListWidget.
# The app uses an ONNX model to classify the images.
############################################

from os import listdir, path, remove
from numpy import ndarray, float32, array, expand_dims, argsort

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QMainWindow,
    QListWidgetItem,
    QApplication,
)
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import QThread, pyqtSignal, Qt
import webbrowser
from PIL import Image, ImageFilter

from onnxruntime import InferenceSession

# Error message definition
ERROR = ""

# Model definition
MODEL = None

# Load the pre-trained model
# Get current location

# If operating system is windows
dir_path = path.dirname("./")
saved_model_path = dir_path + "/../model/mobilenet_model.onnx"
# Check there is a model file on the given dir
if not path.exists(saved_model_path):
    ERROR = "Model dosyası bulunamadı. Lütfen model dosyasını kontrol edin."

# List of class names
# Read class names from a file
class_names = {}
try:
    with open(dir_path + "/desteklenen_polenler.txt", "r") as file:
        if not file:
            raise Exception(
                "Sınıf isimleri okunurken bir hata oluştu. Lütfen tekrar deneyin."
            )
        for line in file:
            class_str, key = line.strip().split(":")
            class_names[int(key)] = class_str
except Exception as e:
    ERROR = (
        "Sınıf isimleri okunurken bir hata oluştu. Lütfen tekrar deneyin. Hata kodu: "
        + str(e)
    )


class LoadModelThread(QThread):
    finished = pyqtSignal()

    def run(self):
        try:
            global MODEL
            MODEL = InferenceSession(saved_model_path)
        except Exception as e:
            print("Error loading the model:", e)

        # Disable classify button if model is not loaded
        if not MODEL:
            ERROR = "Model yüklenirken bir hata oluştu. Lütfen tekrar deneyin."
            # exit the thread
        self.finished.emit()


class ClassifyThread(QThread):
    finished = pyqtSignal(ndarray)

    def __init__(self, processed_image):
        super(ClassifyThread, self).__init__()
        self.processed_image = processed_image

    def run(self):
        input_name = MODEL.get_inputs()[0].name
        output_name = MODEL.get_outputs()[0].name
        prediction = MODEL.run(
            [output_name], {input_name: self.processed_image.astype(float32)}
        )
        self.finished.emit(prediction[0])


class Ui(QMainWindow):
    def __init__(self):
        """
        Initialize the main window and load the UI file.
        Connect the button signals to their respective slots.
        """
        super(Ui, self).__init__()
        self.selected_class_name = "Hata!"
        uic.loadUi("ui.ui", self)  # Load the .ui file

        self.classifyButton.setEnabled(False)
        self.pushButton.clicked.connect(self.load_img)
        self.classifyButton.clicked.connect(self.classify)
        self.pushButton_2.clicked.connect(self.clear)
        self.listWidget.itemClicked.connect(self.display_predicted_image)
        self.pushButton_4.clicked.connect(self.google_search)

        self.show()
        # If ERROR str is not empty show the error message
        if ERROR:
            # Create a message box, if okay clicked close the program
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText(ERROR)
            msg.setWindowTitle("Hata")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            exit(1)

        else:
            self.loading_popup_show(
                "Lütfen Bekleyiniz!\nGereken model dosyaları yükleniyor...\n"
            )
            # Create an instance of the LoadModelThread
            self.m_thread = LoadModelThread()
            self.m_thread.finished.connect(self.loading_popup_hide)
            self.m_thread.start()

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

            # Print Original version
            pixmap = QPixmap(image_path)
            self.label_3.setPixmap(pixmap)

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
        if self.listWidget.count() == 0:
            return

        url = "https://www.google.com/search?q=" + self.selected_class_name
        webbrowser.open_new_tab(url)

    def loading_popup_show(self, str):
        """Show the information"""
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Icon.Information)
        self.msg.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.msg.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.msg.setText(str)

        self.progress = QProgressBar(self.msg)
        self.progress.setGeometry(60, 45, 200, 15)
        self.progress.setMaximum(0)
        self.progress.setMinimum(0)
        self.progress.setValue(0)
        self.msg.show()

    def loading_popup_hide(self):
        """Hide the information"""
        # delete the message
        self.msg.deleteLater()
        self.progress.deleteLater()

    def loading_popup_hide(self):
        """Hide the information"""
        # delete the message
        self.msg.deleteLater()

    def clear(self):
        """
        Clear the image, image name, and top 5 predicted classes from the UI.
        """
        self.listWidget.clear()
        self.label_3.clear()
        self.label_9.clear()
        self.label_2.clear()
        self.label.clear()

    def load_img(self):
        """
        Open a file dialog to select an image file.
        Display the selected image in a QLabel.
        Set the image name to another QLabel.
        """
        try:
            fname = QFileDialog.getOpenFileName(
                self,
                "Open file",
                dir_path,
                "Image files (*.jpg *.png *.bmp *.heic *.jpeg)",
            )
        except Exception as e:
            print("Seçilen görüntü açılamadı Hata kodu:", e)
            return

        # clear all
        self.clear()

        self.classifyButton.setEnabled(True)
        self.image_path = fname[0]
        pixmap = QPixmap(self.image_path)
        self.label.setPixmap(pixmap)
        # Set image name to label_2
        self.label_2.setText(path.basename(self.image_path))

    def classify(self):
        """
        Load the selected image, preprocess it, and classify it using the pre-trained model.
        Display the top 5 predicted classes and their probabilities in a QListWidget.
        """
        original = Image.open(self.image_path).resize((50, 50))
        original = original.convert("RGB")
        numpy_image = array(original)
        image_batch = expand_dims(numpy_image, axis=0)
        processed_image = image_batch / 255.0
        self.loading_popup_show("Lütfen Bekleyiniz!\nGörüntü sınıflandırılıyor...\n")
        self.predict_thread = ClassifyThread(processed_image)
        self.predict_thread.finished.connect(self.display_prediction)
        self.predict_thread.start()

    def display_prediction(self, prediction):
        self.loading_popup_hide()
        # Clear the list
        self.listWidget.clear()

        top_10 = argsort(prediction[0])[-10:][::-1]

        for i in top_10:
            # Print percentage of accuracy instead the raw data
            percentage = prediction[0][i] * 100
            if percentage < 0.11:
                continue
            item = QListWidgetItem(f"{class_names[i]}: {percentage:.2f}%")
            self.listWidget.addItem(item)

        # Set the background color of the top 5 classes to green
        item = self.listWidget.item(0)
        item.setBackground(QColor(0, 255, 0))


app = QApplication([])

window = Ui()
app.exec()
