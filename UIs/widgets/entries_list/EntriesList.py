from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from .entries_list import Ui_entries_list as ui

class EntriesList(qtw.QWidget, ui):
    """
    Base widget for editing a list of entries. Used for the status and manufacture
    editor widgets.
    """

    entriesChanged = qtc.pyqtSignal(list)

    def __init__(self, entries = None):
        """
        Sets up the ui, creates the model and connects the signals to the slots.

        Args:
            entries (list[str]): the default entries list if any. Default to None.
        """

        super(EntriesList, self).__init__()
        self.setupUi(self)

        self.model = qtc.QStringListModel()
        self.uiList.setModel(self.model)

        if entries:
            self.model.setStringList(entries)

        self.uiAddBtn.clicked.connect(self._addItem)
        self.model.dataChanged.connect(self._emitEntries)
        self.uiList.customContextMenuRequested.connect(self._contextMenu)

    def _addItem(self):
        """
        Adds an entry to the model, then the line is cleared and the signal is emitted.
        """

        item = self.uiEntry.text()
        if item:
            strings = self.model.stringList()
            strings.append(item)
            self.model.setStringList(strings)

        self._clearLine()
        self._emitEntries()

    def _removeItem(self):
        """
        Removes an item from the model and emit the updated entries.
        """

        row = self.uiList.selectionModel().currentIndex().row()
        self.model.removeRow(row)

        self._emitEntries()

    def _clearLine(self):
        """
        Clears the lineedit.
        """

        self.uiEntry.clear()

    def _emitEntries(self):
        """
        Emits the current entries of the widget as a list of strings.
        """

        self.entriesChanged.emit(self.model.stringList())

    def _contextMenu(self, position):
        """
        Creates the context menu when an item is selected and adds the remove action.

        Args:
            position (?): the position of the menu
        """

        menu = qtw.QMenu()
        removeAction = qtw.QAction('Remove')
        removeAction.triggered.connect(self._removeItem)

        current = self.uiList.selectionModel().currentIndex().row()

        if current >= 0:
            menu.addAction(removeAction)
            menu.exec_(self.uiList.viewport().mapToGlobal(position))

    def setEntries(self, entries):
        """
        Reads a list of strings and sets them as current entries in the list view and model.

        Args:
            entries (list[str]): the list of strings to set as entries.
        """

        self.model.setStringList(entries)
