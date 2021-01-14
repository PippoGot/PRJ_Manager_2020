from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import os

from ProxyHardware import HardwareProxyModel
from BaseNode import BaseNode

import resources

from ui_hardware_selector import Ui_uiHardwareEditor as ui

class HardwareSelector(qtw.QWidget, ui):
    """
    This class is a popup window for inserting hardware components into the list.
    Has a filter to filter out the different hadware and component type.
    Emits the signal containing all the data when a component needs to be added.
    """

    submit = qtc.pyqtSignal(BaseNode)

    def __init__(self, archive):
        """
        Loads the UI window, connects the buttons to the respective functions,
        sets the widgets models for the views and finally refreshes the views.

        Custom functions:
            self.changeFilter()

        Args:
            archive (ModelHardware): model of the hardware archive.
        """

        super(HardwareSelector, self).__init__()
        self.setupUi(self)

        self.uiOkButton.setDisabled(True)

        self.uiCancelButton.clicked.connect(self.close)
        self.uiOkButton.clicked.connect(self.onSubmit)

        self.uiSearchEntry.addAction(qtg.QIcon(":/search.png"), qtw.QLineEdit.LeadingPosition)

        self.uiMechanicalButton.clicked.connect(self.changeFilter)
        self.uiMeasuredButton.clicked.connect(self.changeFilter)
        self.uiElectricalButton.clicked.connect(self.changeFilter)
        self.uiElectromechanicalButton.clicked.connect(self.changeFilter)
        self.uiConsumableButton.clicked.connect(self.changeFilter)
        self.uiSearchEntry.textChanged.connect(self.changeFilter)

        self.current = None
        self.currentSelection = None

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

    def changeFilter(self):
        """
        When called, scans the buttons and filters the selected category of items in the view.

        Custom functions:
            self.chekFilters()
            self.refreshView()
        """

        text = self.uiSearchEntry.text()
        textString = '.*(' + text.replace(' ', ').*(') + ')'
        prefix = self.checkFilters()
        filterString = '#' + prefix + '-[0-9A-Z]{3}' + textString

        self.proxyModel.setFilterRegExp(filterString)
        self.refreshView()

    def setCurrentSelection(self):
        """Updates the archive selection."""

        self.currentSelection = self.selectionModel.selectedIndexes()

    def setCurrentIndex(self, index):
        """
        Updates the current selected item.

        Args:
            index (QModelIndex): the index of the current selected item.
        """

        self.current = index
        self.uiOkButton.setDisabled(False)

    def onSubmit(self):
        """
        Emits a signal with the current selected item.
        If more than one item is selected the user is notified by a dialog box, and asked to
        select only one item.

        Custom functions:
            BaseNode.copy()
            BaseNode.addFeatures()
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
            node = index.internalPointer()
            newComponent = node.copy()
            newComponent.addFeatures(quantity = self.uiSelectQuantity.text())

            self.submit.emit(newComponent)
            self.close()

    def refreshView(self):
        """Updates the view resizing the columns to the content."""

        for column in range(self.model.columnCount(qtc.QModelIndex())):
            if column != self.model.columnCount(qtc.QModelIndex()):
                self.uiHardwareView.resizeColumnToContents(column)
        self.uiHardwareView.horizontalHeader().setStretchLastSection(True)

    def checkFilters(self):
        """
        Checks the pushbuttons and returns the correspondinf prefix.

        Returns:
            str: the current selected category prefix.
        """

        if self.uiMechanicalButton.isChecked():
            prefix = 'MEH'
        elif self.uiMeasuredButton.isChecked():
            prefix = 'MMH'
        elif self.uiElectricalButton.isChecked():
            prefix = 'ELH'
        elif self.uiConsumableButton.isChecked():
            prefix = 'CON'
        else:
            prefix = 'EMH'

        return prefix