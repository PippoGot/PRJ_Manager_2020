from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import json

from ...widgets.entries_list.EntriesList import EntriesList
from ...widgets.file_selector.FileSelector import FileSelector

from .settings_window import Ui_settings_window as ui

class SettingsWindow(qtw.QWidget, ui):

    archivePathChanged = qtc.pyqtSignal(str)
    recentFileAdded = qtc.pyqtSignal(str)

# INIT

    def __init__(self):
        """
        Sets up the ui, then looks for the settings file. If the file does not exist
        a default one is created. Otherwise the existing one is read. Then all the custom
        widgets are added to the layout and initialised.
        """

        # ui
        super(SettingsWindow, self).__init__()
        self.setupUi(self)

        # reads settings file
        self.data = {}
        self._checkSettings()
        self._checkArchive(self.archivePath)

        # signals-slots connections of the ui
        self.uiOkBtn.clicked.connect(self.close)
        self.uiImportBtn.clicked.connect(self._importSettings)
        self.uiExportBtn.clicked.connect(self._exportSettings)

        # archive path section init
        self.archiveSelector = FileSelector(details = 'Path', path = self.archivePath)
        self.uiArchiveBox.layout().addWidget(self.archiveSelector)
        self.archiveSelector.pathChanged.connect(self._updateArchivePath)

        # status editor section init
        self.statusEditor = EntriesList(self.statusEntries)
        self.uiStatusBox.layout().addWidget(self.statusEditor)
        self.statusEditor.entriesChanged.connect(self._updateStatusEntries)

        # manufacture editor section init
        self.manufactureEditor = EntriesList(self.manufactureEntries)
        self.uiManufactureBox.layout().addWidget(self.manufactureEditor)
        self.manufactureEditor.entriesChanged.connect(self._updateManufactureEntries)

# RECENT FILES

    def addRecentFile(self, filename):
        """
        Adds a new filename to the list then checks the list length. If a name is
        already in the list it's moved to the front, otherwise the new filename is
        inserted in the front.

        Args:
            filename (str): the new filename
        """

        if filename in self.recentFiles:
            self.recentFiles.pop(self.recentFiles.index(filename))
        self.recentFiles.insert(0, filename)

        self._checkOpening()
        self._checkLength()
        self._saveSettings()
        self.recentFileAdded.emit(filename)

    def _checkLength(self):
        """
        Checks the length of the recent files list and removes the older ones.
        """

        length = len(self.recentFiles)
        if length > 5:
            for _ in range(length - 5):
                self.recentFiles.pop(-1)

    def _checkOpening(self):
        """
        Checks if the filenames in the recent files list can be opened. If not they are
        removed from the list.
        """

        notFoundList = []
        for file in self.recentFiles:
            try:
                with open(file, 'r') as _: pass
            except FileNotFoundError:
                notFoundList.append(file)
        for file in notFoundList:
            self.recentFiles.remove(file)

    def getRecentFilesList(self):
        """
        Returns the list of strings of the recent files.

        Returns:
            list[str]: the list with the recent files
        """

        self._checkOpening()
        return self.data['recentFiles']

# UPDATING

    def _initRecentFiles(self, files):
        """
        Updates the recent files list and saves the settings.

        Args:
            files (list[str]): the paths of the recent files
        """

        self.recentFiles = files
        self.data['recentFiles'] = self.recentFiles

        self._saveSettings()

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

# GETTERS

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

# ACTIVATORS

    def activateArchivePathChanged(self):
        """
        Emits the corresponding signal.
        """

        self.archivePathChanged.emit(self.archivePath)

# FILE MANAGEMENT

    def _checkSettings(self):
        """
        Checks if the settings file is in the right location, otherwise a new one
        is initialized.
        """

        try:
            self._importSettings('settings.json')
        except FileNotFoundError:
            self._initSettings()

    def _initSettings(self):
        """
        Sets the default settings if a file is not present.
        """

        self.data = {
            'archivePath': 'HardwareArchive.json',
            'statusEntries': [],
            'manufactureEntries': [],
            'recentFiles': []
        }

        with open('settings.json', 'w') as file:
            json.dump(self.data, file)

        self._updateArchivePath('HardwareArchive.json')
        self._updateStatusEntries([])
        self._updateManufactureEntries([])
        self._initRecentFiles([])

    def _checkArchive(self, archivePath):
        """
        Checks if the archive exists in the specified location, if not the archive is
        reinitialized

        Args:
            archivePath (str): the filename of the archive to check
        """

        try:
            with open(archivePath, 'r') as _:
                pass
        except FileNotFoundError:
            self._initArchive()

    def _initArchive(self):
        """
        Initialises a new archive file.
        """

        with open(self.archivePath, 'w') as file:
            root = {
                "class": "ProjectNode",
                "ID": "#000-000",
                "name": "Name",
                "description": "Description",
                "comment": "",
                "packageQuantity": 1,
                "quantity": 1,
                "price": 0.0,
                "type": "Project",
                "manufacture": "Assembled",
                "status": "Not Designed",
                "seller": None,
                "link": None,
                "children": []
            }

            json.dump(root, file, indent = 4)

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
            self._initRecentFiles(data.get('recentFiles'))

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

    def _saveSettings(self):
        """
        Saves the current settings in a json file.
        """

        self._exportSettings('settings.json')
