from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from ProxyHardware import HardwareProxyModel

class HardwareEditor(qtw.QWidget):
    """
    This widget is the one responsible for the editing of the hardware archive.
    it can remove and add items from it, as well as edit them.
    """
    
    def __init__(self, archive):
        """
        Loads the .ui file, connects the buttons to their respective functions and sets the widget model.

        INPUT:
            ModelHardware - archive: model that connects to the hardware archive
        """
        
        super(HardwareEditor, self).__init__()                                          

        uic.loadUi('code/resources/UIs/ui_hardware_editor_page.ui', self)  

        self.uiSubmitButton.clicked.connect(self.addHardwareToArchive)                    
        self.uiRemoveButton.clicked.connect(self.removeHardware)

        self.uiSearchEntry.addAction(qtg.QIcon('code/resources/icons/search.png'), qtw.QLineEdit.LeadingPosition)

        self.uiMEHCheck.clicked.connect(self.updateNumber)
        self.uiMMHCheck.clicked.connect(self.updateNumber)
        self.uiELHCheck.clicked.connect(self.updateNumber)
        self.uiEMHCheck.clicked.connect(self.updateNumber)
        self.uiCONCheck.clicked.connect(self.updateNumber)
        self.uiSearchEntry.textChanged.connect(self.changeFilter)

        self.uiRemoveButton.setDisabled(True)                                               

        self.current = None                                                                  
        self.prefix = 'MEH'                                                 

        self.archive = archive                                                              
        self.proxyModel = HardwareProxyModel()                                        
        self.proxyModel.setSourceModel(self.archive)                                        
        self.proxyModel.sort(0, qtc.Qt.DescendingOrder)                                   
        self.uiHardwareView.setModel(self.proxyModel)                          

        self.selectionModel = self.uiHardwareView.selectionModel()                        
        self.selectionModel.selectionChanged.connect(self.setCurrentSelection)              

        self.mapper = qtw.QDataWidgetMapper()
        self.mapper.setModel(self.archive)

        self.mapper.addMapping(self.uiCurrentNumberID, 0)                               
        self.mapper.addMapping(self.uiCurrentName, 2)
        self.mapper.addMapping(self.uiCurrentDescription, 3)
        self.mapper.addMapping(self.uiCurrentType, 4)
        self.mapper.addMapping(self.uiCurrentManufacture, 5)
        self.mapper.addMapping(self.uiCurrentStatus, 6)
        self.mapper.addMapping(self.uiCurrentComment, 7)
        self.mapper.addMapping(self.uiCurrentPriceUnit, 8)
        self.mapper.addMapping(self.uiCurrentQuantityNeeded, 9)
        self.mapper.addMapping(self.uiCurrentQuantityUnit, 10)
        self.mapper.addMapping(self.uiCurrentSeller, 11)
        self.mapper.addMapping(self.uiCurrentKit, 12)
        self.mapper.addMapping(self.uiCurrentLink, 13)

        self.updateNumber()
        self.uiCurrentComponentEditor.setDisabled(True)

    def updateNumber(self):
        """
        When a radio button is checked the number of the current item that is being added
        is recalculated and updated. The values are reset.
        """

        if self.uiMEHCheck.isChecked():                                                       
            self.prefix = 'MEH'                                                        
        elif self.uiMMHCheck.isChecked():
            self.prefix = 'MMH'
        elif self.uiELHCheck.isChecked():
            self.prefix = 'ELH'
        elif self.uiCONCheck.isChecked():
            self.prefix = 'CON'
        else:
            self.prefix = 'EMH'

        number = '#' + self.prefix + '-000'                                         

        self.uiNewNumberID.setText(self.archive.calculateNumber(number))

        self.initFields()
        self.changeFilter()                                                         

    def addHardwareToArchive(self):
        """Adds a new hardware item to the archive and resets the values for a new item."""

        data = {
            'number': self.uiNewNumberID.text(),                                   
            'title': self.uiNewName.text(), 
            'description': self.uiNewDescription.toPlainText(),
            'type': self.uiNewType.text(),
            'manufacture': self.uiNewManufacture.text(),
            'status': self.uiNewStatus.currentText(),
            'comment': self.uiNewComment.toPlainText(),
            'price': self.uiNewPriceUnit.text(),
            'quantity': self.uiNewQuantityNeeded.text(),
            'quantityPackage': self.uiNewQuantityUnit.text(),
            'seller': self.uiNewSeller.text(),
            'kit': '',
            'link': self.uiNewLink.toPlainText()
        }

        self.archive.insertRows(data)                                                

        self.updateNumber()
    
    def setCurrentSelection(self):
        """Updates the archive selection and enables the remove button."""

        self.currentSelection = self.selectionModel.selectedIndexes()                      
        self.current = self.proxyModel.mapToSource(self.selectionModel.currentIndex())
        self.uiRemoveButton.setDisabled(False)                                          
        self.uiCurrentComponentEditor.setDisabled(False)
        parent = self.current.parent()                                                   
        self.mapper.setRootIndex(parent)                                             
        self.mapper.setCurrentModelIndex(self.current)

        self.changeManufacture(self.uiCurrentNumberID.text(), self.uiCurrentManufacture)

    def removeHardware(self):
        """Removes the selected item from the archive model."""
        
        mapped = []                                                                      
        if not self.currentSelection: return
        
        for index in self.currentSelection:                                       
            mapped.append(self.proxyModel.mapToSource(index))                               

        self.archive.removeRows(mapped)                                                    

        self.currentSelection = None
        self.updateNumber()                                                          
        self.uiRemoveButton.setDisabled(True)

    def refreshView(self):
        """Updates the view."""

        for column in range(self.archive.columnCount(qtc.QModelIndex())):
            if column != self.archive.columnCount(qtc.QModelIndex()):
                self.uiHardwareView.resizeColumnToContents(column)
        self.uiHardwareView.horizontalHeader().setStretchLastSection(True)

    def changeFilter(self):
        """When called, scans the buttons and filters the selected cathegory of items in the view."""
        
        text = self.uiSearchEntry.text()                                                  
        textString = '.*(' + text.replace(' ', ').*(') + ')'                             

        if self.uiMEHCheck.isChecked():                                                 
            filterString = '#MEH-[0-9A-Z]{3}' + textString                        
        elif self.uiMMHCheck.isChecked():
            filterString = '#MMH-[0-9A-Z]{3}' + textString
        elif self.uiELHCheck.isChecked():
            filterString = '#ELH-[0-9A-Z]{3}' + textString
        elif self.uiCONCheck.isChecked():
            filterString = '#CON-[0-9A-Z]{3}' + textString
        else:
            filterString = '#EMH-[0-9A-Z]{3}' + textString

        self.proxyModel.setFilterRegExp(filterString)                                      
        self.refreshView()

    def initFields(self):
        """Resets all the editor values to a default value."""
        
        self.uiNewName.setText('-')                                                        
        self.uiNewDescription.setPlainText('-')
        self.uiNewComment.setPlainText('-')
        self.uiNewSeller.setText('-')
        self.uiNewLink.setPlainText('-')
        self.uiNewPriceUnit.setText('0')

        if self.uiCONCheck.isChecked():
            self.uiNewType.setText('Consumables')
        else:
            self.uiNewType.setText('Hardware')

        self.changeManufacture(self.uiNewNumberID.text(), self.uiNewManufacture)

    def changeManufacture(self, number, widgetPtr):
        if number[1:4] == 'MMH':
            widgetPtr.setText('Cut to length')
        else:
            widgetPtr.setText('Off the shelf')