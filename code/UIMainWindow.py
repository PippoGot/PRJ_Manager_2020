from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import os

from UIComponentsPage import ComponentsPage
from UIBillPage import BillPage
from UIHardwareEditor import HardwareEditor
from UIComponentEditor import ComponentEditor
from UIHardwareSelector import HardwareSelector

from ModelHardware import ModelHardware
from ModelTree import ModelTree
from ModelCombobox import ModelCombobox

from CompositeNodes import AssemblyNode, LeafNode, JigNode, PlaceholderNode

from constants import COLUMNS_TO_UPDATE
from stylesheet import stylesheet as qss
# import resources

from ui_main_window import Ui_uiMainWindow as ui

class MainWindow(qtw.QMainWindow, ui):
    """
    Class for the main window UI and the actions functions. This class manage every action that can
    be performed in the application.
    """

    def __init__(self):
        """
        Loads the UI window, creates the models for the archive and the comboboxes,
        then connects the menu actions to the respective functions.
        """

        super(MainWindow, self).__init__()
        self.setupUi(self)

# MODEL INIT

        self.filename = None
        self.model = None
        self.copied = None
        self.archive = ModelHardware()
        statusPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'statuses.csv')
        self.statuses = ModelCombobox(statusPath)
        manufacturesPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'manufactures.csv')
        self.manufactures = ModelCombobox(manufacturesPath)

# COMPONENT PAGE

        self.treeEditor = ComponentsPage(self.manufactures)
        self.uiTreePage.layout().addWidget(self.treeEditor)
        self.treeEditor.uiStatus.setModel(self.statuses)
        self.treeEditor.uiComponentsView.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.treeEditor.uiComponentsView.customContextMenuRequested.connect(self.rightClickMenu)

# HARDWARE EDITOR PAGE

        self.hardwareEditor = HardwareEditor(self.archive)
        self.hardwareEditor.uiCurrentStatus.setModel(self.statuses)
        self.hardwareEditor.uiNewStatus.setModel(self.statuses)
        self.uiHardwarePage.layout().addWidget(self.hardwareEditor)

# BILL PAGE

        self.billPage = BillPage()
        self.uiBillPage.layout().addWidget(self.billPage)
        self.uiTabWidget.currentChanged.connect(self.refreshBillModel)

# FILE MENU ACTIONS

        self.uiActionNew.triggered.connect(self.newFile)
        self.uiActionOpen.triggered.connect(self.openFile)
        self.uiActionSave.triggered.connect(self.saveFile)
        self.uiActionSaveAs.triggered.connect(self.saveAsFile)
        self.uiActionClear.triggered.connect(self.clearFile)
        self.uiActionExportBOM.triggered.connect(self.exportBOM)

# EDIT MENU ACTIONS

        self.uiActionAddComponent.triggered.connect(self.addComponent)
        self.uiActionAddSpecialComponent.triggered.connect(self.addSpecialComponent)
        self.uiActionAddLeafComponent.triggered.connect(self.addLeafComponent)
        self.uiActionAddJig.triggered.connect(self.addJig)
        self.uiActionAddPlaceholder.triggered.connect(self.addPlaceholder)

        self.uiActionMorphSpecialComponent.triggered.connect(self.morphSpecialComponent)
        self.uiActionUpdateSpecialComponents.triggered.connect(self.updateSpecialComponents)
        self.uiActionRemoveComponent.triggered.connect(self.removeComponent)

        self.uiActionCut.triggered.connect(self.cut)
        self.uiActionCopy.triggered.connect(self.copy)
        self.uiActionPaste.triggered.connect(self.paste)
        # self.uiActionUndo.triggered.connect(self.undo)
        # self.uiActionRedo.triggered.connect(self.redo)

# VIEW MENU ACTIONS

        self.uiActionHideDeprecated.triggered.connect(self.hideDeprecated)
        self.uiActionExpandAll.triggered.connect(self.treeEditor.uiComponentsView.expandAll)
        self.uiActionCollapseAll.triggered.connect(self.treeEditor.uiComponentsView.collapseAll)

# --- ACTION FUNCTIONS ---

