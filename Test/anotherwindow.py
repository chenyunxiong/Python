import imp
from random import randint
import sys
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QPushButton

class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("label %d"%randint(1, 200))
        layout.addWidget(self.label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.wind = None
        self.button = QPushButton('click button')
        self.button.clicked.connect(self.onButtonClick)
        self.setCentralWidget(self.button)

    def onButtonClick(self):
        print("click")
        if self.wind == None:
            self.wind = AnotherWindow()
        self.wind.show()

app = QApplication(sys.argv)
windows = MainWindow()
windows.show()
app.exec()
