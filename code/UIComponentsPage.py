from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from ProxyTree import ProxyTree
from constants import COMPONENTS_PAGE_SIZES

class ComponentsPage(qtw.QWidget):
    """
    This widget is the one managing the components list and editor. Displays the components
    and manages their modifications.
    """

    def __init__(self, manufacture_model):
        """Loads the .ui file."""

        super(ComponentsPage, self).__init__()

        self.uiManufacture = None

        uic.loadUi('code/resources/UIs/ui_components_page.ui', self)

        self.mapper = qtw.QDataWidgetMapper()
        self.current = None
        self.uiComponentsEditor.setDisabled(True)
        self.manufactures = manufacture_model

    def setModel(self, model):
        """
        Sets the editor's and view's model, then refreshes the view.

        INPUT:
            ModelTree - model: the model that the widgets are set to
        """

        self.model = model

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
            self.mapper.addMapping(self.uiKit, 11)
            self.mapper.addMapping(self.uiLink, 12)

            self.treeSelection = self.uiComponentsView.selectionModel()
            self.treeSelection.currentChanged.connect(self.mapTreeIndex)

            self.model.dataChanged.connect(self.mapper.revert)

            self.treeProxyModel.setFilterRegExp('Deprecated')

            self.refreshView()
        else:
            self.uiComponentsView.setModel(None)
            self.mapper.setModel((None))
            self.uiComponentsEditor.setDisabled(True)

    def mapTreeIndex(self, index):
        """
        Convert the given index from a proxy model index to an original model index.
        Then the index is set as the current index of the editor.

        INPUT:
            QModelIndex - index: the index to convert
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

        INPUT:
            str - nodeType: the type of the current component
            QWidget - widgetPtr: the widget to modify
            QWidget - numberPtr: the widget holding the number
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
        """Updates the view."""

        self.uiComponentsView.expandAll()
        for column in range(self.treeProxyModel.columnCount(qtc.QModelIndex())):
            self.uiComponentsView.setColumnWidth(column, COMPONENTS_PAGE_SIZES[column])
        self.treeProxyModel.sort(0, qtc.Qt.AscendingOrder)