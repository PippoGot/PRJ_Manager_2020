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
            self.mapper.addMapping(self.uiName, 2)
            self.mapper.addMapping(self.uiDescription, 3)
            self.mapper.addMapping(self.uiType, 4)
            self.mapper.addMapping(self.uiManufacture, 5)
            self.mapper.addMapping(self.uiStatus, 6)
            self.mapper.addMapping(self.uiComment, 7)
            self.mapper.addMapping(self.uiPriceUnit, 8)
            self.mapper.addMapping(self.uiQuantityNeeded, 9)
            self.mapper.addMapping(self.uiQuantityUnit, 10)
            self.mapper.addMapping(self.uiSeller, 11)
            self.mapper.addMapping(self.uiKit, 12)
            self.mapper.addMapping(self.uiLink, 13)

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

        self.changeManufactureWidget(self.uiType.text(), self.uiManufacture, self.uiNumberID)

    def changeManufactureWidget(self, nodeType, widgetPtr, numberPtr):
        """
        Changes dinamically the manufacture widget and initializes it's text in every context.

        INPUT:
            str - nodeType: the type of the current component
            QWidget - widgetPtr: the widget to modify
            QWidget - numberPtr: the widget holding the number
        """

        layout = widgetPtr.parentWidget().layout()

        def changeWidget(widget, widgetPointer, text = None):
            layout.removeWidget(widgetPointer)
            widgetPointer.close()
            layout.removeRow(2)

            if widget == 'LineEdit':
                widgetPointer = qtw.QLineEdit()
                widgetPointer.setReadOnly(True)
                widgetPointer.setText(text)
            elif widget == 'ComboBox':
                widgetPointer = qtw.QComboBox()
                widgetPointer.setCurrentIndex(0)
                widgetPointer.setModel(self.manufactures)

            layout.insertRow(2, 'Manufacture', widgetPointer)
            layout.update()

        if nodeType == 'Project' or nodeType == 'Assembly':
            changeWidget('LineEdit', widgetPtr, 'Assembled')
        elif nodeType == 'Hardware' or nodeType == 'Consumables':
            if numberPtr.text()[1:4] == 'MMH':
                changeWidget('LineEdit', widgetPtr, 'Cut to Length')
            else:
                changeWidget('LineEdit', widgetPtr, 'Off the Shelf')
        elif nodeType == 'Placeholder':
            changeWidget('LineEdit', widgetPtr, 'None')
        else:
            changeWidget('ComboBox', widgetPtr)

    def refreshView(self):
        """Updates the view."""

        self.uiComponentsView.expandAll()
        for column in range(self.treeProxyModel.columnCount(qtc.QModelIndex())):
            self.uiComponentsView.setColumnWidth(column, COMPONENTS_PAGE_SIZES[column])

        self.treeProxyModel.sort(0, qtc.Qt.AscendingOrder)