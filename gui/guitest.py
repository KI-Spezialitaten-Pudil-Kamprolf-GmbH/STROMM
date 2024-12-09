from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget

import sys


GUI_APP_VERSION_STR = "2024.12A"

GUI_WINDOW_WIDTH = 500
GUI_WINDOW_HEIGHT = 400

class MainWindow(QMainWindow):
    clickCount = 0

    def __init__(self, title):
        super().__init__()

        self.setWindowTitle(title)
        self.setFixedSize(GUI_WINDOW_WIDTH, GUI_WINDOW_HEIGHT)

        # Initialize window elements
        self.button = QPushButton("Test button")
        self.button.setFixedSize(100, 40)
        self.button.setCheckable(True)
        self.button.pressed.connect(self.event_button_clicked)

        self.label = QLabel("Button pressed: " + str(self.clickCount) + " times")
        self.label.setFixedSize(100, 40)

        self.input = QLineEdit("")
        self.input.setFixedSize(200, 40)
        self.input.textChanged.connect(self.event_input_textChanged)

        # Set layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def event_button_clicked(self):
        self.clickCount += 1
        self.label.setText(self.input.text() + " " + str(self.clickCount))

    def event_input_textChanged(self):
        self.label.setText(self.input.text() + " " + str(self.clickCount))

# QApplication nimmt Argumente als Parameter:
# Entweder sys.argv für Programmparameter oder [] für leere Liste
app = QApplication([])

print("Initializing main GUI.")
window = MainWindow("KI-PK NN for Energy infrastructure management Ver. " + GUI_APP_VERSION_STR)
# TODO: Set Window title here somehow
window.show()

app.exec()