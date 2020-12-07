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

        if self.model:
            self.uiView.expandAll()
            for column in range(self.model.columnCount(qtc.QModelIndex())):
                self.uiView.resizeColumnToContents(column)

    def addNode(self, newNode):
        """
        Adds a generic component node to the tree in the selected location.

        Args:
            newNode (ComponentNode): the new node to add
        """

        currentSelection = self.getCurrentIndex()
        parentItem = currentSelection.internalPointer()

        self.model.insertRows(len(parentItem), newNode, currentSelection)

        self._resizeView()

    def getCurrentNode(self):
        """
        Returns the current selected node.

        Returns:
            ComponentNode: the current selected node
        """

        if self.getCurrentIndex():
            return self.getCurrentIndex().internalPointer()

    def getCurrentIndex(self):
        """
        Returns the current selected item's index.

        Returns:
            QModelIndex: the current item's index
        """

        return self.uiEditor.currentIndex

    def getNewNode(self, tp):
        """
        Returns a new node given the parent and the type. The node isn't inserted in the
        tree, it is a temporary node instead, that has the values of the one that should
        be inserted as next with the given properties.

        Args:
            tp (str): the node type of the new node

        Returns:
            ComponentNode: the next node
        """

        currentNode = self.getCurrentNode()
        if currentNode:
            return self.model.getNewNode(currentNode, tp)

    def readFile(self, filename):
        """
        Reads a .csv file and turns it into a component tree data structure.

        Args:
            filename (str): the name or path of the file
        """

        if self.model:
            self.model.readFile(filename)