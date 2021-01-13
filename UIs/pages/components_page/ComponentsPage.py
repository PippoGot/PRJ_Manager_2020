from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from models.tree.Model import TreeModel
from models.tree.Proxy import TreeProxy
from ...main_window.dialogs import saveDialog

from ...widgets.component_editor.ComponentEditor import ComponentEditor
from ...popups.newcomponent_editor.NewComponentEditor import NewComponentEditor

from .components_page import  Ui_uiComponentsPage as ui

class ComponentsPage(qtw.QWidget, ui):
    """
    Main tree page, displays the current working component tree and provides a
    component editor to edit the inserted nodes. Offers a toolkit of functions to
    add remove and swap nodes in the tree model.
    Uses the ComponentEditor widget.
    """

    fileSaved = qtc.pyqtSignal(str)
    nodeAdded = qtc.pyqtSignal(object)

    def __init__(self):
        """
        Loads the UI window and initialise the class variables.
        """

        super(ComponentsPage, self).__init__()
        self.setupUi(self)

        self.model = None
        self.filename = None
        self.manufactureModel = None
        self.statusModel = None
        self.copiedNode = None
        self.proxy = TreeProxy()
        self.uiEditor = ComponentEditor()
        self.horizontalLayout.addWidget(self.uiEditor)
        self.expandLvl = 0

# --- MODELS ---

    def setModel(self, model):
        """
        Sets the editor's and view's model, then refreshes the view.

        Args:
            model (ModelTree): the model of the view and editor widget
        """

        self.model = model
        self.proxy.setSourceModel(self.model)
        self.uiView.setModel(self.proxy)
        self.uiEditor.setModel(self.model)

        self.proxy.sort(0, qtc.Qt.AscendingOrder)

        if self.model:
            self.selection = self.uiView.selectionModel()
            self.selection.currentChanged.connect(self._mapIndex)
            self.model.dataChanged.connect(self.hideDeprecated)
            self.expandAll()

        self._resizeView()

    def setManufactureModel(self, manufactureModel):
        """
        Sets the editor's manufacture combobox model.

        Args:
            manufactureModel (ModelCombobox): the model of the combobox
        """

        self.manufactureModel = manufactureModel
        self.uiEditor.setManufactureModel(manufactureModel)

    def setStatusModel(self, statusModel):
        """
        Sets the editor's status combobox model.

        Args:
            statusModel (ModelCombobox): the model of the combobox
        """

        self.statusModel = statusModel
        self.uiEditor.setStatusModel(statusModel)

# --- SELECTION ---

    def _mapIndex(self, index):
        """
        The index is set as the current index of the editor.

        Args:
            index (QModelIndex): the index to update
        """

        index = self.proxy.mapToSource(index)
        self.uiEditor.setCurrentSelection(index)

# --- GETTERS ---

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

        currentIndex = self.selection.currentIndex()
        currentIndex = self.proxy.mapToSource(currentIndex)
        return currentIndex

    def getNewNode(self, classname):
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
            level = currentNode.getLevel()
            if level < 4:
                return self.model.getNewNode(currentNode, classname)

            return self.model.getNewNode(currentNode, 'LeafNode')

    def getModel(self):
        """
        Returns the current model.

        Returns:
            TreeModel: the model
        """

        return self.model

# --- UTILITY ---

    def _resizeView(self):
        """
        Updates the view resizing the columns to a specified value and expanding the tree.
        """

        if self.model:
            for column in range(self.model.columnCount(qtc.QModelIndex())):
                self.uiView.resizeColumnToContents(column)

    def readJsonString(self, string):
        """
        Reads a json formatted string and extracts the model out of it.

        Args:
            string (str): the string in json format
        """

        model = TreeModel()
        model.readString(string)
        self.setModel(model)

# --- MAIN WINDOW FUNCTIONS ---

# FILE MENU

    def resetModel(self):
        """
        Sets the current model to an empty one and the filename to None.
        """

        self.readModel()

    def readModel(self, filename = None):
        """
        Reads a file if given, and converts it to a model if possible. Then the model is
        set as current model.

        Args:
            filename (str): the filename of the file to read. Defaults to None.
        """

        self.filename = filename
        self.setModel(TreeModel(filename))

    def saveModel(self):
        """
        Saves the current model with the current filename. If there's not a filename
        the save as function is called.

        Returns:
            bool: if the file is saved or not
        """

        if self.filename:
            self.model.saveFile(self.filename)
            self.fileSaved.emit(self.filename)
            return True
        else:
            return self.saveModelAs()
        return False

    def saveModelAs(self):
        """
        Saves the current model with the chosen filename.

        Returns:
            bool: if the file is saved or not
        """

        filename = saveDialog()
        if filename:
            self.filename = filename
            self.model.saveFile(self.filename)
            self.fileSaved.emit(self.filename)
            return True
        return False

    def clearModel(self):
        """
        Clears the model and sets the filename to None.
        """

        self.filename = None
        self.setModel(None)

