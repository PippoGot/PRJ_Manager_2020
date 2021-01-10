from uis.settings_window.SettingsWindow import SettingsWindow
from PyQt5 import QtWidgets as qtw

if __name__ == '__main__':
    import sys
    app = qtw.QApplication(sys.argv)

    mw = SettingsWindow()
    mw.show()

    print(mw.getRecentFilesList()[0])

    app.exec_()