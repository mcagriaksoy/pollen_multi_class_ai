from PyQt6.QtWidgets import QApplication, QMessageBox, QProgressBar
from PyQt6.QtCore import Qt
'''
def create_popup(title, message):
    app = QApplication([])  # Create an application instance

    # Create a message box
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    
    # Show the message box
    msg_box.exec()
'''
class ProgressPopUp:
    def __init__(self, text):
        self.msg_box = QMessageBox()
        self.msg_box.setWindowTitle("Progress")
        self.msg_box.setText(text)
        self.msg_box.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.msg_box.setWindowModality(Qt.WindowModality.ApplicationModal)

    def show_popup(self):
        self.msg_box.show()

    def hide_popup(self):
        self.msg_box.hide()

    def destroy_popup(self):
        self.msg_box.close()