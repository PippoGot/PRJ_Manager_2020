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
        self.currentNode = None
        self.currentIndex = None
        self.currentSelection = None

        self.layout().insertWidget(1, self.uiArchiveView)
        self.layout().insertWidget(2, self.uiEditor)

        self.uiAddBtn.clicked.connect(self._addNode)
        self.uiDelBtn.clicked.connect(self._deleteNode)
        self.uiArchiveView.indexChanged.connect(self.setCurrentSelection)

        self._disableRemove()

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

    def setCurrentSelection(self, index):
        """
        Updates the currently selected model index for the editor.

        Args:
            index (QModelIndex): the new index
        """

        self.uiEditor.setCurrentSelection(index)
        self.currentIndex = self.uiEditor.currentIndex
        self.currentNode = self.uiEditor.currentNode
        self.currentSelection = self.uiArchiveView.indexSelection
        self._disableRemove()

    def _addNode(self):
        pass

    def _deleteNode(self):
        """
        Removes the currently selected node from the archive model.
        """

        if self.currentIndex:
            indexSet = {index.siblingAtColumn(0) for index in self.currentSelection}
            for index in indexSet:
                self.model.removeRows(index)

            self.currentNode = None
            self.currentIndex = None
            self.currentSelection = None

            self._disableRemove()
            self._updateNewNode()

    def _disableRemove(self):
        """
        Disables the delete button based on the current selection.
        """

        self.uiDelBtn.setDisabled(not self.currentIndex)

    def _updateNewNode(self):
        pass