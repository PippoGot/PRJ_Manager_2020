# --- IMPORTS ---
# LIBRARIES
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import os

# MODELS
from models.ComboboxModel import ComboboxModel
from models.tree.Model import TreeModel
from models.archive.Model import ArchiveModel

# POPUPS
from ..newcomponent_editor.NewComponentEditor import NewComponentEditor
from ..hardware_selector.HardwareSelector import HardwareSelector

# PAGES
from ..components_page.ComponentsPage import ComponentsPage
from ..archive_page.ArchivePage import ArchivePage

# RESOURCES
from .. import resources
from . import decorators as decor

# UI
from .main_window import Ui_uiMainWindow as ui

# --- CLASS ---

class MainWindow(qtw.QMainWindow, ui):
    def __init__(self):
        """
        Loads the UI window and set the manufacture model.
        """

        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.filename = None
        self.copiedNode = None
        self.unsavedChanges = False
        self.archivePath = r'D:\Data\_PROGETTI\APPS\PRJ Manager 2.0\HardwareArchive.csv'

# COMBOBOX MODELS
        self.manufactureModel = ComboboxModel(r'D:\Data\_PROGETTI\APPS\PRJ Manager 2.0\uis\main_window\manufactures.csv')
        self.statusModel = ComboboxModel(r'D:\Data\_PROGETTI\APPS\PRJ Manager 2.0\uis\main_window\statuses.csv')

# COMPONENTS PAGE
        self.componentsPage = ComponentsPage()
        self.ComponentsPage.layout().addWidget(self.componentsPage)

        self.componentsPage.setManufactureModel(self.manufactureModel)
        self.componentsPage.setStatusModel(self.statusModel)

        self.componentsPage.uiView.customContextMenuRequested.connect(self._rightClickMenu)

# ARCHIVE PAGE
        self.archivePage = ArchivePage()
        self.ArchivePage.layout().addWidget(self.archivePage)

        self.archivePage.setManufactureModel(self.manufactureModel)
        self.archivePage.setStatusModel(self.statusModel)

# DATA MODELS
        self._setModel(TreeModel())
        self._setArchive(self.archivePath)

# FILE MENU
        self.uiActNew.triggered.connect(self.newFile)
        self.uiActOpen.triggered.connect(self.openFile)
        self.uiActSave.triggered.connect(self.saveFile)
        self.uiActSaveas.triggered.connect(self.saveFileAs)
        self.uiActExportBill.triggered.connect(self.exportBill)
        self.uiActClear.triggered.connect(self.clearFile)

        self.uiActArchive.triggered.connect(self.findArchive)

# EDIT MENU
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

# VIEW MENU
        self.uiActDeprecated.triggered.connect(self.hideDeprecated)

# --- FILE MENU FUNCTIONS ---

    @decor.askSave
    @decor.produceChanges
    def newFile(self, *args):
        """
        Creates a new model for a new file. When a new file is created the page
        index is set to the components page.
        """

        self._setModel(TreeModel())
        self.tabWidget.setCurrentIndex(0)

    @decor.askSave
    @decor.produceChanges
    def openFile(self, *args):
        """
        Opens a file given it's name or path.
        """

        filename, _ = qtw.QFileDialog.getOpenFileName(
            self,
            "Select a file to open...",
            qtc.QDir.homePath(),
            'CSV Documents (*.csv) ;; All Files (*)',
            'CSV Documents (*.csv)'
        )

        if filename:
            self._setModel()

            model = TreeModel(filename)
            self._setModel(model)
            self.filename = filename

            self.tabWidget.setCurrentIndex(0)

    @decor.ifHasModel
    def saveFile(self, *args):
        """
        Saves a file given it's name or path. Otherwise the filename is asked
        to the user.
        """

        if self.filename:
            self.componentsPage.saveFile(self.filename)
            self.unsavedChanges = False
        else:
            self.saveFileAs()

    @decor.ifHasModel
    def saveFileAs(self, *args):
        """
        Saves a file with a new name.
        """

        filename, _ = qtw.QFileDialog.getSaveFileName(
            self,
            "Select the file to save to...",
            qtc.QDir.homePath(),
            'CSV Documents (*.csv)'
        )

        if filename:
            self.componentsPage.saveFile(filename)
            self.filename = filename
            self.unsavedChanges = False

    def exportBill(self, *args):
        pass

    @decor.askSave
    @decor.produceChanges
    def clearFile(self, *args):
        """
        Clears the current model.
        """

        self._setModel()

    def findArchive(self, *args):
        """
        Opens the editor to look for an archive file to open and use.
        """

        filename, _ = qtw.QFileDialog.getOpenFileName(
            self,
            "Select a file to open...",
            qtc.QDir.homePath(),
            'CSV Documents (*.csv) ;; All Files (*)',
            'CSV Documents (*.csv)'
        )

        if filename:
            self.archivePath = filename
            self._setArchive(self.archivePath)

