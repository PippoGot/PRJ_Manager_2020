from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from ProxyHardware import HardwareProxyModel
from ComponentTree import ComponentTree

class HardwareSelector(qtw.QWidget):
    """
    This class is a popup window for inserting hardware components into the list.
    It can also add and remove hardware components to and from the archive file.
    Emits the signal containing all the data when a component needs to be added.
    """

    submit = qtc.pyqtSignal(ComponentTree)                                    # signal emitted when submit is pressed

    def __init__(self, archive):
        """Loads the .ui file, connects the buttons to the respective functions, 
        sets the widgets models for the views and finally refreshes the views.

        INPUT:
            HardwareModel - archive: model that connects to the hardware archive
        """

        super(HardwareSelector, self).__init__()                                            # superclass constructor    
        
        uic.loadUi('D:/Data/_PROGETTI/Apps/PRJ_Manager/UIs/ui_hardware_selector.ui', self)  # loads the UI from the .ui file

        self.uiCancelButton.clicked.connect(self.close)                                     # connects the buttons to the respective functions
        self.uiOkButton.clicked.connect(self.onSubmit)

        self.uiMechanicalButton.clicked.connect(self.changeFilter)
        self.uiMeasuredButton.clicked.connect(self.changeFilter)
        self.uiElectricalButton.clicked.connect(self.changeFilter)
        self.uiElectromechanicalButton.clicked.connect(self.changeFilter)
        self.uiConsumableButton.clicked.connect(self.changeFilter)
        self.uiSearchEntry.textChanged.connect(self.changeFilter)

        self.current = None                                                                 # initialize the parameter current to None
        self.currentSelection = None
        self.uiOkButton.setDisabled(True)                                                   # and disables the ok and remove buttons

        self.model = archive                                                                # save the archive model in a class parameter
        self.proxyModel = HardwareProxyModel()                                              # creates a hardware proxy model
        self.proxyModel.setSourceModel(self.model)                                          # and sets the original model as it's source model
        self.proxyModel.setSortCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.proxyModel.sort(0, qtc.Qt.DescendingOrder)                                     # automatically sorts the view before displaying
        self.uiHardwareView.setModel(self.proxyModel)                                       # and sets the proxy model as the view source model

        self.selectionModel = self.uiHardwareView.selectionModel()                          # then extract the selection model from the view
        self.selectionModel.currentChanged.connect(self.setCurrentIndex)                    # and connects the current changed signal to the update function
        self.selectionModel.selectionChanged.connect(self.setCurrentSelection)              # and the selection changed signal is connected to the respective function

        self.changeFilter()

    def setCurrentSelection(self):
        """Updates the archive selection."""

        self.currentSelection = self.selectionModel.selectedIndexes()                       # the class parameter is updated with the current selected indexes

    def setCurrentIndex(self, index):
        """
        Updates the current selected item parameter.

        INPUT:
            QModelIndex - index: the index of the current selected item
        """

        self.current = index                                                                # updates the parameter
        self.uiOkButton.setDisabled(False)                                                  # and enables the ok buttons

    def onSubmit(self):
        """
        Emits a signal with the current selected item data.
        The signal can be connected to the TreeModel insertRows() function if a row and an index are set 
        as class parameters before emitting the signal.
        """

        if self.currentSelection and len(self.currentSelection) > 1:                        # if more than one item is selected
            self.msgBox = qtw.QMessageBox.warning(                                          # the user is notified
                self, 
                'Warning!', 
                'Multiple items currently selected.\nSelect only one item to add', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

        else:                                                                               # otherwise
            index = self.proxyModel.mapToSource(self.current)                               # the index is mapped from the proxy model to the original model
            data = index.internalPointer()                                                  # the data is extracted
            newComponent = ComponentTree(data['number'], data)
            newComponent.quantity = self.uiSelectQuantity.text()
            self.submit.emit(newComponent)                                                  # the signal is emitted
            self.close()                                                                    # and the selector is closed

    def changeFilter(self):
        """When called, scans the buttons and filters the selected cathegory of items in the view."""
        
        text = self.uiSearchEntry.text()                                                    # extracts the entry text
        textString = '.*(' + text.replace(' ', ').*(') + ')'                                # creates two empty strings

        if self.uiMechanicalButton.isChecked():                                             # then scans the buttons
            filterString = '#MEH-[0-9A-Z]{3}' + textString                                  # and creates the filter string
        elif self.uiMeasuredButton.isChecked():
            filterString = '#MMH-[0-9A-Z]{3}' + textString
        elif self.uiElectricalButton.isChecked():
            filterString = '#ELH-[0-9A-Z]{3}' + textString
        elif self.uiConsumableButton.isChecked():
            filterString = '#CON-[0-9A-Z]{3}' + textString
        else:
            filterString = '#EMH-[0-9A-Z]{3}' + textString

        self.proxyModel.setFilterRegExp(filterString)                                       # updates the filter expression
        self.refreshView()                                                                  # finally resizes the view to its content

    def refreshView(self):
        """Updates the view."""

        for column in range(self.model.columnCount(qtc.QModelIndex())):                     # every column is resized to it's content
            self.uiHardwareView.resizeColumnToContents(column)