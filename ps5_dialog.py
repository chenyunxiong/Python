import imp
import sys
from tkinter import Button
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QDialogButtonBox, QVBoxLayout, QLabel, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        button = QPushButton("button")
        button.clicked.connect(self.onbuttonclick)
        self.setCentralWidget(button)

    def onbuttonclick(self, s):
        print('click ', s)

        dlg = QMessageBox.question(self, "dlg", "???")
        if dlg == QMessageBox.Yes:
            print("yes")
        else:
            print("no")

        # dlg = QMessageBox(self)
        # dlg.setWindowTitle("app box")
        # dlg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # dlg.setText("are you sure to cost money?")
        # res = dlg.exec()
        # if res == QMessageBox.Ok:
        #     print("...........a")
        # else:
        #     print(".............2")

        # dialog = CustomDialog(self)
        # if dialog.exec():
        #     print("confirm click")
        # else:
        #     print("cancel click")

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("my custom dialog")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.btnBox = QDialogButtonBox(QBtn)
        self.btnBox.accepted.connect(self.accept)
        self.btnBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel('you shold cost 1000$! are you sure cost it?')
        self.layout.addWidget(message)
        self.layout.addWidget(self.btnBox)
        self.setLayout(self.layout)

    def acceptClick(self):
        print("on accept click")

    def rejectedClick(self):
        print("on rejected click")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()