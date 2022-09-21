from enum import Flag
from tabnanny import check
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PySide6.QtCore import QSize, Qt

# Only needed for access to command line arguments
import sys

window_titles = [
    "app1",
    "app2",
    "app3",
]

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.button_is_checked = True
        self.clickIndex = 0

        self.setWindowTitle("App")

        self.button = QPushButton("Button")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.the_button_was_clicked)
        # self.button.clicked.connect(self.the_button_was_toggle)
        # self.button.setChecked(self.button_is_checked)
        self.windowTitleChanged.connect(self.the_window_title_change)

        self.button.setFixedSize(100, 200)
        self.setFixedSize(400, 400)
        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        self.setWindowTitle(window_titles[self.clickIndex])
        self.clickIndex += 1
        print("click button~")

    def the_button_was_toggle(self):
        # self.setWindowTitle("App2")
        print("checked", self.button_is_checked)

    def the_window_title_change(self, title):
        if title == "app3":
            self.button.setDisabled(True)
        


# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.