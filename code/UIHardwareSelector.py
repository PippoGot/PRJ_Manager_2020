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

    submit = qtc.pyqtSignal(ComponentTree)                                

    def __init__(self, archive):
        """Loads the .ui file, connects the buttons to the respective functions, 
        sets the widgets models for the views and finally refreshes the views.

        INPUT:
            HardwareModel - archive: model that connects to the hardware archive
        """

        super(HardwareSelector, self).__init__()                            
        
        uic.loadUi('D:/Data/_PROGETTI/Apps/PRJ_Manager/UIs/ui_hardware_selector.ui', self) 

        self.uiCancelButton.clicked.connect(self.close)              
        self.uiOkButton.clicked.connect(self.onSubmit)

        self.uiMechanicalButton.clicked.connect(self.changeFilter)
        self.uiMeasuredButton.clicked.connect(self.changeFilter)
        self.uiElectricalButton.clicked.connect(self.changeFilter)
        self.uiElectromechanicalButton.clicked.connect(self.changeFilter)
        self.uiConsumableButton.clicked.connect(self.changeFilter)
        self.uiSearchEntry.textChanged.connect(self.changeFilter)

        self.current = None                                                           
        self.currentSelection = None
        self.uiOkButton.setDisabled(True)                                           

        self.model = archive                                                           
        self.proxyModel = HardwareProxyModel()                                    
        self.proxyModel.setSourceModel(self.model)                                      
        self.proxyModel.setSortCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.proxyModel.sort(0, qtc.Qt.DescendingOrder)                               
        self.uiHardwareView.setModel(self.proxyModel)                          

        self.selectionModel = self.uiHardwareView.selectionModel()            
        self.selectionModel.currentChanged.connect(self.setCurrentIndex)                 
        self.selectionModel.selectionChanged.connect(self.setCurrentSelection)             

        self.changeFilter()

    def setCurrentSelection(self):
        """Updates the archive selection."""

        self.currentSelection = self.selectionModel.selectedIndexes()              

    def setCurrentIndex(self, index):
        """
        Updates the current selected item parameter.

        INPUT:
            QModelIndex - index: the index of the current selected item
        """

        self.current = index                                                       
        self.uiOkButton.setDisabled(False)                                

    def onSubmit(self):
        """
        Emits a signal with the current selected item data.
        The signal can be connected to the TreeModel insertRows() function if a row and an index are set 
        as class parameters before emitting the signal.
        """

        if self.currentSelection and len(self.currentSelection) > 1:                 
            self.msgBox = qtw.QMessageBox.warning(                           
                self, 
                'Warning!', 
                'Multiple items currently selected.\nSelect only one item to add', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

        else:                                                        
            index = self.proxyModel.mapToSource(self.current)                         
            data = index.internalPointer()                              
            newComponent = ComponentTree(data['number'], data)
            newComponent.quantity = self.uiSelectQuantity.text()
            self.submit.emit(newComponent)                                         
            self.close()                                                              

    def changeFilter(self):
        """When called, scans the buttons and filters the selected cathegory of items in the view."""
        
        text = self.uiSearchEntry.text()                                              
        textString = '.*(' + text.replace(' ', ').*(') + ')'                          

        if self.uiMechanicalButton.isChecked():                                      
            filterString = '#MEH-[0-9A-Z]{3}' + textString                 
        elif self.uiMeasuredButton.isChecked():
            filterString = '#MMH-[0-9A-Z]{3}' + textString
        elif self.uiElectricalButton.isChecked():
            filterString = '#ELH-[0-9A-Z]{3}' + textString
        elif self.uiConsumableButton.isChecked():
            filterString = '#CON-[0-9A-Z]{3}' + textString
        else:
            filterString = '#EMH-[0-9A-Z]{3}' + textString

        self.proxyModel.setFilterRegExp(filterString)                                
        self.refreshView()                                                             

    def refreshView(self):
        """Updates the view."""

        for column in range(self.model.columnCount(qtc.QModelIndex())):
            if column != self.model.columnCount(qtc.QModelIndex()):
                self.uiHardwareView.resizeColumnToContents(column)
        self.uiHardwareView.horizontalHeader().setStretchLastSection(True)