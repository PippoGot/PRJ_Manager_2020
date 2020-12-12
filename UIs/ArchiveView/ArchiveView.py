from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from Models.ProxyArchive import ProxyArchive

from .archive_view import Ui_uiArchiveView as ui

class ArchiveView(qtw.QWidget, ui):
    """
    Widget for archive display and filtering. Offers a filter by type as well as
    by keywords, it displays the archive model in a table, showing the key elements only.
    """

    indexChanged = qtc.pyqtSignal(qtc.QModelIndex)
    selectionChanged = qtc.pyqtSignal(list)
    filterChanged = qtc.pyqtSignal(str)

    def __init__(self):
        """
        Loads the UI window and connects the buttons to the proper slots.
        """

        super(ArchiveView, self).__init__()
        self.setupUi(self)

        self.model = None
        self.proxy = ProxyArchive()
        self.currentIndex = None
        self.currentSelection = None

        self.uiMEHBtn.clicked.connect(self._updateFilter)
        self.uiELHBtn.clicked.connect(self._updateFilter)
        self.uiEMHBtn.clicked.connect(self._updateFilter)
        self.uiMMHBtn.clicked.connect(self._updateFilter)
        self.uiPROBtn.clicked.connect(self._updateFilter)
        self.uiSearchEntry.textChanged.connect(self._updateFilter)

        self.uiSearchEntry.addAction(qtg.QIcon(":/search.png"), qtw.QLineEdit.LeadingPosition)

        self._updateFilter()
        self._refreshView()

# --- MODEL ---

    def setModel(self, model):
        """
        Sets this view's model and the corresponding proxy model.

        Args:
            model (ArchiveModel): the model to visualize
        """

        self.model = model
        self.proxy.setSourceModel(self.model)
        self.uiView.setModel(self.proxy)

        self.proxy.sort(0, qtc.Qt.DescendingOrder)

        if self.model:
            self.selection = self.uiView.selectionModel()
            self.selection.currentChanged.connect(self._mapIndex)
            self.selection.currentChanged.connect(self._mapSelection)
            self._refreshView()

# --- SELECTION ---

    def _mapIndex(self, index):
        """
        Maps the index to the correct model and emits the current changed signal.

        Args:
            index (QModelIndes): the index to map
        """

        self.currentIndex = self.proxy.mapToSource(index)
        self.indexChanged.emit(self.currentIndex)

    def _mapSelection(self):
        """
        Maps the indexes to the correct model and emits the selection changed signal.
        """

        self.currentSelection = self.selection.selectedIndexes()

        tempIndexes = []
        for index in self.currentSelection:
            index = self.proxy.mapToSource(index)
            tempIndexes.append(index)

        self.currentSelection = tempIndexes

        self.selectionChanged.emit(self.currentSelection)

# --- UTILITY ---

    def _refreshView(self):
        """
        Updates the view resizing the columns.
        """

        if self.model:
            for column in range(self.model.columnCount(qtc.QModelIndex())):
                self.uiView.resizeColumnToContents(column)

    def _updateFilter(self):
        """
        Updates the current filter with the written keywords and the current selected
        prefix.
        """

        text = self.uiSearchEntry.text()
        textString = '.*(' + text.replace(' ', ').*(') + ')'

        prefix = self._getPrefix()
        self.filterChanged.emit(prefix)

        filterString = '#' + prefix + '-[0-9A-Z]{3}' + textString
        self.proxy.setFilterRegExp(filterString)

        self._refreshView()

    def _getPrefix(self):
        """
        Scans the buttons to determine the current selected prefix.

        Returns:
            str: the current selected prefix
        """

        if self.uiMEHBtn.isChecked(): return 'MEH'
        if self.uiMMHBtn.isChecked(): return 'MMH'
        if self.uiELHBtn.isChecked(): return 'ELH'
        if self.uiPROBtn.isChecked(): return 'PRO'
        if self.uiEMHBtn.isChecked(): return 'EMH'
