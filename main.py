import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *

form_class = uic.loadUiType('qt/form.ui')[0]


class MyWindow(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
