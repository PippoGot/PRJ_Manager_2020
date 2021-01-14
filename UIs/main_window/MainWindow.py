# --- IMPORTS ---
# LIBRARIES
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import os

from data_types.UndoStack import UndoStack

# MODELS
from models.tree.Model import TreeModel
from models.archive.Model import ArchiveModel

# POPUPS
from ..popups.settings_window.SettingsWindow import SettingsWindow

# PAGES
from ..pages.components_page.ComponentsPage import ComponentsPage
from ..pages.archive_page.ArchivePage import ArchivePage

# RESOURCES
from .. import resources_rc
from . import decorators as decor
from . import dialogs
from ..stylesheet import stylesheet as qss

# UI
from .main_window import Ui_uiMainWindow as ui

# --- CLASS ---

class MainWindow(qtw.QMainWindow, ui):
    def __init__(self, application):
        """
        Loads the UI window and set the manufacture model.
        """

# ui
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.application = application
        self.application.setStyleSheet(qss)

# undo stack init
        self.unsavedChanges = False
        self.undoStack = UndoStack()

# settings window init
        self.settingsWindow = SettingsWindow()
        self.statusModel = self.settingsWindow.getStatusModel()
        self.manufactureModel = self.settingsWindow.getManufactureModel()

# components page init
        self.componentsPage = ComponentsPage()
        self.ComponentsPage.layout().addWidget(self.componentsPage)

        self.componentsPage.setManufactureModel(self.manufactureModel)
        self.componentsPage.setStatusModel(self.statusModel)

        self.componentsPage.uiView.customContextMenuRequested.connect(self._rightClickMenu)
        self.componentsPage.fileSaved.connect(self.settingsWindow.addRecentFile)
        self.componentsPage.nodeAdded.connect(self._undoable)
        self.componentsPage.nodeAdded.connect(self._producesChanges)

        self._openLatest()
        self._updateRecentFilesMenu()
        self.settingsWindow.recentFileAdded.connect(self._updateRecentFilesMenu)

# archive page init
        self.archivePage = ArchivePage()
        self.ArchivePage.layout().addWidget(self.archivePage)

        self.archivePage.setManufactureModel(self.manufactureModel)
        self.archivePage.setStatusModel(self.statusModel)

        self.settingsWindow.archivePathChanged.connect(self.archivePage.readArchive)
        self.settingsWindow.activateArchivePathChanged()

# file menu actions connections
        self.uiActNew.triggered.connect(self.newFile)
        self.uiActOpen.triggered.connect(self.openFile)
        self.uiActSave.triggered.connect(self.saveFile)
        self.uiActSaveas.triggered.connect(self.saveFileAs)
        self.uiActExportBill.triggered.connect(self.exportBill)
        self.uiActClear.triggered.connect(self.clearFile)

        self.uiActSettings.triggered.connect(self.openSettings)

# edit menu actions connections
        self.uiActAddAssembly.triggered.connect(self.addNode)
        self.uiActAddAssembly.setData('AssemblyNode')
        self.uiActAddPart.triggered.connect(self.addNode)
        self.uiActAddPart.setData('LeafNode')
        self.uiActAddSpecial.triggered.connect(self.addSpecialNode)
        self.uiActAddJig.triggered.connect(self.addNode)
        self.uiActAddJig.setData('JigNode')
        self.uiActAddPlaceholder.triggered.connect(self.addNode)
        self.uiActAddPlaceholder.setData('PlaceholderNode')

        self.uiActRemove.triggered.connect(self.removeComponent)
        self.uiActMorph.triggered.connect(self.morphComponent)
        self.uiActUpdate.triggered.connect(self.updateSpecialComponents)

        self.uiActCut.triggered.connect(self.cut)
        self.uiActCopy.triggered.connect(self.copy)
        self.uiActPaste.triggered.connect(self.paste)
        self.uiActUndo.triggered.connect(self.undo)
        self.uiActRedo.triggered.connect(self.redo)

