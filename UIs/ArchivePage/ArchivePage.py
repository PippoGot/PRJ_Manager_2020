from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from ..ComponentEditor.ComponentEditor import ComponentEditor
from ..ArchiveView.ArchiveView import ArchiveView

from .archive_page import Ui_uiArchivePage as ui

class ArchivePage(qtw.QWidget, ui):
    def __init__(self):
        """
        Loads the UI window and set the manufacture model.
        """

        super(ArchivePage, self).__init__()
        self.setupUi(self)

        self.uiArchiveView = ArchiveView()
        self.uiEditor = ComponentEditor()

        self.model = None
        self.manufactureModel = None
        self.statusModel = None

        self.layout().insertWidget(1, self.uiArchiveView)
        self.layout().insertWidget(2, self.uiEditor)

    def setModel(self, model):
        """
        Sets the editor's and view's model.

        Args:
            model (ModelTree): the model of the view and editor widget
        """

        self.model = model
        self.uiArchiveView.setModel(self.model)
        self.uiEditor.setModel(self.model)

    def setManufactureModel(self, manufactureModel):
        """
        Sets the editor's manufacture combobox model.

        Args:
            manufactureModel (ModelCombobox): the model of the combobox
        """

        self.manufactureModel = manufactureModel
        self.uiEditor.setManufactureModel(manufactureModel)
        self.editable.setModel(self.manufactureModel)

    def setStatusModel(self, statusModel):
        """
        Sets the editor's status combobox model.

        Args:
            statusModel (ModelCombobox): the model of the combobox
        """

        self.statusModel = statusModel
        self.uiEditor.setStatusModel(statusModel)
        self.uiStatus.setModel(self.statusModel)

# MAIN
if __name__ == '__main__':
    import sys
    app = qtw.QApplication(sys.argv)

    mw = ArchivePage()
    mw.show()

    app.exec_()