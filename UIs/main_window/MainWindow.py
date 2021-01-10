# --- IMPORTS ---
# LIBRARIES
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import os

from data_types.UndoStack import UndoStack

# MODELS
from models.tree.Model import TreeModel
from models.archive.Model import ArchiveModel

# POPUPS
from ..popups.newcomponent_editor.NewComponentEditor import NewComponentEditor
from ..popups.hardware_selector.HardwareSelector import HardwareSelector
from ..popups.settings_window.SettingsWindow import SettingsWindow

# PAGES
from ..pages.components_page.ComponentsPage import ComponentsPage
from ..pages.archive_page.ArchivePage import ArchivePage

# RESOURCES
from .. import resources_rc
from . import decorators as decor
from . import dialogs
from ..stylesheet import stylesheet as qss

# UI
from .main_window import Ui_uiMainWindow as ui

# --- CLASS ---

class MainWindow(qtw.QMainWindow, ui):
    def __init__(self):
        """
        Loads the UI window and set the manufacture model.
        """

        # ui
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(qss)

        # class variables
        self.copiedNode = None

        # undo stack init
        self.unsavedChanges = False
        self.undoStack = UndoStack()

        # settings window init
        self.settingsWindow = SettingsWindow()
        self.settingsWindow.archivePathChanged.connect(self._setArchive)
        self.statusModel = self.settingsWindow.getStatusModel()
        self.manufactureModel = self.settingsWindow.getManufactureModel()

        # components page init
        self.componentsPage = ComponentsPage()
        self.ComponentsPage.layout().addWidget(self.componentsPage)

        self.componentsPage.setManufactureModel(self.manufactureModel)
        self.componentsPage.setStatusModel(self.statusModel)

        self.componentsPage.uiView.customContextMenuRequested.connect(self._rightClickMenu)

        # archive page init
        self.archivePage = ArchivePage()
        self.ArchivePage.layout().addWidget(self.archivePage)

        self.archivePage.setManufactureModel(self.manufactureModel)
        self.archivePage.setStatusModel(self.statusModel)

        # data models
        self.filename = None
        recentFiles = self.settingsWindow.getRecentFilesList()
        if recentFiles:
            self.filename = recentFiles[0]
        self._setModel(TreeModel(self.filename))
        self._setArchive(self.settingsWindow.archivePath)
        self.undoStack.addSnapshot(str(self.treeModel), 'init')

        # recent files
        self.recentFilesMenu = qtw.QMenu('Recent Files...')
        for file in recentFiles:
            name = file.split('/')[-1]
            action = qtw.QAction(name, self)
            self.recentFilesMenu.addAction(action)
            action.setData(file)
            action.triggered.connect(self._openRecent)
        self.menuFile.insertMenu(self.uiActClear, self.recentFilesMenu)

        # file menu actions connections
        self.uiActNew.triggered.connect(self.newFile)
        self.uiActOpen.triggered.connect(self.openFile)
        self.uiActSave.triggered.connect(self.saveFile)
        self.uiActSaveas.triggered.connect(self.saveFileAs)
        self.uiActExportBill.triggered.connect(self.exportBill)
        self.uiActClear.triggered.connect(self.clearFile)

        self.uiActSettings.triggered.connect(self.openSettings)

        # edit menu actions connections
        self.uiActAddAssembly.triggered.connect(self.addAssemblyNode)
        self.uiActAddPart.triggered.connect(self.addLeafNode)
        self.uiActAddSpecial.triggered.connect(self.addSpecialNode)
        self.uiActAddJig.triggered.connect(self.addJigNode)
        self.uiActAddPlaceholder.triggered.connect(self.addPlaceholderNode)

        self.uiActRemove.triggered.connect(self.removeComponent)
        self.uiActMorph.triggered.connect(self.morphComponent)
        self.uiActUpdate.triggered.connect(self.updateSpecialComponents)

        self.uiActCut.triggered.connect(self.cut)
        self.uiActCopy.triggered.connect(self.copy)
        self.uiActPaste.triggered.connect(self.paste)
        self.uiActUndo.triggered.connect(self.undo)
        self.uiActRedo.triggered.connect(self.redo)

        # view menu actions connections
        self.uiActDeprecated.triggered.connect(self.hideDeprecated)
        self.uiActExpandAll.triggered.connect(self.expandAll)
        self.uiActExpandOne.triggered.connect(self.expandOne)
        self.uiActCollapseOne.triggered.connect(self.collapseOne)

