from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from ProxyTree import ProxyTree

class ComponentsPage(qtw.QWidget):
    """
    This widget is the one managing the components list and editor. Displays the components
    and manages their modifications.
    """

    def __init__(self):
        """Loads the .ui file."""

        super(ComponentsPage, self).__init__()                                              # superclass constructor

        uic.loadUi('D:/Data/_PROGETTI/Apps/PRJ_Manager/UIs/ui_components_page.ui', self)    # loads the interface from the .ui file

        self.mapper = qtw.QDataWidgetMapper()
        self.current = None
        self.uiComponentsEditor.setDisabled(True)

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

    def refreshView(self):
        """Updates the view."""

        self.uiComponentsView.expandAll()                                                   # every item is expanded
        for column in range(self.treeProxyModel.columnCount(qtc.QModelIndex())):            # then every column is resized to it's content
            self.uiComponentsView.setColumnWidth(column, self.sizes[column])
        
        self.treeProxyModel.sort(0, qtc.Qt.AscendingOrder)                                  # automatically sorts the view before displaying

    sizes = {                                                                               # size dictionary
        0: 150,
        1: 200,
        2: 340,
        3: 130,
        4: 130,
        5: 130,
        6: 340,
        7: 60,
        8: 60
    }