# view menu actions connections
        self.uiActDeprecated.triggered.connect(self.hideDeprecated)
        self.uiActExpandAll.triggered.connect(self.expandAll)
        self.uiActExpandOne.triggered.connect(self.expandOne)
        self.uiActCollapseOne.triggered.connect(self.collapseOne)

# --- FILE MENU FUNCTIONS ---

    @decor.askSave
    def newFile(self, *args):
        """
        Creates a new model for a new file. When a new file is created the page
        index is set to the components page.
        """

        self.componentsPage.resetModel()
        self.tabWidget.setCurrentIndex(0)

    @decor.askSave
    def openFile(self, filename = None, *args):
        """
        Opens a file given it's name or path.
        """

        if not filename:
            filename = dialogs.openDialog()

        if filename:
            try:
                self.componentsPage.resetModel()
                self.componentsPage.readModel(filename)
                self.settingsWindow.addRecentFile(filename)
                self.tabWidget.setCurrentIndex(0)
            except Exception:
                dialogs.fileReadError()

    @decor.ifHasModel
    def saveFile(self, *args):
        """
        Saves a file given it's name or path. Otherwise the filename is asked
        to the user.
        """

        if self.componentsPage.saveModel(): self.unsavedChanges = False

    @decor.ifHasModel
    def saveFileAs(self, *args):
        """
        Saves a file with a new name.
        """

        if self.componentsPage.saveModelAs(): self.unsavedChanges = False

    def exportBill(self, *args):
        pass

    @decor.askSave
    def clearFile(self, *args):
        """
        Clears the current model.
        """

        self.componentsPage.clearModel()

    def openSettings(self):
        """
        Opens the settings window.
        """

        self.settingsWindow.show()

# --- EDIT MENU FUNCTIONS ---

    @decor.ifNotLeaf
    def addNode(self, *args):
        """
        Adds a new node based on the sender function.
        """

        action = self.sender()
        tp = action.data()
        self.componentsPage.prepareNode(tp)

    @decor.ifNotLeaf
    def addSpecialNode(self, *args):
        """
        Adds a special node, either hardware or product.
        """

        self.selector = self.archivePage.getSelector()
        self.selector.submit.connect(self.componentsPage.addNode)

    @decor.ifNotRoot
    @decor.undoableAction
    def removeComponent(self, *args):
        """
        Removes a component node that is not at level 1.

        Returns:
            ComponentNode: the removed node
        """

        return self.componentsPage.removeNode()

    @decor.ifLeaf
    @decor.ifIsHardware
    def morphComponent(self, *args):
        """
        Swaps two archive components in the component tree model.
        """

        self.selector = self.archivePage.getSelector()
        self.selector.submit.connect(self.componentsPage.swapNode)

    @decor.componentsAction
    @decor.ifHasModel
    @decor.undoableAction
    def updateSpecialComponents(self, *args):
        """
        Updates all of the components in the tree model with data of the archive model.
        """

        archiveNodes = self.archivePage.getNodes()
        self.componentsPage.updateSpecialNodes(archiveNodes)

    @decor.ifNotRoot
    @decor.undoableAction
    def cut(self, *args):
        """
        Removes and stores a component for later pasting.
        """

        self.componentsPage.cutNode()

    @decor.ifNotRoot
    def copy(self, *args):
        """
        Copies a node with it's children to paste it in other nodes.
        """

        self.componentsPage.copyNode()

    @decor.ifNotLeaf
    @decor.undoableAction
    def paste(self, *args):
        """
        Insert the copied or cut node in the currently selected node.
        """

        self.componentsPage.pasteNode()

    @decor.componentsAction
    @decor.producesChanges
    def undo(self, *args):
        """
        Undo the current action.
        """

        string = self.undoStack.undo()
        self.componentsPage.readJsonString(string)

    @decor.componentsAction
    @decor.producesChanges
    def redo(self, *args):
        """
        Redo the currently undone action.
        """

        string = self.undoStack.redo()
        self.componentsPage.readJsonString(string)

