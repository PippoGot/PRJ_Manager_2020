from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from ..ComponentEditor.ComponentEditor import ComponentEditor
from ..NewComponentEditor.NewComponentEditor import NewComponentEditor

from .components_page import  Ui_uiComponentsPage as ui

class ComponentsPage(qtw.QWidget, ui):
    def __init__(self):
        """
        Loads the UI window and set the manufacture model.
        """

        super(ComponentsPage, self).__init__()
        self.setupUi(self)

        self.model = None
        self.uiEditor = ComponentEditor()
        self.horizontalLayout.addWidget(self.uiEditor)

    def setModel(self, model):
        """
        Sets the editor's and view's model, then refreshes the view.

        Args:
            model (ModelTree): the model of the view and editor widget
        """

        self.model = model
        self.uiView.setModel(self.model)
        self.uiEditor.setModel(model)

        if self.model:
            self.selection = self.uiView.selectionModel()
            self.selection.currentChanged.connect(self._mapIndex)

        self._resizeView()

    def setManufactureModel(self, manufactureModel):
        """
        Sets the editor's manufacture combobox model.

        Args:
            manufactureModel (ModelCombobox): the model of the combobox
        """

        self.uiEditor.setManufactureModel(manufactureModel)

    def setStatusModel(self, statusModel):
        """
        Sets the editor's status combobox model.

        Args:
            statusModel (ModelCombobox): the model of the combobox
        """

        self.uiEditor.setStatusModel(statusModel)

    def getNewNode(self, tp):
        parentNode = self.uiEditor.currentNode
        return self.model.getNewNode(parentNode, tp)

    def _mapIndex(self, index):
        """
        The index is set as the current index of the editor.

        Args:
            index (QModelIndex): the index to update
        """

        self.uiEditor.setCurrentSelection(index)

    def _resizeView(self):
        """
        Updates the view resizing the columns to a specified value and expanding the tree.
        """

        self.uiView.expandAll()
        for column in range(self.model.columnCount(qtc.QModelIndex())):
            self.uiView.resizeColumnToContents(column)

    def addNode(self, newNode):
        parentItem = self.uiEditor.currentNode
        currentSelection = self.uiEditor.currentIndex

        self.model.insertRows(len(parentItem), newNode, currentSelection)

        self._resizeView()

# MAIN
if __name__ == '__main__':
    import sys
    app = qtw.QApplication(sys.argv)

    mw = ComponentsPage()
    mw.show()

    app.exec_()