# EDIT MENU

    def prepareNode(self, tp):
        """
        Opens the editor with the new selected node type ready for editing. If the node
        is submitted then the node is added to the tree.

        Args:
            tp (str): the type of node to prepare
        """

        newNode = self.getNewNode(tp)
        if newNode:
            self.newEditor = NewComponentEditor(newNode)
            self.newEditor.setManufactureModel(self.manufactureModel)
            self.newEditor.setStatusModel(self.statusModel)
            self.newEditor.submit.connect(self.addNode)

    def addNode(self, newNode):
        """
        Adds a generic component node to the tree in the selected location.

        Args:
            newNode (ComponentNode): the new node to add
        """

        currentIndex = self.getCurrentIndex()
        parentItem = currentIndex.internalPointer()

        self.model.insertRows(len(parentItem), newNode, currentIndex)
        currentIndex = self.proxy.mapFromSource(self.getCurrentIndex().siblingAtColumn(0))
        self.uiView.expandRecursively(currentIndex, 0)

        self._resizeView()
        self.nodeAdded.emit(newNode)

    def removeNode(self):
        """
        Removes a component node.

        Returns:
            ComponentNode: the removed node
        """

        currentNode = self.getCurrentNode()
        currentIndex = self.getCurrentIndex()

        removedNode = self.model.removeRows(currentNode.getIndex(), currentIndex.parent())

        self._resizeView()

        return removedNode

    def swapNode(self, node):
        """
        Removes the selected component and then adds a new component in it's place.

        Args:
            node (ComponentNode): the new component to add
        """

        index = self.getCurrentIndex()
        position = index.row()
        parent = index.parent()

        self.model.swapComponent(position, node, parent)

        self._resizeView()
        self.nodeAdded.emit(node)

    def updateSpecialNodes(self, archiveNodes):
        """
        Updates the fields of all the hardware archive nodes inside the tree.

        Args:
            archiveNodes (list[ComponentNode]): the list of archive nodes
        """

        COLUMNS_TO_UPDATE = [
            'name',
            'description',
            'type',
            'manufacture',
            'status',
            'price',
            'package',
            'seller',
            'link'
        ]

        hardwareNodes = self.model.tree.getHardwareNodes()

        for hNode in hardwareNodes:
            for aNode in archiveNodes:
                if hNode == aNode:
                    features = aNode.getFeatures(*COLUMNS_TO_UPDATE)
                    hNode.addFeatures(**features)

        self._resizeView()

    def cutNode(self):
        """
        Removes and stores the currently selected node.
        """

        self.copiedNode = self.removeNode()

    def copyNode(self):
        """
        Copies and stores the currently selected node.
        """

        currentNode = self.getCurrentNode()
        self.copiedNode = currentNode.deepCopy()

    def pasteNode(self):
        """
        Generates a copy of the currently stored node and adds it to the model in the
        currently selected node.
        """

        if self.copiedNode:
            newNode = self.copiedNode.deepCopy()
            self.addNode(newNode)

# VIEW MENU

    def hideDeprecated(self, hide):
        """
        Changes the proxy filter regular expression based on this function's
        input variable.

        Args:
            hide (bool): whether to show or hide the deprecated nodes
        """

        if hide:
            self.proxy.setFilterRegExp('Deprecated')
        else:
            self.proxy.setFilterRegExp(None)

        self._resizeView()

    def expandAll(self):
        """
        Expands all of the items in the view.
        """

        self.uiView.expandAll()
        self.expandLvl = self.model.tree.getHeight() - 1

        self._resizeView()

    def expandOne(self):
        """
        Expands the current lowest level of items in the tree.
        """

        if self.expandLvl >= self.model.tree.getHeight() - 1: return

        rootIndex = self.model.createIndex(0, 0, self.model.first)
        rootIndex = self.proxy.mapFromSource(rootIndex)

        self.uiView.expandRecursively(rootIndex, self.expandLvl + 1)
        self.expandLvl += 1

        self._resizeView()

    def collapseOne(self):
        """
        Collapses the lowest level currently expanded in the tree.
        """

        if self.expandLvl < 1: return

        self.uiView.collapseAll()
        rootIndex = self.model.createIndex(0, 0, self.model.first)
        rootIndex = self.proxy.mapFromSource(rootIndex)

        self.uiView.expandRecursively(rootIndex, self.expandLvl - 1)
        self.expandLvl -= 1

        self._resizeView()
