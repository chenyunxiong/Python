import sys
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMenu, QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel()

    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction('test1', self))
        context.addAction(QAction('test2', self))
        context.exec(e.globalPos())


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()