# --- EDIT MENU FUNCTIONS ---

    @decor.componentsAction
    @decor.ifNodeSelected
    @decor.ifNotLeaf
    def addAssemblyNode(self, *args):
        """
        Adds an assembly node.
        """

        newNode = self.componentsPage.getNewNode('Assembly')
        if newNode:
            self._addNode(newNode)

    @decor.componentsAction
    @decor.ifNodeSelected
    @decor.ifNotLeaf
    def addLeafNode(self, *args):
        """
        Adds a leaf node.
        """

        newNode = self.componentsPage.getNewNode('Leaf')
        if newNode:
            self._addNode(newNode)

    @decor.componentsAction
    @decor.ifNodeSelected
    @decor.ifNotLeaf
    def addSpecialNode(self, *args):
        """
        Adds a special node, either hardware or product.
        """

        self.newSelector = HardwareSelector()
        self.newSelector.setModel(self.archiveModel)
        self.newSelector.submit.connect(self.componentsPage.addNode)
        self.newSelector.submit.connect(self._produceChanges)

    @decor.componentsAction
    @decor.ifNodeSelected
    @decor.ifNotLeaf
    def addJigNode(self, *args):
        """
        Adds a jig node.
        """

        newNode = self.componentsPage.getNewNode('Jig')
        if newNode:
            self._addNode(newNode)

    @decor.componentsAction
    @decor.ifNodeSelected
    @decor.ifNotLeaf
    def addPlaceholderNode(self, *args):
        """
        Adds a placeholder node.
        """

        newNode = self.componentsPage.getNewNode('Placeholder')
        if newNode:
            self._addNode(newNode)

    @decor.componentsAction
    @decor.ifNodeSelected
    @decor.ifNotRoot
    @decor.produceChanges
    def removeComponent(self, *args):
        """
        Removes a component node that is not at level 1.

        Returns:
            ComponentNode: the removed node
        """

        return self.componentsPage.removeNode()

    @decor.componentsAction
    @decor.ifNodeSelected
    @decor.ifIsLeaf
    @decor.ifIsHardware
    def morphComponent(self, *args):
        """
        Swaps two archive components in the component tree model.
        """

        self.newSelector = HardwareSelector()
        self.newSelector.setModel(self.archiveModel)
        self.newSelector.submit.connect(self.componentsPage.swapNode)
        self.newSelector.submit.connect(self._produceChanges)

    @decor.componentsAction
    @decor.produceChanges
    def updateSpecialComponents(self, *args):
        pass

    def cut(self, *args):
        """
        Removes and stores a component for later pasting. Inherits the decorators from
        removeComponents.
        """

        self.copiedNode = self.removeComponent()

    @decor.componentsAction
    @decor.ifNodeSelected
    @decor.ifNotRoot
    def copy(self, *args):
        """
        Copies a node with it's children to paste it in other nodes.
        """

        currentNode = self.componentsPage.getCurrentNode()
        self.copiedNode = currentNode.deepCopy()

    @decor.componentsAction
    @decor.ifNodeSelected
    @decor.ifNotLeaf
    @decor.produceChanges
    def paste(self, *args):
        """
        Insert the copied or cut node in the currently selected node.
        """

        newNode = self.copiedNode.deepCopy()
        self.componentsPage.addNode(newNode)

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

        self.archiveModel = ArchiveModel(self.archivePath)
        self.archivePage.setModel(self.archiveModel)

    @decor.produceChanges
    def _produceChanges(self, *args):
        """
        Sets the unsaved changes variable to true. Used in functions that cannot
        use the corresponding decorator.
        """

        return

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
        self.newEditor.submit.connect(self._produceChanges)

# DIALOGS and MENUS

    def _okDialog(self, title, message):
        """
        Creates a dialog window with an OK button.

        Args:
            title (str): the title of the dialog.
            message (str): the message of the dialog.

        Returns:
            enum: the button pressed by the user
        """

        self.msgBox = qtw.QMessageBox.warning(
            self,
            title,
            message,
            qtw.QMessageBox.Ok,
            qtw.QMessageBox.Ok
        )

        return self.msgBox

    def _choiceDialog(self, title, message):
        """
        Creates a dialog window with a YES/NO choice.

        Args:
            title (str): the title of the dialog.
            message (str): the message of the dialog.

        Returns:
            enum: the button pressed by the user.
        """

        self.msgBox = qtw.QMessageBox.warning(
            self,
            title,
            message,
            qtw.QMessageBox.Yes | qtw.QMessageBox.No,
            qtw.QMessageBox.Yes
        )

        return self.msgBox

    def _cancelDialog(self, title, message):
        """
        Creates a dialog window with an YES/NO/CANCEL choice.

        Args:
            title (str): the title of the dialog.
            message (str): the message of the dialog.

        Returns:
            enum: the button pressed by the user.
        """

        self.msgBox = qtw.QMessageBox.warning(
            self,
            title,
            message,
            qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel,
            qtw.QMessageBox.Yes
        )

        return self.msgBox

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

            if self.uiActHash.isChecked():
                icon = qtg.QIcon(':id.png')

                value = node.parentHash
                dataType = type(value)
                string = f'Parent hash: {value}, type: {dataType}'
                parentHashAction = qtw.QAction()
                parentHashAction.setText(string)
                parentHashAction.setIcon(icon)
                menu.addAction(parentHashAction)

                value = node.selfHash
                dataType = type(value)
                string = f'Self hash: {value}, type: {dataType}'
                selfHashAction = qtw.QAction()
                selfHashAction.setText(string)
                selfHashAction.setIcon(icon)
                menu.addAction(selfHashAction)

            if self.uiActLevel.isChecked():
                icon = qtg.QIcon(':lv.png')

                dataType = type(level)
                string = f'Level: {level}, type: {dataType}'
                levelAction = qtw.QAction()
                levelAction.setText(string)
                levelAction.setIcon(icon)
                menu.addAction(levelAction)

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
            self._okDialog('Warning!', 'You are not in the proper page!')
            return True
        return False