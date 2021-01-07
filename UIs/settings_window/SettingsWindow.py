from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import json

from ..widgets.entries_list.EntriesList import EntriesList
from ..widgets.file_selector.FileSelector import FileSelector

from .settings_window import Ui_settings_window as ui

class SettingsWindow(qtw.QWidget, ui):

    archivePathChanged = qtc.pyqtSignal(str)

    def __init__(self):
        """
        Sets up the ui, then looks for the settings file. If the file does not exist
        a default one is created. Otherwise the existing one is read. Then all the custom
        widgets are added to the layout and initialised.
        """

        super(SettingsWindow, self).__init__()
        self.setupUi(self)

        self.data = {}
        try:
            self._importSettings('settings.json')
        except FileNotFoundError:
            self.data = self._defaultSettings()

        self.uiOkBtn.clicked.connect(self.close)
        self.uiImportBtn.clicked.connect(self._importSettings)
        self.uiExportBtn.clicked.connect(self._exportSettings)

        self.archiveSelector = FileSelector(details = 'Path', path = self.archivePath)
        self.uiArchiveBox.layout().addWidget(self.archiveSelector)
        self.archiveSelector.pathChanged.connect(self._updateArchivePath)

        self.statusEditor = EntriesList(self.statusEntries)
        self.uiStatusBox.layout().addWidget(self.statusEditor)
        self.statusEditor.entriesChanged.connect(self._updateStatusEntries)

        self.manufactureEditor = EntriesList(self.manufactureEntries)
        self.uiManufactureBox.layout().addWidget(self.manufactureEditor)
        self.manufactureEditor.entriesChanged.connect(self._updateManufactureEntries)

    def _defaultSettings(self):
        """
        Sets the default settings if a file is not present.

        Returns:
            dict[str, PyObject]: the dictionary with the default settings
        """

        data = {
            'archivePath': None,
            'statusEntries': [],
            'manufactureEntries': [],
            'recentFiles': []
        }

        with open('settings.json', 'w') as file:
            json.dump(data, file)

        self._updateArchivePath(None)
        self._updateStatusEntries([])
        self._updateManufactureEntries([])
        return data

    def _updateArchivePath(self, path):
        """
        Updates the archive path and saves the settings.

        Args:
            path (str): the path of the file
        """

        self.archivePath = path
        self.data['archivePath'] = self.archivePath

        self._saveSettings()
        self.archivePathChanged.emit(self.archivePath)

    def _updateStatusEntries(self, entries):
        """
        Updates the status entries and saves the settings.

        Args:
            entries (list[str]): the list of entries
        """

        self.statusEntries = entries
        self.data['statusEntries'] = self.statusEntries

        self._saveSettings()

    def _updateManufactureEntries(self, entries):
        """
        Updates the manufacture entries and saves the settings.

        Args:
            entries (list[str]): the list of entries
        """

        self.manufactureEntries = entries
        self.data['manufactureEntries'] = self.manufactureEntries

        self._saveSettings()

    def _saveSettings(self):
        """
        Saves the current settings in a json file.
        """

        self._exportSettings('settings.json')

    def getStatusModel(self):
        """
        Returns the model of the status editor.

        Returns:
            QStringListModel: the model with the status entries
        """

        return self.statusEditor.model

    def getManufactureModel(self):
        """
        Returns the model of the manufacture editor.

        Returns:
            QStringListModel: the model with the manufacture entries
        """

        return self.manufactureEditor.model

    def _importSettings(self, filename = None):
        """
        Opens a popup to browse for a json file, if one is selected the settings are copied.

        Args:
            filename (str): the path of the file. Default to None.
        """

        if not filename:
            filename, _ = qtw.QFileDialog.getOpenFileName(
                self,
                "Select a file to open...",
                qtc.QDir.homePath(),
                'JSON Documents (*.json) ;; All Files (*)',
                'JSON Documents (*.json)'
            )

        if filename:
            with open(filename, 'r') as file:
                data = json.load(file)

            self._updateArchivePath(data.get('archivePath'))
            self._updateStatusEntries(data.get('statusEntries'))
            self._updateManufactureEntries(data.get('manufactureEntries'))

    def _exportSettings(self, filename = None):
        """
        Saves a settings file with a new name.

        Args:
            filename (str): the path of the file. Default to None.
        """

        if not filename:
            filename, _ = qtw.QFileDialog.getSaveFileName(
                self,
                "Select the file to save to...",
                qtc.QDir.homePath(),
                'JSON Documents (*.json)'
            )

        if filename:
            with open(filename, 'w') as file:
                json.dump(self.data, file, indent = 4)
