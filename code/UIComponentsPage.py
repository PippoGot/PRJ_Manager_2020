from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import os

from ProxyTree import ProxyTree
from constants import COMPONENTS_PAGE_SIZES

uiPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources\\UIs\\')
ui = uic.loadUiType(os.path.join(uiPath, "ui_components_page.ui"))[0]

class ComponentsPage(qtw.QWidget, ui):
    """
    This window is the one managing the components list and editor. Displays the components
    and manages their modifications.
    """

    def __init__(self, manufacture_model):
        """
        Loads the UI window and set the manufacture model.

        Args:
            manufacture_model (QAbstractItemModel): the model with the values for the combobox.
        """

        super(ComponentsPage, self).__init__()
        self.uiManufacture = None
        self.setupUi(self)

        self.mapper = qtw.QDataWidgetMapper()
        self.current = None
        self.uiComponentsEditor.setDisabled(True)
        self.manufactures = manufacture_model

    def setModel(self, model):
        """
        Sets the editor's and view's model, then refreshes the view.

        Custom function:
            self.refreshView()

        Args:
            model (ModelTree): the model of the view and editor widget.
        """

        self.model = model
        self.current = None

        if self.model:
            self.treeProxyModel = ProxyTree()
            self.treeProxyModel.setSourceModel(self.model)
            self.treeProxyModel.sort(0, qtc.Qt.AscendingOrder)
            self.uiComponentsView.setModel(self.treeProxyModel)

            self.mapper.setModel(self.model)
            self.mapper.addMapping(self.uiNumberID, 0)
            self.mapper.addMapping(self.uiName, 1)
            self.mapper.addMapping(self.uiDescription, 2)
            self.mapper.addMapping(self.uiType, 3)
            self.mapper.addMapping(self.uiManufacture, 4)
            self.mapper.addMapping(self.uiStatus, 5)
            self.mapper.addMapping(self.uiComment, 6)
            self.mapper.addMapping(self.uiPriceUnit, 7)
            self.mapper.addMapping(self.uiQuantityNeeded, 8)
            self.mapper.addMapping(self.uiQuantityUnit, 9)
            self.mapper.addMapping(self.uiSeller, 10)
            self.mapper.addMapping(self.uiLink, 11)

            self.treeSelection = self.uiComponentsView.selectionModel()
            self.treeSelection.currentChanged.connect(self.mapTreeIndex)

            self.model.dataChanged.connect(self.mapper.revert)

            self.treeProxyModel.setFilterRegExp('Deprecated')

            self.refreshView()
        else:
            self.uiComponentsView.setModel(None)
            self.mapper.setModel(None)
            self.uiComponentsEditor.setDisabled(True)

    def mapTreeIndex(self, index):
        """
        Convert the given index from a proxy model index to an original model index.
        Then the index is set as the current index of the editor.

        Custom functions:
            self.changeManufacture()

        Args:
            index (QModelIndex): the index to convert.
        """

        index = self.treeProxyModel.mapToSource(index)

        parent = index.parent()
        self.mapper.setRootIndex(parent)
        self.mapper.setCurrentModelIndex(index)

        self.current = index
        self.uiComponentsEditor.setDisabled(False)

        self.changeManufacture()

    def changeManufacture(self):
        """
        Changes dinamically the manufacture widget and initializes it's text in every context.
        The editable nodes will have a combobox, while non-editable nodes will have a read-only line edit.

        Custom functions:
            BaseNode.getFeature()
        """

        layout = self.uiManufacture.parentWidget().layout()
        currentNode = self.current.internalPointer()
        text = currentNode.getFeature('manufacture')

        layout.removeWidget(self.uiManufacture)
        self.uiManufacture.close()
        layout.removeRow(2)

        if not currentNode.getFeature('manufactureEditable'):
            self.uiManufacture = qtw.QLineEdit()
            self.uiManufacture.setReadOnly(True)
            self.uiManufacture.setText(text)
        else:
            self.uiManufacture = qtw.QComboBox()
            self.uiManufacture.setCurrentIndex(0)
            self.uiManufacture.setModel(self.manufactures)

        layout.insertRow(2, 'Manufacture', self.uiManufacture)
        layout.update()

    def refreshView(self):
        """
        Updates the view resizing the columns to a specified value and expanding the tree.
        Also sorts the items.
        """

        self.uiComponentsView.expandAll()
        for column in range(self.treeProxyModel.columnCount(qtc.QModelIndex())):
            self.uiComponentsView.setColumnWidth(column, COMPONENTS_PAGE_SIZES[column])
        self.treeProxyModel.sort(0, qtc.Qt.AscendingOrder)