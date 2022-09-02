import imp
import sys
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout, QTabWidget
from PySide6.QtGui import QColor, QPalette

class WidgetColor(QWidget):
    def __init__(self, color):
        super().__init__()

        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # layout = QHBoxLayout()
        # layout.setSpacing(0)
        # layoutV = QVBoxLayout()
        # layoutV.setSpacing(10)
        # layout.addWidget(WidgetColor("red"))
        # layout.addLayout(layoutV)
        # layout.addWidget(WidgetColor("yellow"))
        # layout.addWidget(WidgetColor("green"))

        # layoutV.addWidget(WidgetColor("orange"))
        # layoutV.addWidget(WidgetColor("black"))

        # layout = QGridLayout()
        # layout.addWidget(WidgetColor("yellow"), 0, 0)
        # layout.addWidget(WidgetColor("green"), 1, 1)
        # layout.addWidget(WidgetColor("red"), 2, 2)

        layout = QStackedLayout()
        layout.addWidget(WidgetColor('yellow'))
        layout.addWidget(WidgetColor('blue'))
        layout.addWidget(WidgetColor('green'))
        layout.addWidget(WidgetColor('red'))
        # layout.setCurrentIndex(2)

        tabWidget = QTabWidget()
        tabWidget.setTabPosition(QTabWidget.South)
        tabWidget.setMovable(True)
        for name in ["red", "blue", "green", "red"]:
            tabWidget.addTab(WidgetColor(name), name)



        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(tabWidget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
