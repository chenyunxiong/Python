import imp
import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QPushButton

def click():
    print("aaa")
    return

def main():
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle("app")
    btn = QPushButton('button', w)
    btn.actionEvent = click
    btn.move(50, 50)
    w.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()