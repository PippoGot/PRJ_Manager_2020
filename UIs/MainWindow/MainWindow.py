# LIBRARIES
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import os

# MODELS
from Models.ModelCombobox import ModelCombobox
from Models.ModelTree import ModelTree

# POPUPS
from ..NewComponentEditor.NewComponentEditor import NewComponentEditor
from ..HardwareSelector.HardwareSelector import HardwareSelector

# PAGES
from ..ComponentsPage.ComponentsPage import ComponentsPage
from ..ArchivePage.ArchivePage import ArchivePage

# RESOURCES
from .. import resources

# UI
from .main_window import Ui_uiMainWindow as ui

class MainWindow(qtw.QMainWindow, ui):
    def __init__(self):
        """
        Loads the UI window and set the manufacture model.
        """

        super(MainWindow, self).__init__()
        self.setupUi(self)

# COMBOBOX MODELS
        self.manufactureModel = ModelCombobox(r'D:\Data\_PROGETTI\APPS\PRJ Manager 2.0\UIs\MainWindow\manufactures.csv')
        self.statusModel = ModelCombobox(r'D:\Data\_PROGETTI\APPS\PRJ Manager 2.0\UIs\MainWindow\statuses.csv')

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
        self._setModel(ModelTree())

# EDIT MENU
        self.uiActAddAssembly.triggered.connect(self.addAssemblyNode)
        self.uiActAddPart.triggered.connect(self.addLeafNode)
        self.uiActAddSpecial.triggered.connect(self.addSpecialNode)
        self.uiActAddJig.triggered.connect(self.addJigNode)
        self.uiActAddPlaceholder.triggered.connect(self.addPlaceholderNode)

# EDIT MENU FUNCTIONS

    def addAssemblyNode(self):
        """
        Adds an assembly node.
        """

        def func():
            newNode = self.componentsPage.getNewNode('Assembly')
            if newNode:
                self._addGenericNode(newNode)

        self._checkGenericNode(func)

    def addLeafNode(self):
        """
        Adds a leaf node.
        """

        def func():
            newNode = self.treeModel.getNewNode('Leaf')
            if newNode:
                self._addGenericNode(newNode)

        self._checkGenericNode(func)

    def addSpecialNode(self):
        """
        Adds a special node, either hardware or product.
        """

        def func():
            self.newSelector = HardwareSelector()
            self.newSelector.submit.connect(self.componentsPage.addNode)

        self._checkGenericNode(func)

    def addJigNode(self):
        """
        Adds a jig node.
        """

        def func():
            newNode = self.treeModel.getNewNode('Jig')
            if newNode:
                self._addGenericNode(newNode)

        self._checkGenericNode(func)

    def addPlaceholderNode(self):
        """
        Adds a placeholder node.
        """

        def func():
            newNode = self.treeModel.getNewNode('Placeholder')
            if newNode:
                self._addGenericNode(newNode)

        self._checkGenericNode(func)

# PRIVATE UTILITY FUNCTIONS

    def _setModel(self, model):
        """
        Sets the models if one is given, then updates the models of the other widgets.

        Args:
            model (ModelTree): the new model
        """

        self.treeModel = model
        self.componentsPage.setModel(self.treeModel)

# NODES HANDLING

    def _checkGenericNode(self, func):
        """
        Does all the checkings to add a node then executes the specific passed function
        to add the node. A node can be added only in the proper page and on a component
        with a level lower than 5.

        Args:
            func (PyFunction): the function to execute to add the node in the proper way
        """

        if self._checkPage(0): return

        currentNode = self.componentsPage.getCurrentNode()

        if currentNode:
            if currentNode.getLevel() < 5:
                func()
            else:
                self._okDialog('Warning!', 'The selected item is not of an appropriate level!')
        else:
            self._okDialog('Warning!', 'No item currently selected.')

    def _addGenericNode(self, node):
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