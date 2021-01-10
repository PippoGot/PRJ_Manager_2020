from PyQt5 import QtWidgets as qtw

from uis.main_window.MainWindow import MainWindow

if __name__ == '__main__':
    import sys
    app = qtw.QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    app.exec_()