# FILE MENU

    def newFile(self):
        """Creates a new model, for a new file. If a model is present asks to be save changes."""

        if not self.filename and self.model:
            dialog = self.cancelDialog('File not saved...', 'Save changes to current file?')

            if dialog == qtw.QMessageBox.Yes:
                self.saveFile()
            elif dialog == qtw.QMessageBox.Cancel:
                return

        self.setModel(ModelTree())
        self.uiTabWidget.setCurrentIndex(0)

    def openFile(self):
        """
        Opens and read a .csv file, then displays the corresponding model.
        If a model is present asks to save changes.
        """

        if not self.filename and self.model:
            dialog = self.choiceDialog('File not saved...', 'Save changes to current file?')

            if dialog == qtw.QMessageBox.Yes:
                self.saveFile()

        filename, _ = qtw.QFileDialog.getOpenFileName(
            self,
            "Select a file to open...",
            qtc.QDir.homePath(),
            'CSV Documents (*.csv) ;; All Files (*)',
            'CSV Documents (*.csv)'
        )

        if filename:
            try:
                self.setModel(ModelTree(filename), filename)
                self.uiTabWidget.setCurrentIndex(0)

            except Exception as e:
                self.okDialog('Critical Error!', f'Could not open the file at {filename}\nbecause " {e} " exception occurred!')

    def saveFile(self):
        """Saves the current file with the current filename or calls Save as function."""

        if self.model:
            if self.filename:
                self.model.saveFile(self.filename)
            else:
                self.saveAsFile()

        else:
            self.okDialog('Warning!', 'No file currently open.')

    def saveAsFile(self):
        """Saves the file with a different filename from the original, or a new file."""

        if self.model:
            filename, _ = qtw.QFileDialog.getSaveFileName(
                self,
                "Select the file to save to...",
                qtc.QDir.homePath(),
                'CSV Documents (*.csv)'
            )

            if filename:
                try:
                    self.model.saveFile(filename)

                except Exception as e:
                    self.okDialog('Critical Error!', f'Could not save the file at {filename}\nbecause " {e} " exception occurred!')

                self.filename = filename

        else:
            self.okDialog('Warning!', 'No file currently open.')

    def exportBOM(self):
        """Exports the bill of material of the current project."""

        if self.model:
            filename, _ = qtw.QFileDialog.getSaveFileName(
                self,
                "Select the file to save to...",
                qtc.QDir.homePath(),
                'CSV Documents (*.csv)'
            )

            if filename:
                try:
                    self.billPage.exportBOM(filename)

                except Exception as e:
                    self.okDialog('Critical Error!', f'Could not save the file at {filename}\nbecause " {e} " exception occurred!')

        else:
            self.okDialog('Warning!', 'No file currently open.')

    def clearFile(self):
        """Resets the current open file, as well as the components view."""

        if self.model:
            dialog = self.cancelDialog('File not saved...', 'Save changes to current file?')

            if dialog == qtw.QMessageBox.Yes:
                self.saveFile()
            elif dialog == qtw.QMessageBox.Cancel:
                return

        self.setModel()

