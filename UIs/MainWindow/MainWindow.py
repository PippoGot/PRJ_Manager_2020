from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import os

# change to tree when implemented
from Data.Nodes.CompositeNodes import AssemblyNode, LeafNode, JigNode, PlaceholderNode

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
        self.manufactureModel = ModelCombobox(r'D:\Data\_PROGETTI\APPS\PRJ_MANAGER_2020\UIs\MainWindow\manufactures.csv')
        self.statusModel = ModelCombobox(r'D:\Data\_PROGETTI\APPS\PRJ_MANAGER_2020\UIs\MainWindow\statuses.csv')

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

# DATA MOELS
        self._setModel(ModelTree())

# EDIT MENU
        self.uiActAddAssembly.triggered.connect(self.addAssemblyNode)
        self.uiActAddPart.triggered.connect(self.addLeafNode)
        self.uiActAddSpecial.triggered.connect(self.addSpecialNode)
        self.uiActAddJig.triggered.connect(self.addJigNode)
        self.uiActAddPlaceholder.triggered.connect(self.addPlaceholderNode)

# EDIT MENU FUNCTIONS

    def addAssemblyNode(self):
        newNode = self.componentsPage.getNewNode('Assembly')
        self._addGenericNode(newNode)

    def addLeafNode(self):
        newNode = LeafNode()# dummy code
        self._addGenericNode(newNode)

    def addSpecialNode(self):
        self.newSelector = HardwareSelector()
        self.newSelector.submit.connect(self.componentsPage.addNode)

    def addJigNode(self):
        newNode = JigNode(level = 3)# dummy code
        self._addGenericNode(newNode)

    def addPlaceholderNode(self):
        newNode = PlaceholderNode(level = 3)# dummy code
        self._addGenericNode(newNode)

# PRIVATE UTILITY FUNCTIONS

    def _setModel(self, model):
        self.treeModel = model
        self.componentsPage.setModel(self.treeModel)

    def _addGenericNode(self, node):
        self.newEditor = NewComponentEditor(node)
        self.newEditor.setManufactureModel(self.manufactureModel)
        self.newEditor.setStatusModel(self.statusModel)
        self.newEditor.submit.connect(self.componentsPage.addNode)

# MAIN
if __name__ == '__main__':
    import sys
    app = qtw.QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    app.exec_()