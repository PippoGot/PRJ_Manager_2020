from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from ..ArchiveView.ArchiveView import ArchiveView

from .hardware_selector import Ui_uiHardwareSelector as ui

class HardwareSelector(qtw.QWidget, ui):
    """
    Popup window to select and add a special component node from the archive.
    Uses the ArchiveView widget.
    """

    submit = qtc.pyqtSignal(object)

    def __init__(self):
        """
        Loads the UI window and connects the buttons to the event handler.
        """

        super(HardwareSelector, self).__init__()
        self.setupUi(self)

        self.archiveView = ArchiveView()
        self.uiArchiveView.layout().insertWidget(1, self.archiveView)
        self.archiveView.uiView.setSelectionMode(qtw.QAbstractItemView.SingleSelection)

        self.model = None
        self.currentNode = None

        self.uiCancelBtn.clicked.connect(self.close)
        self.uiOkBtn.clicked.connect(self.submitNode)

        self._enableSubmit()
        self.show()

# --- MODELS ---

    def setModel(self, model):
        """
        Sets this widget's model.

        Args:
            model (ArchiveModel): this widget's model
        """

        self.model = model
        self.archiveView.setModel(self.model)

        if self.model:
            self.archiveView.indexChanged.connect(self._mapIndex)

# --- NODE EMIT ---

    def submitNode(self):
        """
        Emits the currently selected node to add it to the tree.
        """

        self.currentNode.addFeatures(quantity = self.uiQuantity.text())

        self.submit.emit(self.currentNode)
        self.close()

# --- SELECTION ---

    def _mapIndex(self, index):
        """
        The index is set as the current index of the editor.

        Args:
            index (QModelIndex): the index to update
        """

        self.currentNode = index.internalPointer()
        self._enableSubmit()

# --- UTILITY ---

    def _enableSubmit(self):
        """
        Enables or disables the submit button based on the current selection.
        """

        if self.currentNode:
            self.uiOkBtn.setDisabled(False)
        else:
            self.uiOkBtn.setDisabled(True)
