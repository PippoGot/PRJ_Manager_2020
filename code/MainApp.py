import sys
from PyQt5 import QtWidgets as qtw

from UIMainWindow import MainWindow

from stylesheet import stylesheet

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyleSheet(stylesheet)

    mw = MainWindow()

    sys.exit(app.exec())