# --- FILE MENU FUNCTIONS ---

    @decor.askSave
    def newFile(self, *args):
        """
        Creates a new model for a new file. When a new file is created the page
        index is set to the components page.
        """

        self._setModel(TreeModel())
        self.filename = None
        self.tabWidget.setCurrentIndex(0)

    @decor.askSave
    def openFile(self, filename = None, *args):
        """
        Opens a file given it's name or path.
        """

        if not filename:
            filename = dialogs.openDialog()

        if filename:
            self._setModel()

            model = TreeModel(filename)
            self._setModel(model)
            self.filename = filename
            self.settingsWindow.addRecentFile(self.filename)

            self.tabWidget.setCurrentIndex(0)

    @decor.ifHasModel
    def saveFile(self, *args):
        """
        Saves a file given it's name or path. Otherwise the filename is asked
        to the user.
        """

        if self.filename:
            self.treeModel.saveFile(self.filename)
            self.unsavedChanges = False
        else:
            self.saveFileAs()

    @decor.ifHasModel
    def saveFileAs(self, *args):
        """
        Saves a file with a new name.
        """

        filename = dialogs.saveDialog()

        if filename:
            self.treeModel.saveFile(filename)
            self.filename = filename
            self.settingsWindow.addRecentFile(self.filename)
            self.unsavedChanges = False

    def exportBill(self, *args):
        pass

    @decor.askSave
    def clearFile(self, *args):
        """
        Clears the current model.
        """

        self._setModel()

    def openSettings(self):
        """
        Opens the settings window.
        """

        self.settingsWindow.show()

# --- EDIT MENU FUNCTIONS ---

    @decor.ifNotLeaf
    def addAssemblyNode(self, *args):
        """
        Adds an assembly node.
        """

        newNode = self.componentsPage.getNewNode('AssemblyNode')
        if newNode:
            self._addNode(newNode)

    @decor.ifNotLeaf
    def addLeafNode(self, *args):
        """
        Adds a leaf node.
        """

        newNode = self.componentsPage.getNewNode('LeafNode')
        if newNode:
            self._addNode(newNode)

    @decor.ifNotLeaf
    def addSpecialNode(self, *args):
        """
        Adds a special node, either hardware or product.
        """

        self.newSelector = HardwareSelector()
        self.newSelector.setModel(self.archiveModel)
        self.newSelector.submit.connect(self.componentsPage.addNode)
        self.newSelector.submit.connect(self._undoable)
        self.newSelector.submit.connect(self._producesChanges)

    @decor.ifNotLeaf
    def addJigNode(self, *args):
        """
        Adds a jig node.
        """

        newNode = self.componentsPage.getNewNode('JigNode')
        if newNode:
            self._addNode(newNode)

    @decor.ifNotLeaf
    def addPlaceholderNode(self, *args):
        """
        Adds a placeholder node.
        """

        newNode = self.componentsPage.getNewNode('PlaceholderNode')
        if newNode:
            self._addNode(newNode)

    @decor.ifNotRoot
    @decor.undoableAction
    def removeComponent(self, *args):
        """
        Removes a component node that is not at level 1.

        Returns:
            ComponentNode: the removed node
        """

        return self.componentsPage.removeNode()

    @decor.ifLeaf
    @decor.ifIsHardware
    @decor.undoableAction
    def morphComponent(self, *args):
        """
        Swaps two archive components in the component tree model.
        """

        self.newSelector = HardwareSelector()
        self.newSelector.setModel(self.archiveModel)
        self.newSelector.submit.connect(self.componentsPage.swapNode)
        self.newSelector.submit.connect(self._producesChanges)

    @decor.componentsAction
    @decor.ifHasModel
    @decor.undoableAction
    def updateSpecialComponents(self, *args):
        """
        Updates all of the components in the tree model with data of the archive model.
        """

        archiveComponents = self.archiveModel.rootItem.getChildren()
        treeComponents = self.treeModel.tree.searchNodes(type = 'Hardware')
        treeComponents.extend(self.treeModel.tree.searchNodes(type = 'Product'))

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

        for treeNode in treeComponents:
            for archiveNode in archiveComponents:
                if treeNode == archiveNode:
                    features = archiveNode.getNodeDictionary(*COLUMNS_TO_UPDATE)
                    for key, value in features.items():
                        treeNode.addFeature(key, value)
        self.componentsPage._resizeView()

    def cut(self, *args):
        """
        Removes and stores a component for later pasting. Inherits the decorators from
        removeComponents.
        """

        self.copiedNode = self.removeComponent()

    @decor.ifNotRoot
    def copy(self, *args):
        """
        Copies a node with it's children to paste it in other nodes.
        """

        currentNode = self.componentsPage.getCurrentNode()
        self.copiedNode = currentNode.deepCopy()

    @decor.ifNotLeaf
    @decor.undoableAction
    def paste(self, *args):
        """
        Insert the copied or cut node in the currently selected node.
        """

        newNode = self.copiedNode.deepCopy()
        self.componentsPage.addNode(newNode)

    @decor.producesChanges
    def undo(self, *args):
        """
        Undo the current action.
        """

        string = self.undoStack.undo()
        model = TreeModel()
        model.readString(string)
        self._setModel(model)

    @decor.producesChanges
    def redo(self, *args):
        """
        Redo the currently undone action.
        """

        string = self.undoStack.redo()
        model = TreeModel()
        model.readString(string)
        self._setModel(model)

