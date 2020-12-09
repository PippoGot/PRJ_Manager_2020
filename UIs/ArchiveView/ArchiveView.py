from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from .archive_view import Ui_uiArchiveView as ui

class ArchiveView(qtw.QWidget, ui):

    indexChanged = qtc.pyqtSignal(qtc.QModelIndex)

    def __init__(self):
        """
        Loads the UI window and connects the buttons to the event handler.
        """

        super(ArchiveView, self).__init__()
        self.setupUi(self)

        self.model = None
        self.currentIndex = None
        self.indexSelection = None

        self.uiMEHBtn.clicked.connect(self._updateFilter)
        self.uiELHBtn.clicked.connect(self._updateFilter)
        self.uiEMHBtn.clicked.connect(self._updateFilter)
        self.uiMMHBtn.clicked.connect(self._updateFilter)
        self.uiPROBtn.clicked.connect(self._updateFilter)
        self.uiSearchEntry.textChanged.connect(self._updateFilter)

        self._refreshView()

    def setModel(self, model):
        """
        Sets this view model.

        Args:
            model (ArchiveModel): the model to visualize
        """

        self.model = model
        self.uiView.setModel(self.model)

        if self.model:
            self.selection = self.uiView.selectionModel()
            self.selection.currentChanged.connect(self._mapIndex)
            self._refreshView()

    def _updateFilter(self):
        self._refreshView()

    def _mapIndex(self, index):
        """
        Maps the index to the correct model and emits the current changed signal.

        Args:
            index (QModelIndes): the index to map
        """

        self.currentIndex = index
        self.indexSelection = self.selection.selectedIndexes()
        self.indexChanged.emit(self.currentIndex)
        self.update()

    def _refreshView(self):
        """
        Updates the view resizing the columns.
        """

        if self.model:
            for column in range(self.model.columnCount(qtc.QModelIndex())):
                self.uiView.resizeColumnToContents(column)