# EDIT MENU

    def addComponent(self):
        """Adds a custom assembly/part component to the model."""

        if self.checkPage(0):
            return

        currentSelection = self.treeEditor.current

        if currentSelection:
            parentItem = currentSelection.internalPointer()
            level = parentItem.getLevel()
            newNumber = parentItem.getNewNumber(parentItem.getPrefix(), level + 1)

            if level < 5:
                new = AssemblyNode(number=newNumber, level=level + 1)

                self.newComponentEditor = ComponentEditor(self.manufactures, new)
                self.newComponentEditor.uiStatus.setModel(self.statuses)
                self.newComponentEditor.submit.connect(self.insertNode)
                self.newComponentEditor.show()

            else:
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else:
            self.okDialog('Warning!', 'No item currently selected.')

    def addSpecialComponent(self):
        """Adds a hardware/consumable component from the hardware archive."""

        if self.checkPage(0):
            return

        currentSelection = self.treeEditor.current

        if currentSelection:
            parentItem = currentSelection.internalPointer()
            level = parentItem.getLevel()

            if level < 5:
                self.hardwareSelector = HardwareSelector(self.archive)
                self.hardwareSelector.submit.connect(self.insertNode)
                self.hardwareSelector.show()

            else:
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else:
            self.okDialog('Warning!', 'No item currently selected.')

    def addLeafComponent(self):
        """Adds a level 5 part to the tree."""

        if self.checkPage(0):
            return

        currentSelection = self.treeEditor.current

        if currentSelection:
            parentItem = currentSelection.internalPointer()
            level = parentItem.getLevel()
            newNumber = parentItem.getNewNumber(parentItem.getPrefix(), 5)

            if level < 5:
                new = LeafNode(number=newNumber)

                self.newComponentEditor = ComponentEditor(self.manufactures, new)
                self.newComponentEditor.uiStatus.setModel(self.statuses)
                self.newComponentEditor.submit.connect(self.insertNode)
                self.newComponentEditor.show()

            else:
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else:
            self.okDialog('Warning!', 'No item currently selected.')

    def addJig(self):
        """Adds a jig component to the tree."""

        if self.checkPage(0):
            return

        currentSelection = self.treeEditor.current

        if currentSelection:
            parentItem = currentSelection.internalPointer()
            level = parentItem.getLevel()
            newNumber = parentItem.getNewNumber('JIG', 5)

            if level < 5:
                new = JigNode(number=newNumber, level=level + 1)

                self.newComponentEditor = ComponentEditor(self.manufactures, new)
                self.newComponentEditor.uiStatus.setModel(self.statuses)
                self.newComponentEditor.submit.connect(self.wrapper)
                self.newComponentEditor.show()

            else:
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else:
            self.okDialog('Warning!', 'No item currently selected.')

    def addPlaceholder(self):
        """Adds a placeholder component to the tree."""

        if self.checkPage(0):
            return

        currentSelection = self.treeEditor.current

        if currentSelection:
            parentItem = currentSelection.internalPointer()
            level = parentItem.getLevel()
            newNumber = parentItem.getNewNumber('PLC', 5)

            if level < 5:
                new = PlaceholderNode(number = newNumber, level = level + 1)

                self.newComponentEditor = ComponentEditor(self.manufactures, new)
                self.newComponentEditor.uiStatus.setModel(self.statuses)
                self.newComponentEditor.submit.connect(self.insertNode)
                self.newComponentEditor.show()

            else:
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else:
            self.okDialog('Warning!', 'No item currently selected.')

    def morphSpecialComponent(self):
        """Changes a selected hardware component with another hardware component of choice."""

        if self.checkPage(0):
            return

        currentSelection = self.treeEditor.current

        if currentSelection:
            item = currentSelection.internalPointer()
            level = item.getLevel()
            tp = item.getFeature('type')

            if level == 5:
                if tp in ['Hardware', 'Consumable']:
                    self.hardwareSelector = HardwareSelector(self.archive)
                    self.hardwareSelector.submit.connect(self.swapNode)
                    self.hardwareSelector.show()
                else:
                    self.okDialog('Warning!', 'The item is not of an appropriate type!')
            else:
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')
        else:
            self.okDialog('Warning!', 'No item currently selected.')

    def updateSpecialComponents(self):
        """
        Iterates over the hardware/consumables components and over the archive items.
        Then updates every present item in the list with the data in the archive.
        """

        if self.checkPage(0):
            return

        archiveRoot = self.archive.rootItem
        modelRoot = self.model.rootItem

        if self.model:
            for node in modelRoot.getNodesList(type = 'Hardware'):
                for hardwareNode in archiveRoot.getNodesList(type = 'Hardware'):
                    if node == hardwareNode:
                        features = hardwareNode.getNodeDictionary(*COLUMNS_TO_UPDATE)
                        for key, value in features.items():
                            node.updateFeature(key, value)

            for node in modelRoot.getNodesList(type = 'Consumable'):
                for hardwareNode in archiveRoot.getNodesList(type = 'Consumable'):
                    if node == hardwareNode:
                        features = hardwareNode.getNodeDictionary(*COLUMNS_TO_UPDATE)
                        for key, value in features.items():
                            node.updateFeature(key, value)

    def removeComponent(self):
        """Removes a component from the model."""

        if self.checkPage(0):
            return

        currentSelection = self.treeEditor.current

        if currentSelection:
            item = currentSelection.internalPointer()
            row = item.getIndex()
            parent = currentSelection.parent()

            if item.getLevel() != 1:
                self.model.removeRows(row, parent)
            else:
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else:
            self.okDialog('Warning!', 'No item currently selected.')

    def cut(self):
        """Removes and stores a component for later pasting."""

        if self.checkPage(0):
            return

        currentSelection = self.treeEditor.current

        if currentSelection:
            item = currentSelection.internalPointer()
            row = item.getIndex()
            parent = currentSelection.parent()

            if item.getLevel() != 1:
                self.copied = self.model.removeRows(row, parent)
            else:
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else:
            self.okDialog('Warning!', 'No item currently selected.')

    def copy(self):
        """Creates and stores a deep copy of a component to paste it in another component."""

        if self.checkPage(0):
            return

        currentSelection = self.treeEditor.current

        if currentSelection:
            item = currentSelection.internalPointer()

            if item.getLevel() != 1:
                self.copied = item.deepCopy()
            else:
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else:
            self.okDialog('Warning!', 'No item currently selected.')

    def paste(self):
        """Adds the cut or copied component to this components' children."""

        if self.checkPage(0):
            return

        currentSelection = self.treeEditor.current

        if currentSelection:
            parentItem = currentSelection.internalPointer()

            if parentItem.level < 5:
                self.model.insertRows(len(parentItem.getChildren()), self.copied, currentSelection)
                self.copied = self.copied.deepCopy()
                self.treeEditor.refreshView()

            else:
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else:
            self.okDialog('Warning!', 'No item currently selected.')

