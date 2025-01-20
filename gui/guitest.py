from typing import override
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap


GUI_APP_VERSION_STR = "2024.12A"
GUI_TITLE = "KI-PK NN for Energy Infrastructure Management ver. " + GUI_APP_VERSION_STR

GUI_WINDOW_WIDTH = 500
GUI_WINDOW_HEIGHT = 400

class MainWindow(QMainWindow):
    clickCount = 0

    def __init__(self, title):
        super().__init__()

        self.setWindowTitle(title)
        self.setFixedSize(GUI_WINDOW_WIDTH, GUI_WINDOW_HEIGHT)
        self.setMouseTracking(True)

        # Initialize window elements
        self.label = QLabel("")
        self.label.setFixedSize(100, 40)

        # Set layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(self.label)
        container = QWidget()
        container.setLayout(layout)
        container.setMouseTracking(True)

        self.label2 = QLabel()
        self.img = QPixmap("C:\\Users\\Theophil\\Downloads\\RDT_20250115_1425031785123197527477889.jpg")
        self.img = self.img.scaledToWidth(500)#.scaledToHeight(400)
        self.label2.setPixmap(self.img)

        self.setCentralWidget(self.label2)
        #self.setCentralWidget(container)

    def event_button_clicked(self):
        self.clickCount += 1
        self.label.setText(self.input.text() + " " + str(self.clickCount))
    
    @override
    def mouseMoveEvent(self, event):
        pos = event.pos()
        relX = pos.x() / self.width()
        relY = pos.y() / self.height()
        self.label.setText("X: " + str(relX) + ", Y: " + str(relY))
        self.img.scaledToHeight(500*relY)
        event.accept()
        # return super().mouseMoveEvent(event)


if __name__ == "__main__":
    import sys

    # QApplication nimmt Argumente als Parameter:
    # Entweder sys.argv für Programmparameter oder [] für leere Liste
    app = QApplication([])

    print("Initializing main GUI.")
    window = MainWindow(GUI_TITLE)
    window.show()

    app.exec()