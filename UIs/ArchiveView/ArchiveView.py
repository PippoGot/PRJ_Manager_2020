from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from .archive_view import Ui_uiArchiveView as ui

class ArchiveView(qtw.QWidget, ui):
    def __init__(self):
        """
        Loads the UI window and connects the buttons to the event handler.
        """

        super(ArchiveView, self).__init__()
        self.setupUi(self)

        self.model = None

        self.uiMEHBtn.clicked.connect(self._updateFilter)
        self.uiELHBtn.clicked.connect(self._updateFilter)
        self.uiEMHBtn.clicked.connect(self._updateFilter)
        self.uiMMHBtn.clicked.connect(self._updateFilter)
        self.uiPROBtn.clicked.connect(self._updateFilter)
        self.uiSearchEntry.textChanged.connect(self._updateFilter)

    def setModel(self, model):
        """
        Sets this view model.

        Args:
            model (ArchiveModel): the model to visualize
        """

        self.model = model
        self.uiView.setModel(self.model)

    def _updateFilter(self):
        pass

# MAIN
if __name__ == '__main__':
    import sys
    app = qtw.QApplication(sys.argv)

    mw = ArchiveView()
    mw.show()

    app.exec_()