# VIEW MENU

    def hideDeprecated(self):
        """Choose whether to see or not deprecated components."""

        if self.model:
            if self.uiActionHideDeprecated.isChecked():
                self.treeEditor.treeProxyModel.setFilterRegExp('Deprecated')
            else:
                self.treeEditor.treeProxyModel.setFilterRegExp(None)
            self.treeEditor.refreshView()

# --- OTHER FUNCTIONS ---

# NODE UTILITY

    def insertNode(self, new):
        """
        Inserts the node in the model at the right position, then updates the hashes
        and refreshes the view.

        Args:
            new (BaseNode): the node to insert in the model.
        """

        currentSelection = self.treeEditor.current
        parentItem = currentSelection.internalPointer()

        self.model.insertRows(len(parentItem.getChildren()), new, currentSelection)
        new.updateHashes(self.model.rootItem)
        self.treeEditor.refreshView()

    def swapNode(self, node):
        """
        Swap a node with another node to update it, then updates the hashes and refreshes
        the view.

        Args:
            node (BaseNode): the node to insert at the current location to replace the present one.
        """

        currentSelection = self.treeEditor.current

        self.model.swapComponent(currentSelection.row(), node, currentSelection.parent())
        node.updateHashes(self.model.rootItem)
        self.treeEditor.refreshView()

# MODEL FUNCTIONS

    def setModel(self, model = None, filename = None):
        """
        Sets the window model for all the different pages. Also if the model is from an external file
        the filename is updated.

        Args:
            model (QAbstractItemModel): the model to set. Default is None.
            filename (str): the name or path of the file. Default is None.
        """

        self.model = model
        self.filename = filename
        self.treeEditor.setModel(self.model)
        self.refreshBillModel(1)

    def refreshBillModel(self, index):
        """
        Refreshes the bill model to update it.

        Args:
            index (int): the current index of the tab widget.
        """

        if index == 1:
            if self.model:
                nodesList = self.model.getBillNodes()
                self.billPage.setModel(nodesList)
            else:
                self.billPage.setModel()

# DIALOGS and MENUS

    def okDialog(self, title, message):
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

    def choiceDialog(self, title, message):
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

    def cancelDialog(self, title, message):
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

    def rightClickMenu(self, position):
        """
        Creates the context menu in the components view when the right click is pressed.

        Args:
            position (?): the position of the cursor on the screen.
        """

        index = self.treeEditor.current

        separator = qtw.QAction()
        separator.setSeparator(True)

        if index:
            node = index.internalPointer()
            level = node.getLevel()

            menu = qtw.QMenu()

            if self.uiActionShowHashes.isChecked():
                icon = qtg.QIcon('code/resources/icons/id.png')

                value = node.getFeature('parentHash')
                dataType = type(value)
                string = f'Parent hash: {value}, type: {dataType}'
                parentHashAction = qtw.QAction()
                parentHashAction.setText(string)
                parentHashAction.setIcon(icon)
                menu.addAction(parentHashAction)

                value = node.getFeature('selfHash')
                dataType = type(value)
                string = f'Self hash: {value}, type: {dataType}'
                selfHashAction = qtw.QAction()
                selfHashAction.setText(string)
                selfHashAction.setIcon(icon)
                menu.addAction(selfHashAction)

            if self.uiActionShowLevel.isChecked():
                icon = qtg.QIcon('code/resources/icons/lv.png')

                value = node.getFeature('level')
                dataType = type(value)
                string = f'Level: {value}, type: {dataType}'
                levelAction = qtw.QAction()
                levelAction.setText(string)
                levelAction.setIcon(icon)
                menu.addAction(levelAction)

            if level < 5:
                menu.addAction(self.uiActionAddComponent)
                menu.addAction(self.uiActionAddSpecialComponent)
                menu.addAction(self.uiActionAddLeafComponent)
                menu.addAction(self.uiActionAddJig)
                menu.addAction(self.uiActionAddPlaceholder)
                menu.addAction(separator)

            if node.getFeature('type') == 'Hardware':
                menu.addAction(self.uiActionMorphSpecialComponent)
                menu.addAction(separator)

            if level > 1:
                menu.addAction(self.uiActionRemoveComponent)

            menu.exec_(self.treeEditor.uiComponentsView.viewport().mapToGlobal(position))

    def checkPage(self, page):
        """
        Checks if the user is in the correct page and notify with a dialog if it's not.

        Args:
            page (int): the page to check for.

        Returns:
            bool: whether the user is in the correct page or not.
        """

        if self.uiTabWidget.currentIndex() != page:
            self.okDialog('Warning!', 'You are not in the proper page!')
            return True
        return False



# MAIN
if __name__ == '__main__':
    import sys
    app = qtw.QApplication(sys.argv)
    app.setStyleSheet(qss)

    mw = MainWindow()
    mw.showMaximized()

    app.exec_()