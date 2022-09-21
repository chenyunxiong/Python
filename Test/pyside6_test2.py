from operator import contains
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('App')

        self.label = QLabel()
        self.label2 = QLabel()
        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)
        self.label2.setText('click me please')

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)
        layout.addWidget(self.label2)

        contains = QWidget()
        contains.setLayout(layout)

        self.setCentralWidget(contains)
    
    def mouseMoveEvent(self, event):
        print('on monse move:', event)
    
    def mousePressEvent(self, event):
        print('on mouse press')

    def mouseDoubleClickEvent(self, event):
        print('on mouse mouseDoubleClickEvent')


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()