# --- VIEW MENU FUNCTIONS ---

    @decor.ifHasModel
    def hideDeprecated(self, *args):
        """
        Hides or shows the deprecated nodes in the tree view.
        """

        if self.uiActDeprecated.isChecked():
            self.componentsPage.hideDeprecated(True)
        else:
            self.componentsPage.hideDeprecated(False)

    @decor.ifHasModel
    def expandAll(self, *args):
        """
        Expands all of the items in the view.
        """

        self.componentsPage.expandAll()

    @decor.ifHasModel
    def expandOne(self, *args):
        """
        Expands the current lowest level of items in the tree.
        """

        self.componentsPage.expandOne()

    @decor.ifHasModel
    def collapseOne(self, *args):
        """
        Collapses the lowest level currently expanded in the tree.
        """

        self.componentsPage.collapseOne()

# --- PRIVATE UTILITY FUNCTIONS ---

# UNDO and CHANGES

    @decor.producesChanges
    def _producesChanges(self, *args):
        """
        Sets the unsaved changes variable to true. Used in functions that cannot
        use the corresponding decorator.
        """

        pass

    @decor.undoable
    def _undoable(self, *args):
        """
        Saves a snapshot of the current file. Used in functions that cannot
        use the corresponding decorator.
        """

        pass

# DIALOGS and MENUS

    def _rightClickMenu(self, position):
        """
        Creates the context menu in the components view when the right click is pressed.

        Args:
            position (?): the position of the cursor on the screen.
        """

        index = self.componentsPage.getCurrentIndex()

        separator = qtw.QAction()
        separator.setSeparator(True)
        menu = qtw.QMenu()

        if index:
            node = index.internalPointer()
            level = node.getLevel()

            if level < 5:
                menu.addAction(self.uiActAddAssembly)
                menu.addAction(self.uiActAddSpecial)
                menu.addAction(self.uiActAddPart)
                menu.addAction(self.uiActAddJig)
                menu.addAction(self.uiActAddPlaceholder)
                menu.addAction(separator)

            if node.getFeature('type') == 'Hardware':
                menu.addAction(self.uiActMorph)
                menu.addAction(separator)

            if level > 1:
                menu.addAction(self.uiActRemove)

            menu.exec_(self.componentsPage.uiView.viewport().mapToGlobal(position))

    def _updateRecentFilesMenu(self):
        """
        Updates the recent files menu with the latest files.
        """

        recentFiles = self.settingsWindow.getRecentFilesList()
        self.recentFilesMenu = qtw.QMenu('Recent Files...', self)
        for file in recentFiles:
            name = file.split('/')[-1]
            action = qtw.QAction(name, self)
            self.recentFilesMenu.addAction(action)
            action.setData(file)
            action.triggered.connect(self._openRecent)
        self.menuFile.insertMenu(self.uiActClear, self.recentFilesMenu)

    def _checkPage(self, page):
        """
        Checks if the user is in the correct page and notify with a dialog if it's not.

        Args:
            page (int): the page to check for.

        Returns:
            bool: whether the user is in the correct page or not.
        """

        if self.tabWidget.currentIndex() != page:
            dialogs.pageError()
            return True
        return False

# RECENT FILE OPENING

    def _openRecent(self):
        """
        Opens a recent file based on the filename inside the calling action.
        """

        action = self.sender()
        if action:
            self.openFile(action.data())

    def _openLatest(self):
        """
        Opens the most recent file if it exists, otherwise starts a new model and saves the
        changes to the undo stack.
        """

        recentFiles = self.settingsWindow.getRecentFilesList()
        filename = None
        if recentFiles:
            filename = recentFiles[0]

        self.componentsPage.readModel(filename)
        self.undoStack.addSnapshot(str(self.componentsPage.getModel()), 'init')
