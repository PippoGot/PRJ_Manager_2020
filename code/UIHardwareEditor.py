from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from ProxyHardware import HardwareProxyModel
from CompositeNodes import HardwareNode, MeasuredNode, ConsumableNode


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

        self.current = None

        self.uiSubmitButton.clicked.connect(self.addHardwareToArchive)
        self.uiRemoveButton.clicked.connect(self.removeHardware)

        self.uiSearchEntry.addAction(qtg.QIcon('code/resources/icons/search.png'), qtw.QLineEdit.LeadingPosition)

        self.uiMEHCheck.clicked.connect(self.updateNumber)
        self.uiMMHCheck.clicked.connect(self.updateNumber)
        self.uiELHCheck.clicked.connect(self.updateNumber)
        self.uiEMHCheck.clicked.connect(self.updateNumber)
        self.uiCONCheck.clicked.connect(self.updateNumber)
        self.uiSearchEntry.textChanged.connect(self.changeFilter)

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
        self.mapper.addMapping(self.uiCurrentName, 1)
        self.mapper.addMapping(self.uiCurrentDescription, 2)
        self.mapper.addMapping(self.uiCurrentType, 3)
        self.mapper.addMapping(self.uiCurrentManufacture, 4)
        self.mapper.addMapping(self.uiCurrentStatus, 5)
        self.mapper.addMapping(self.uiCurrentComment, 6)
        self.mapper.addMapping(self.uiCurrentPriceUnit, 7)
        self.mapper.addMapping(self.uiCurrentQuantityNeeded, 8)
        self.mapper.addMapping(self.uiCurrentQuantityUnit, 9)
        self.mapper.addMapping(self.uiCurrentSeller, 10)
        self.mapper.addMapping(self.uiCurrentKit, 11)
        self.mapper.addMapping(self.uiCurrentLink, 12)

        self.updateNumber()

        self.uiCurrentComponentEditor.setDisabled(True)
        self.uiRemoveButton.setDisabled(True)

    def updateNumber(self):
        """
        When a radio button is checked the number of the current item that is being added
        is recalculated and updated. The values are reset.
        """

        self.checkFilters()
        self.uiNewNumberID.setText(self.archive.rootItem.getNewNumber(self.prefix, 5))
        self.initFields()
        self.changeFilter()

    def initFields(self):
        """Resets all the editor values to a default value."""

        self.uiNewName.setText('Name')
        self.uiNewDescription.setPlainText('Description')
        self.uiNewComment.setPlainText('-')
        self.uiNewSeller.setText('-')
        self.uiNewLink.setPlainText('-')
        self.uiNewPriceUnit.setText('0')

        if self.uiCONCheck.isChecked():
            self.uiNewType.setText('Consumables')
        else:
            self.uiNewType.setText('Hardware')

        self.changeManufacture()

    def changeManufacture(self):
        """
        Changes the manufacture field based on the number of the component.

        INPUT:
            str - number: the number of the component
            QWidget - widgetPtr: the widget to change the value of
        """

        if self.prefix == 'MMH':
            self.uiNewManufacture.setText('Cut to length')
        else:
            self.uiNewManufacture.setText('Off the shelf')

    def changeFilter(self):
        """When called, scans the buttons and filters the selected cathegory of items in the view."""

        text = self.uiSearchEntry.text()
        textString = '.*(' + text.replace(' ', ').*(') + ')'
        self.checkFilters()
        filterString = '#' + self.prefix + '-[0-9A-Z]{3}' + textString

        self.proxyModel.setFilterRegExp(filterString)
        self.refreshView()

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
            'package': self.uiNewQuantityUnit.text(),
            'seller': self.uiNewSeller.text(),
            'kit': '',
            'link': self.uiNewLink.toPlainText()
        }

        typeDict = {
            'MEH': HardwareNode(data['number']),
            'ELH': HardwareNode(data['number']),
            'EMH': HardwareNode(data['number']),
            'MMH': MeasuredNode(data['number']),
            'CON': ConsumableNode(data['number'])
        }

        self.checkFilters()
        new = typeDict[self.prefix]
        new.addFeatures(**data)
        row = len(self.archive.rootItem.getChildren())

        self.archive.insertRows(row, new)

        self.updateNumber()

    def setCurrentSelection(self):
        """Updates the archive selection and enables the remove button."""

        self.uiRemoveButton.setDisabled(False)
        self.uiCurrentComponentEditor.setDisabled(False)

        self.currentSelection = self.selectionModel.selectedIndexes()
        self.current = self.proxyModel.mapToSource(self.selectionModel.currentIndex())

        parent = self.current.parent()

        self.mapper.setRootIndex(parent)
        self.mapper.setCurrentModelIndex(self.current)

        self.changeManufacture()

    def removeHardware(self):
        """Removes the selected item from the archive model."""

        if not self.currentSelection:
            return

        mapped = []

        for index in self.currentSelection:
            newIndex = self.proxyModel.mapToSource(index).siblingAtColumn(0)
            if newIndex not in mapped:
                mapped.append(newIndex)

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

    def checkFilters(self):
        """Checks the pushbuttons and changes the prefix accordingly."""

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
