import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from UIMainWindow import MainWindow

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)

    mw = MainWindow()
    
    sys.exit(app.exec())