# --- VIEW MENU FUNCTIONS ---

    @decor.ifHasModel
    def hideDeprecated(self, *args):
        """
        Hides or shows the deprecated nodes in the tree view.
        """

        if self.uiActDeprecated.isChecked():
            self.componentsPage.hideDeprecated(True)
        else:
            self.componentsPage.hideDeprecated(False)

    @decor.ifHasModel
    def expandAll(self, *args):
        """
        Expands all of the items in the view.
        """

        self.componentsPage.expandAll()

    @decor.ifHasModel
    def expandOne(self, *args):
        """
        Expands the current lowest level of items in the tree.
        """

        self.componentsPage.expandOne()

    @decor.ifHasModel
    def collapseOne(self, *args):
        """
        Collapses the lowest level currently expanded in the tree.
        """

        self.componentsPage.collapseOne()

# --- PRIVATE UTILITY FUNCTIONS ---

    def _setModel(self, model = None):
        """
        Sets the models if one is given, then updates the models of the other widgets.

        Args:
            model (ModelTree): the new model
        """

        self.treeModel = model
        self.componentsPage.setModel(self.treeModel)

        if self.treeModel:
            self.treeModel.dataChanged.connect(self.hideDeprecated)

    def _setArchive(self, archivePath = None):
        """
        Sets the archive model.

        Args:
            archivePath (str): the name or path of the archive file. Defaults to None.
        """

        self.archivePath = archivePath
        self.archiveModel = ArchiveModel(self.archivePath)
        self.archivePage.setModel(self.archiveModel, self.archivePath)

    @decor.producesChanges
    def _producesChanges(self, *args):
        """
        Sets the unsaved changes variable to true. Used in functions that cannot
        use the corresponding decorator.
        """

        pass

    @decor.undoable
    def _undoable(self, *args):
        """
        Saves a snapshot of the current file. Used in functions that cannot
        use the corresponding decorator.
        """

        pass

# NODES HANDLING

    def _addNode(self, node):
        """
        Pops up an editor window with an initialised node to edit. If "Add" is
        pressed the node is added to the tree, while if "Cancel" is pressed
        the node will not be added to the tree.

        Args:
            node (ComponentNode): the node to edit
        """

        self.newEditor = NewComponentEditor(node)
        self.newEditor.setManufactureModel(self.manufactureModel)
        self.newEditor.setStatusModel(self.statusModel)
        self.newEditor.submit.connect(self.componentsPage.addNode)
        self.newEditor.submit.connect(self._undoable)
        self.newEditor.submit.connect(self._producesChanges)

# DIALOGS and MENUS

    def _rightClickMenu(self, position):
        """
        Creates the context menu in the components view when the right click is pressed.

        Args:
            position (?): the position of the cursor on the screen.
        """

        index = self.componentsPage.getCurrentIndex()

        separator = qtw.QAction()
        separator.setSeparator(True)
        menu = qtw.QMenu()

        if index:
            node = index.internalPointer()
            level = node.getLevel()

            if level < 5:
                menu.addAction(self.uiActAddAssembly)
                menu.addAction(self.uiActAddSpecial)
                menu.addAction(self.uiActAddPart)
                menu.addAction(self.uiActAddJig)
                menu.addAction(self.uiActAddPlaceholder)
                menu.addAction(separator)

            if node.getFeature('type') == 'Hardware':
                menu.addAction(self.uiActMorph)
                menu.addAction(separator)

            if level > 1:
                menu.addAction(self.uiActRemove)

            menu.exec_(self.componentsPage.uiView.viewport().mapToGlobal(position))

    def _checkPage(self, page):
        """
        Checks if the user is in the correct page and notify with a dialog if it's not.

        Args:
            page (int): the page to check for.

        Returns:
            bool: whether the user is in the correct page or not.
        """

        if self.tabWidget.currentIndex() != page:
            dialogs.pageError()
            return True
        return False

    def _openRecent(self):
        action = self.sender()
        if action:
            self.openFile(action.data())
