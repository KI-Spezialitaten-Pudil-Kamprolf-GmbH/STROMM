from typing import override
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPen

# TODO: QThread für GUI-Update während Hintergrundberechnung

GUI_VERSION_STR = "2025.3A"
GUI_TITLE = "KI-PK NN for Energy Infrastructure Management ver. " + GUI_VERSION_STR

GUI_WINDOW_WIDTH = 500
GUI_WINDOW_HEIGHT = 400

class MainWindow(QMainWindow):
    clickCount = 0

    def __init__(self, title):
        super().__init__()

        self.setWindowTitle(title)
        self.top = 0
        self.left = 0
        self.width = GUI_WINDOW_WIDTH
        self.height = GUI_WINDOW_HEIGHT
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setMouseTracking(True)

        self.INIT_GUI_ELEMENTS()

    def INIT_GUI_ELEMENTS(self):
        # Initialize window elements
        self.label = QLabel("")
        self.label.setFixedSize(100, 40)

        # Set layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(self.label)
        container = QWidget()
        container.setLayout(layout)
        #self.setCentralWidget(container)
        return
    
    @override
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.green,  8, Qt.DashLine))
        painter.drawEllipse(40, 40, 400, 400)

if __name__ == "__main__":
    import sys

    # QApplication nimmt Argumente als Parameter:
    # Entweder sys.argv für Programmparameter oder [] für leere Liste
    app = QApplication([])

    print("Initializing main GUI.")
    window = MainWindow(GUI_TITLE)
    window.show()

    app.exec()