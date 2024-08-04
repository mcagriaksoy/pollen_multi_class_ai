from PyQt6 import uic

class UIManager:
    def __init__(self, ui_file):
        self.ui_file = ui_file
        self.ui = None

    def load_ui(self, parent):
        self.ui = uic.loadUi(self.ui_file, parent)

    def get_ui(self):
        return self.ui

# Create a global instance of UIManager
ui_manager = UIManager("ui.ui")