############################################
# Mehmet Cagri Aksoy - 2024
# This is the main file for the pollen classification app.
# It loads the UI file, connects the button signals to their respective slots, and runs the app.
# The app allows the user to select an image file and classify it using a pre-trained model.
# The top 5 predicted classes and their probabilities are displayed in a QListWidget.
# The app uses a TensorFlow model to classify the images.
############################################

import os
import numpy as np
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QPixmap, QColor

from PIL import Image

try:
    import tensorflow as tf
except ImportError:
    os.system('pip install tensorflow')
    import tensorflow as tf


# Load the pre-trained model
# Get current location
dir_path = os.path.dirname(os.path.realpath(__file__))
saved_model_path = (dir_path +'/../model/model.h5')

# Load the model
try:
    model = tf.keras.models.load_model(saved_model_path)
except Exception as e:
    print("Error loading the model:", e)

# List of class names
# Read class names from a file
class_names = ['acacia_plumosa', 'acrocomia_aculeta', 'anadenanthera_colubrina', 'arachis_sp', 'arecaceae', 'arrabidaea_florida', 'aspilia_grazielae', 'bacopa_australis', 'caesalpinia_peltophoroides', 'caryocar_brasiliensis', 'cecropia_pachystachya', 'ceiba_speciosa', 'chromolaena_laevigata', 'cissus_campestris', 'cissus_spinosa', 'combretum_discolor', 'cordia_trichotoma', 'cosmos_caudatus', 'croton_urucurana', 'dianella_tasmanica', 'dipteryx_alata', 'doliocarpus_dentatus', 'erythrina_mulungu', 'eucalyptus_sp', 'faramea_sp', 'genipa_auniricana', 'gomphrena_sp', 'guapuruvu', 'guazuma_ulmifolia', 'hortia_oreadica', 'hyptis_sp', 'ligustrum_lucidum', 'luehea_divaricata', 'mabea_fistulifera', 'machaerium_aculeatum', 'magnolia_champaca', 'manihot_esculenta', 'matayba_guianensis', 'mauritia_flexuosa', 'mimosa_ditans', 'mimosa_pigra', 'mitostemma_brevifilis', 'myracroduon_urundeuva', 'myrcia_guianensis', 'ochroma_pyramidale', 'ouratea_hexasperma', 'pachira_aquatica', 'palmeira_real', 'passiflora_gibertii', 'paullinia_spicata', 'piper_aduncum', 'poaceae_sp', 'protium_heptaphyllum', 'qualea_multiflora', 'ricinus_communis', 'schinus_sp', 'senegalia_plumosa', 'serjania_erecta', 'serjania_hebecarpa', 'serjania_laruotteana', 'serjania_sp', 'sida_cerradoensis', 'solanum_sisymbriifolium', 'syagrus', 'syagrus_romanzoffiana', 'symplocos_nitens', 'tabebuia_chysotricha', 'tabebuia_rosealba', 'tapirira_guianensis', 'tradescantia_Pallida', 'trema_micrantha', 'trembleya_phlogiformis', 'tridax', 'tridax_procumbens', 'urochloa', 'vochysia_divergens', 'zea_mays']

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Initialize the main window and load the UI file.
        Connect the button signals to their respective slots.
        """
        super(Ui, self).__init__()
        uic.loadUi('ui.ui', self)  # Load the .ui file
        self.classifyButton.setEnabled(False)

        self.pushButton.clicked.connect(self.load_img)
        self.classifyButton.clicked.connect(self.classify)
        self.pushButton_2.clicked.connect(self.clear)

        #Disable classify button if model is not loaded
        if not model:
            self.classifyButton.setEnabled(False)
            self.label_2.setText("Model yüklenirken bir hata oluştu. Lütfen tekrar deneyin.")

        self.show()

    def clear(self):
        """
        Clear the image, image name, and top 5 predicted classes from the UI.
        """
        self.listWidget.clear()
        self.label_3.clear()
        self.label_2.clear()
        self.label.clear()

    def load_img(self):
        """
        Open a file dialog to select an image file.
        Display the selected image in a QLabel.
        Set the image name to another QLabel.
        """
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', dir_path, "Image files (*.jpg *.png *.bmp *.heic *.jpeg)")
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
        self.label_2.setText(os.path.basename(self.image_path))

    def classify(self):
        """
        Load the selected image, preprocess it, and classify it using the pre-trained model.
        Display the top 5 predicted classes and their probabilities in a QListWidget.
        """
        original = Image.open(self.image_path).resize((128, 128))
        numpy_image = np.array(original)
        image_batch = np.expand_dims(numpy_image, axis=0)
        processed_image = image_batch / 255.0
        prediction = model.predict(processed_image)
        # Instead of printing the maximum predicted value, print the top 10 classes and their probabilities
        top_10 = np.argsort(prediction[0])[-10:][::-1]
        # Clear the list
        self.listWidget.clear()

        for i in top_10:
            # Print percentage of accuracy instead the raw data
            percentage = prediction[0][i] * 100
            if percentage < 0.1:
                continue
            item = QtWidgets.QListWidgetItem(f"{class_names[i]}: {percentage:.2f}%")
            self.listWidget.addItem(item)

        # Set the background color of the top 5 classes to green
        item = self.listWidget.item(0)
        item.setBackground(QColor(0, 255, 0))

        # set reference image to the label_3
        reference_img = dir_path + '/../reference_polen/' + class_names[top_10[0]] + '_0001.png'
        pixmap = QPixmap(reference_img)
        self.label_3.setPixmap(pixmap)

app = QtWidgets.QApplication([])
window = Ui()
app.exec()
