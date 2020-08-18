from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from HardwareProxyModel import HardwareProxyModel

class HardwareEditor(qtw.QWidget):
    """
    This widget is the one responsible for the editing of the hardware archive.
    it can remove and add items from it, as well as edit them.
    """
    
    def __init__(self, archive):
        """
        Loads the .ui file, connects the buttons to their respective functions and sets the widget model.

        INPUT:
            HardwareModel - archive: model that connects to the hardware archive
        """
        
        super(HardwareEditor, self).__init__()                                              # superclass constructor

        uic.loadUi('D:/Data/_PROGETTI/Apps/PRJ_Manager/UIs/ui_hardware_editor_page.ui', self)        # loads the UI from the .ui file

        self.uiSubmitButton.clicked.connect(self.addHardwareToArchive)                      # connects the buttons to their functions
        self.uiRemoveButton.clicked.connect(self.removeHardware)

        self.uiMEHCheck.clicked.connect(self.updateNumber)
        self.uiMMHCheck.clicked.connect(self.updateNumber)
        self.uiELHCheck.clicked.connect(self.updateNumber)
        self.uiEMHCheck.clicked.connect(self.updateNumber)
        self.uiCONCheck.clicked.connect(self.updateNumber)
        self.uiSearchEntry.textChanged.connect(self.changeFilter)

        self.uiRemoveButton.setDisabled(True)                                               # the remove button is set disabled by default

        self.current = None                                                                 # the parameter current is initialized as None
        self.prefix = 'MEH'                                                                 # prefix as MEH

        self.archive = archive                                                              # the hardware model is stored in a class parameter
        self.proxyModel = HardwareProxyModel()                                              # the proxy model is created
        self.proxyModel.setSourceModel(self.archive)                                        # and the archive is set as the original model
        self.proxyModel.sort(0, qtc.Qt.DescendingOrder)                                     # automatically sorts the view before displaying
        self.uiHardwareView.setModel(self.proxyModel)                                       # then the proxy model is set as the view model

        self.selectionModel = self.uiHardwareView.selectionModel()                          # the view's selection model is extracted
        self.selectionModel.selectionChanged.connect(self.setCurrentSelection)              # and the selection changed signal is connected to the respective function

        self.initFields()

        self.changeFilter()                                                                 # finally the filter is changed
        self.updateNumber()

        self.mapper = qtw.QDataWidgetMapper()
        self.mapper.setModel(self.archive)

        self.mapper.addMapping(self.uiCurrentNumberID, 0)                                  # adds all the mappings of the widget
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

    def updateNumber(self):
        """
        When a radio button is checked the number of the current item that is being added
        is recalculated and updated.
        """

        if self.uiMEHCheck.isChecked():                                                     # check for which radio button the function has been called
            self.prefix = 'MEH'                                                             # and updates the prefic parameter is updated
        elif self.uiMMHCheck.isChecked():
            self.prefix = 'MMH'
        elif self.uiELHCheck.isChecked():
            self.prefix = 'ELH'
        elif self.uiCONCheck.isChecked():
            self.prefix = 'CON'
        else:
            self.prefix = 'EMH'

        number = '#' + self.prefix + '-000'                                                 # compose the new number

        self.uiNewNumberID.setText(self.archive.calculateNumber(number))

        self.initFields()
        self.changeFilter()                                                                 # changes the filter

    def addHardwareToArchive(self):
        """Adds a new hardware item to the archive and generates a new item for it to be added."""

        data = {
            'number': self.uiNewNumberID.text(),                                               # gathers the data to emit
            'title': self.uiNewName.text(), 
            'description': self.uiNewDescription.toPlainText(),
            'type': self.uiNewType.text(),
            'manufacture': self.uiNewManufacture.currentText(),
            'status': self.uiNewStatus.currentText(),
            'comment': self.uiNewComment.toPlainText(),
            'priceUnit': self.uiNewPriceUnit.text(),
            'quantity': self.uiNewQuantityNeeded.text(),
            'quantityPackage': self.uiNewQuantityUnit.text(),
            'seller': self.uiNewSeller.text(),
            'kit': '',
            'link': self.uiNewLink.toPlainText()
        }

        self.archive.insertRows(data)                                                       # then the data is inserted in to the archive model

        self.updateNumber()
        self.refreshView()                                                                  # and the view refreshed
    
    def setCurrentSelection(self):
        """Updates the archive selection and enables the remove button."""

        self.currentSelection = self.selectionModel.selectedIndexes()                       # the class parameter is updated with the current selected indexes
        self.current = self.proxyModel.mapToSource(self.selectionModel.currentIndex())
        self.uiRemoveButton.setDisabled(False)                                              # and the button is enabled
        parent = self.current.parent()                                                       # extract the parent index
        self.mapper.setRootIndex(parent)                                                # and sets the mapper indexes
        self.mapper.setCurrentModelIndex(self.current)

    def removeHardware(self):
        """Removes the selected item from the archive model."""
        
        mapped = []                                                                         # an empty list is created for the indexes
        if not self.currentSelection: return
        
        for index in self.currentSelection:                                                 # for every index selected
            mapped.append(self.proxyModel.mapToSource(index))                               # the index is mapped to the source model and added to the list

        self.archive.removeRows(mapped)                                                     # then the indexes are removed from the archive

        self.currentSelection = None
        self.updateNumber()                                                                 # and the current number is updated
        self.uiRemoveButton.setDisabled(True)

    def refreshView(self):
        """Updates the view."""

        for column in range(self.proxyModel.columnCount(qtc.QModelIndex())):                # every column is resized to it's content
            self.uiHardwareView.setColumnWidth(column, self.sizes[column])

    sizes = {
        0: 70,
        1: 200,
        2: 360,
        3: 130,
        4: 130,
        5: 130,
        6: 130,
        7: 70,
        8: 355
    }

    def changeFilter(self):
        """When called, scans the buttons and filters the selected cathegory of items in the view."""
        
        text = self.uiSearchEntry.text()                                                    # extracts the entry text
        textString = ''                                                                     # creates two empty strings
        wordString = ''
        if len(text) > 0:                                                                   # if the entry has text
            words = text.split(' ')                                                         # it is split into words
            for word in words:                                                              # and for every word
                for letter in word:                                                         # for every letter in the word
                    wordString += '(' + letter.upper() + '|' + letter.lower() + ')'         # creates a string to accept both the upper case letter and the lower case letter
                textString += wordString + '([ -0-9a-zA-Z]+)?'                              # then the word string and the optional characters are added to the string
        
        if self.uiMEHCheck.isChecked():                                                     # then scans the buttons
            filterString = '#MEH-[0-9A-Z]{3}([ -0-9a-zA-Z]+)?' + textString                 # and creates the filter string
        elif self.uiMMHCheck.isChecked():
            filterString = '#MMH-[0-9A-Z]{3}([ -0-9a-zA-Z]+)?' + textString
        elif self.uiELHCheck.isChecked():
            filterString = '#ELH-[0-9A-Z]{3}([ -0-9a-zA-Z]+)?' + textString
        elif self.uiCONCheck.isChecked():
            filterString = '#CON-[0-9A-Z]{3}([ -0-9a-zA-Z]+)?' + textString
        else:
            filterString = '#EMH-[0-9A-Z]{3}([ -0-9a-zA-Z]+)?' + textString

        self.proxyModel.setFilterRegExp(filterString)                                       # updates the filter expression
        self.refreshView()                                                                  # finally resizes the view to its content

    def initFields(self):
        self.uiNewName.setText('-')                                                      # sets some fields to default values
        self.uiNewDescription.setPlainText('-')
        self.uiNewComment.setPlainText('-')
        self.uiNewSeller.setText('-')
        self.uiNewLink.setPlainText('-')
        self.uiNewPriceUnit.setText('0')

        if self.uiCONCheck.isChecked():
            self.uiNewType.setText('Consumables')
        else:
            self.uiNewType.setText('Hardware')