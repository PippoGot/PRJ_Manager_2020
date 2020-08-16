from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from HardwareProxyModel import HardwareProxyModel
from ComponentTree import ComponentTree

class HardwareSelector(qtw.QWidget):
    """
    This class is a popup window for inserting hardware components into the list.
    It can also add and remove hardware components to and from the archive file.
    Emits the signal containing all the data when a component needs to be added.
    """

    submit = qtc.pyqtSignal(int, ComponentTree, qtc.QModelIndex)                                    # signal emitted when submit is pressed
    # add = qtc.pyqtSignal()                                                                      # signal emitted when add hardware is pressed

    def __init__(self, archive):
        """Loads the .ui file, connects the buttons to the respective functions, 
        sets the widgets models for the views and finally refreshes the views.

        INPUT:
            HardwareModel - archive: model that connects to the hardware archive
        """

        super(HardwareSelector, self).__init__()                                                # superclass constructor    
        
        uic.loadUi('D:/Data/_PROGETTI/Apps/PRJ_Manager/UIs/ui_hardware_selector.ui', self)          # loads the UI from the .ui file

        self.uiCancelButton.clicked.connect(self.close)                                         # connects the buttons to the respective functions
        self.uiOkButton.clicked.connect(self.onSubmit)
        # self.uiRemoveHardwareButton.clicked.connect(self.removeHardware)
        # self.uiAddHardwareButton.clicked.connect(self.add.emit)

        self.uiMechanicalButton.clicked.connect(self.changeFilter)
        self.uiMeasuredButton.clicked.connect(self.changeFilter)
        self.uiElectricalButton.clicked.connect(self.changeFilter)
        self.uiElectromechanicalButton.clicked.connect(self.changeFilter)
        self.uiConsumableButton.clicked.connect(self.changeFilter)
        self.uiSearchEntry.textChanged.connect(self.changeFilter)

        self.current = None                                                                     # initialize the parameter current to None
        self.currentSelection = None
        self.uiOkButton.setDisabled(True)                                                       # and disables the ok and remove buttons
        # self.uiRemoveHardwareButton.setDisabled(True)

        self.model = archive                                                                    # save the archive model in a class parameter
        self.proxyModel = HardwareProxyModel()                                                  # creates a hardware proxy model
        self.proxyModel.setSourceModel(self.model)                                              # and sets the original model as it's source model
        self.proxyModel.setSortCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.proxyModel.sort(0, qtc.Qt.DescendingOrder)                                         # automatically sorts the view before displaying
        self.uiHardwareView.setModel(self.proxyModel)                                           # and sets the proxy model as the view source model

        self.selectionModel = self.uiHardwareView.selectionModel()                              # then extract the selection model from the view
        self.selectionModel.currentChanged.connect(self.setCurrentIndex)                        # and connects the current changed signal to the update function
        self.selectionModel.selectionChanged.connect(self.setCurrentSelection)                  # and the selection changed signal is connected to the respective function

        self.changeFilter()
        self.refreshView()                                                                      # finally it resizes the view to the content

    def setCurrentSelection(self):
        """Updates the archive selection."""

        self.currentSelection = self.selectionModel.selectedIndexes()                           # the class parameter is updated with the current selected indexes
        # self.uiRemoveHardwareButton.setDisabled(False)                                          # and the remove button is enabled

    # def removeHardware(self):
    #     """Removes the selected hardware item from the archive."""

    #     mapped = []                                                                             # an empty list is created for the indexes
    #     for index in self.currentSelection:                                                     # for every index selected
    #         mapped.append(self.proxyModel.mapToSource(index))                                   # the index is mapped to the source model and added to the list

    #     self.model.removeRows(mapped)                                                           # then the indexes are removed from the archive

    #     self.currentSelection = None

    def setCurrentIndex(self, index):
        """
        Updates the current selected item parameter.

        INPUT:
            QModelIndex - index: the index of the current selected item
        """

        self.current = index                                                                    # updates the parameter
        self.uiOkButton.setDisabled(False)                                                      # and enables the ok buttons

    def onSubmit(self):
        """
        Emits a signal with the current selected item data.
        The signal can be connected to the TreeModel insertRows() function if a row and an index are set 
        as class parameters before emitting the signal.
        """

        if self.currentSelection and len(self.currentSelection) > 1:                            # if more than one item is selected
            self.msgBox = qtw.QMessageBox.warning(                                              # the user is notified
                self, 
                'Warning!', 
                'Multiple items currently selected.\nSelect only one item to add', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

        else:                                                                                   # otherwise
            index = self.proxyModel.mapToSource(self.current)                                   # the index is mapped from the proxy model to the original model
            data = index.internalPointer()                                                      # the data is extracted
            newComponent = ComponentTree(data['number'], data)
            self.submit.emit(self.row, newComponent, self.index)                                     # the signal is emitted
            self.close()                                                                        # and the selector is closed

    def changeFilter(self):
        """When called, scans the buttons and filters the selected cathegory of items in the view."""
        
        text = self.uiSearchEntry.text()                                                        # extracts the entry text
        textString = ''                                                                         # creates two empty strings
        wordString = ''
        if len(text) > 0:                                                                       # if the entry has text
            words = text.split(' ')                                                             # it is split into words
            for word in words:                                                                  # and for every word
                for letter in word:                                                             # for every letter in the word
                    wordString += '(' + letter.upper() + '|' + letter.lower() + ')'             # creates a string to accept both the upper case letter and the lower case letter
                textString += wordString + '([ -0-9a-zA-Z]+)?'                                  # then the word string and the optional characters are added to the string
        
        if self.uiMechanicalButton.isChecked():                                                 # then scans the buttons
            filterString = '#MEH-[0-9A-Z]{3}([ -0-9a-zA-Z]+)?' + textString                     # and creates the filter string
        elif self.uiMeasuredButton.isChecked():
            filterString = '#MMH-[0-9A-Z]{3}([ -0-9a-zA-Z]+)?' + textString
        elif self.uiElectricalButton.isChecked():
            filterString = '#ELH-[0-9A-Z]{3}([ -0-9a-zA-Z]+)?' + textString
        elif self.uiConsumableButton.isChecked():
            filterString = '#CON-[0-9A-Z]{3}([ -0-9a-zA-Z]+)?' + textString
        else:
            filterString = '#EMH-[0-9A-Z]{3}([ -0-9a-zA-Z]+)?' + textString

        self.proxyModel.setFilterRegExp(filterString)                                           # updates the filter expression
        self.refreshView()                                                                      # finally resizes the view to its content

    def refreshView(self):
        """Updates the view."""

        for column in range(self.model.columnCount(qtc.QModelIndex())):                         # every column is resized to it's content
            self.uiHardwareView.resizeColumnToContents(column)