import imp
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QLabel, QStatusBar, QCheckBox, QMenuBar
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        toolbar = QToolBar("main tool bar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        button_action = QAction(QIcon('bug.png'), "button", self)
        button_action.setStatusTip("btn")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        button_action2 = QAction(QIcon('bug.png'), "button", self)
        button_action2.setStatusTip("btn")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        # button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        # button_action3 = QAction(QIcon('bug.png'), "button", self)
        # button_action3.setStatusTip("btn")
        # button_action3.triggered.connect(self.onMyToolBarButtonClick)

        # toolbar.addSeparator()
        # toolbar.addWidget(QLabel("label"))
        # toolbar.addSeparator()
        # toolbar.addWidget(QCheckBox())

        # self.setStatusBar(QStatusBar(self))
        # self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        # menubar = self.menuBar()
        # menu = menubar.addMenu('%menu1')
        # menu.addAction(button_action2)
        # menu.addSeparator()
        # # menu.addAction(button_action3)
        # # menu.addSeparator()
        # subMenu = menu.addMenu("subItem")
        # subMenu.addAction(button_action2)




    def onMyToolBarButtonClick(self):
        print(".....click")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
