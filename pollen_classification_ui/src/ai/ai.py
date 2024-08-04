from shared import class_names_instance
from paths.paths import path_manager
from ui.ui import ui_manager
from popup.popup import ProgressPopUp

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QListWidgetItem
from numpy import ndarray, float32, array, expand_dims, argsort
from PIL import Image
from os import path
from onnxruntime import InferenceSession
from PyQt6.QtGui import QPixmap, QColor

# Model definition
MODEL = None
image_path = None

dir_path = path.dirname("./")
saved_model_path = dir_path + "/../model/model_v13.onnx"
# Check there is a model file on the given dir
if not path.exists(saved_model_path):
    ERROR = "Model dosyası bulunamadı. Lütfen model dosyasını kontrol edin."

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

class LoadModelThread(QThread):
    finished = pyqtSignal()
    
    def __init__(self, parent=None):
        super(LoadModelThread, self).__init__(parent)

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
    
    def stop(self):
        self.quit()
        self.wait()

def load_img(self):
        """
        Open a file dialog to select an image file.
        Display the selected image in a QLabel.
        Set the image name to another QLabel.
        """
        try:
            fname = QFileDialog.getOpenFileName(
                None, 
                "Open file",
                dir_path,
                "Image files (*.jpg *.png *.bmp *.heic *.jpeg)",
            )
        except Exception as e:
            print("Seçilen görüntü açılamadı Hata kodu:", e)
            return

        # clear all
        #self.clear()
        ui = ui_manager.get_ui()
        # Enable classify button
        ui.classifyButton.setEnabled(True)

        global image_path
        image_path = fname[0]
        path_manager.set_path('image_path', image_path)
        pixmap = QPixmap(image_path)


        ui.yuklenen_polen.setPixmap(pixmap)
        # Set image name to label_2
        ui.label_2.setText(path.basename(image_path))

def display_prediction(self, prediction):
    
    # Clear the list
    self.siniflandirma_sonuc_list.clear()

    top_10 = argsort(prediction[0])[-10:][::-1]

    for i in top_10:
        # Print percentage of accuracy instead the raw data
        percentage = prediction[0][i] * 100
        if percentage < 0.11:
            continue
        
        name = class_names_instance.get_class_names().get(i)
        #name = "Class"
        item = QListWidgetItem(f"{name}: {percentage:.2f}%")
        self.siniflandirma_sonuc_list.addItem(item)

    # Set the background color of the top 5 classes to green
    item = self.siniflandirma_sonuc_list.item(0)
    item.setBackground(QColor(0, 255, 0))

def classify(main_window):
        """
        Load the selected image, preprocess it, and classify it using the pre-trained model.
        Display the top 5 predicted classes and their probabilities in a QListWidget.
        """
        original = Image.open(image_path).resize((50, 50))
        original = original.convert("RGB")
        numpy_image = array(original)
        image_batch = expand_dims(numpy_image, axis=0)
        processed_image = image_batch / 255.0
        
        popup = ProgressPopUp("Sınıflandırılıyor, lütfen bekleyin...")
        popup.show_popup()

        main_window.classify_thread = ClassifyThread(processed_image)
        main_window.classify_thread.finished.connect(lambda prediction: display_prediction(main_window, prediction))
        main_window.classify_thread.start()