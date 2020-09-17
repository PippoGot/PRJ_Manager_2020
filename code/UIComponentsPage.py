from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from ProxyTree import ProxyTree
from constants import COMPONENTS_PAGE_SIZES as sizes

class ComponentsPage(qtw.QWidget):
    """
    This widget is the one managing the components list and editor. Displays the components
    and manages their modifications.
    """

    def __init__(self, manufacture_model):
        """Loads the .ui file."""

        super(ComponentsPage, self).__init__()                                              # superclass constructor

        uic.loadUi('D:/Data/_PROGETTI/Apps/PRJ_Manager/UIs/ui_components_page.ui', self)    # loads the interface from the .ui file

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

        self.model = model                                                                  # stores the model in a class parameter

        if self.model:
            self.treeProxyModel = ProxyTree()                                               # creates the proxy model for the view
            self.treeProxyModel.setSourceModel(self.model)                                  # and sets the original model as it's source model
            self.treeProxyModel.sort(0, qtc.Qt.AscendingOrder)                              # automatically sorts the view before displaying
            self.uiComponentsView.setModel(self.treeProxyModel)                             # then sets the proxy model as the view model 
            
            self.mapper.setModel(self.model)                                                # sets the mapper source model
            self.mapper.addMapping(self.uiNumberID, 0)                                      # adds all the mappings of the widget
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
            
            self.treeSelection = self.uiComponentsView.selectionModel()                     # then it extracts the selection model from the view
            self.treeSelection.currentChanged.connect(self.mapTreeIndex)                    # and connects the signal of current changed to the map function
            
            self.model.dataChanged.connect(self.mapper.revert)                              # it connects the data changed signal to the revert function of the editor

            self.treeProxyModel.setFilterRegExp('Deprecated')

            self.refreshView()                                                              # finally it refreshes the view to resize it
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

        index = self.treeProxyModel.mapToSource(index)                                      # converts the index

        parent = index.parent()                                                             # extract the parent index
        self.mapper.setRootIndex(parent)                                                    # and sets the mapper indexes
        self.mapper.setCurrentModelIndex(index)

        self.current = index                                                                # then updates the current parameter
        self.uiComponentsEditor.setDisabled(False)

        self.changeManufactureWidget(self.uiType.text(), self.uiManufacture, self.uiNumberID)

    def changeManufactureWidget(self, nodeType, widgetPtr, numberPtr):
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

        self.uiComponentsView.expandAll()                                                   # every item is expanded
        for column in range(self.treeProxyModel.columnCount(qtc.QModelIndex())):            # then every column is resized to it's content
            self.uiComponentsView.setColumnWidth(column, sizes[column])
        
        self.treeProxyModel.sort(0, qtc.Qt.AscendingOrder)                                  # automatically sorts the view before displaying