from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from .file_selector import Ui_file_selector as ui

class FileSelector(qtw.QWidget, ui):
    """
    This class is a file browser, the path of a file is stored in a line edit that can
    be edited by browsing for a file or by changing it manually. Every time the path
    changes the new path is emitted.
    """

    pathChanged = qtc.pyqtSignal(str)

    def __init__(self, details = None, path = None):
        """
        Sets up the ui and connects the signals to the slots. If a details value is given
        the widget label is set as that value.

        Args:
            details (str): the value of the label. Defaults to None.
            path (str): the default value of the line edit if any. Default to None.
        """

        super(FileSelector, self).__init__()
        self.setupUi(self)

        if details:
            self.uiDetails.setText(details)
        if path:
            self.setPath(path)

        self.uiBrowseBtn.clicked.connect(self._browse)
        self.uiPath.textChanged.connect(self._emitPathChanged)

    def setPath(self, path):
        """
        Sets the line edit text as the selected file path, then emits the path.

        Args:
            path (str): the path of the selected file
        """

        self.uiPath.setText(path)

    def _browse(self):
        """
        Opens a popup to browse for a json file, if one is selected the path is updated.
        """

        filename, _ = qtw.QFileDialog.getOpenFileName(
            self,
            "Select a file to open...",
            qtc.QDir.homePath(),
            'JSON Documents (*.json) ;; All Files (*)',
            'JSON Documents (*.json)'
        )

        if filename:
            self.setPath(filename)

    def _emitPathChanged(self):
        """
        Emits the current text of the line edit.
        """

        self.pathChanged.emit(self.uiPath.text())
