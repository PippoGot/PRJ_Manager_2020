from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import os

from Models.ModelCombobox import ModelCombobox
from Models.ModelTree import ModelTree

from ..NewComponentEditor.NewComponentEditor import NewComponentEditor
from ..HardwareSelector.HardwareSelector import HardwareSelector

from ..ComponentsPage.ComponentsPage import ComponentsPage
from ..ArchivePage.ArchivePage import ArchivePage

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