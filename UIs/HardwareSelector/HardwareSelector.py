from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from ..ArchiveView.ArchiveView import ArchiveView

from .hardware_selector import Ui_uiHardwareSelector as ui

class HardwareSelector(qtw.QWidget, ui):

    submit = qtc.pyqtSignal(object)

    def __init__(self):
        """
        Loads the UI window, sets the manufacture model and connects the
        buttons to the event handler.
        """

        super(HardwareSelector, self).__init__()
        self.setupUi(self)

        self.archiveView = ArchiveView()
        self.uiArchiveView.layout().insertWidget(1, self.archiveView)

        self.model = None
        self.current = None

        self.uiCancelBtn.clicked.connect(self.close)
        self.uiOkBtn.clicked.connect(self.submitNode)

        self._enableSubmit()
        self.show()

    def setModel(self, model):
        """
        Sets this widgets' model.

        Args:
            model (ArchiveModel): this models' widget
        """

        self.model = model
        self.archiveView.setModel(self.model)

        self.selection = self.uiArchiveView.selectionModel()
        self.selection.currentChanged.connect(self._mapIndex)

    def submitNode(self):
        """
        Emits the currently selected node to add it to the tree.
        """

        self.submit.emit(self.currentNode)
        self.close()

    def _mapIndex(self, index):
        """
        The index is set as the current index of the editor.

        Args:
            index (QModelIndex): the index to update
        """

        self.current = index.internalPointer()
        self._enableSubmit()

    def _enableSubmit(self):
        if self.current:
            self.uiOkBtn.setDisabled(False)
        else:
            self.uiOkBtn.setDisabled(True)

# MAIN
if __name__ == '__main__':
    import sys
    app = qtw.QApplication(sys.argv)

    mw = HardwareSelector()
    mw.show()

    app.exec_()