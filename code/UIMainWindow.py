from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from UIComponentsPage import TreeEditor
from UIComponentEditor import PropEditor
from UIHardwareSelector import HardwareSelector
from UIHardwareEditor import HardwareEditor
from ModelHardware import HardwareModel
from ModelTreeETE import ModelTree
from ModelCombobox import ModelCombobox

class MainWindow(qtw.QMainWindow):
    """
    Class for the main UI and the actions functions. This class manage every action that can 
    be performed in the application.
    """

    def __init__(self):
        """
        Loads the .ui file, creates the models from the archive and the central widget,
        then connects the menu actions to the respective functions.
        """

        super(MainWindow, self).__init__()                                              # superclass constructor
        
        uic.loadUi('D:/Data/_PROGETTI/Apps/PRJ_Manager/UIs/ui_main_window.ui', self)        # loads the UI from the .ui file

        self.filename = None                                                            # initialize the filename to None
        self.archive = HardwareModel()                                                  # creates the models from the archive and stores them in a class parameter
        # self.classes = ModelCombobox('D:/Data/_PROGETTI/Apps/PRJ_Manager/archive/classes.csv')
        # self.materials = ModelCombobox('D:/Data/_PROGETTI/Apps/PRJ_Manager/archive/materials.csv')
        # self.statuses = ModelCombobox('D:/Data/_PROGETTI/Apps/PRJ_Manager/archive/statuses.csv')
        self.model = None                                                               # the model class parameter is set to None

        self.treeEditor = TreeEditor()                                                  # creates the tree editor
        self.uiTreePage.layout().addWidget(self.treeEditor)

        self.hardwareEditor = HardwareEditor(self.archive)                              # creates the hardware editor
        self.uiHardwarePage.layout().addWidget(self.hardwareEditor)

        self.uiActionNew.triggered.connect(self.newFile)                                # connects the actions to their respective functions
        self.uiActionOpen.triggered.connect(self.openFile)
        self.uiActionSave.triggered.connect(self.saveFile)
        self.uiActionSaveAs.triggered.connect(self.saveAsFile)
        self.uiActionClear.triggered.connect(self.clearFile)
        # self.uiActionExportBOM.triggered.connect(self.exportBOM)

        self.uiActionAddComponent.triggered.connect(self.addComponent)
        self.uiActionAddSpecialComponent.triggered.connect(self.addSpecialComponent)
        self.uiActionAddLeafComponent.triggered.connect(self.addLeafComponent)
        self.uiActionMorphSpecialComponent.triggered.connect(self.morphSpecialComponent)
        self.uiActionUpdateSpecialComponents.triggered.connect(self.updateSpecialComponents)
        self.uiActionRemoveComponent.triggered.connect(self.removeComponent)

        self.uiActionHideDeprecated.triggered.connect(self.hideDeprecated)

        self.showMaximized()                                                             # finally shows the window

# ACTION FUNCTIONS
# file menu

    def newFile(self):
        """Creates a new model, for a new file."""

        if not self.filename and self.model:                                            # if another file is open and not saved
            self.msgBox = qtw.QMessageBox.warning(                                      # creates a message box to ask the user if the file needs to be saved
                self, 
                'File not saved...', 
                'Save changes to current file?', 
                qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel, 
                qtw.QMessageBox.Yes
            )

            if self.msgBox == qtw.QMessageBox.Yes:                                      # if the answer is yes
                self.saveFile()                                                         # it opens a popup window to save it first
            elif self.msgBox == qtw.QMessageBox.Cancel:
                return

        self.model = ModelTree()                                                        # the model parameter is updated with the new model created
        self.treeEditor.setModel(self.model)                                            # and passed to the central widget
        # self.uiBillView.setModel(self.model.bill)
        self.filename = None                                                            # then the filename is reset
        # self.refreshBillView()

    def openFile(self):
        """Opens and read a .csv file, then creates the corresponding model."""

        if not self.filename and self.model:                                            # if another file is open and not saved
            self.msgBox = qtw.QMessageBox.warning(                                      # creates a message box to ask the user if the file needs to be saved
                self, 
                'File not saved...', 
                'Save changes to current file?', 
                qtw.QMessageBox.Yes | qtw.QMessageBox.No, 
                qtw.QMessageBox.Yes
            )

            if self.msgBox == qtw.QMessageBox.Yes:                                      # if the answer is yes
                self.saveFile()                                                         # it opens a popup window to save it first

        filename, _ = qtw.QFileDialog.getOpenFileName(                                  # then opens up a popup window to get the filename to open
            self, 
            "Select a file to open...", 
            qtc.QDir.homePath(), 
            'CSV Documents (*.csv) ;; All Files (*)', 
            'CSV Documents (*.csv)'
        )

        if filename:                                                                    # if a filename is picked
            try:                                                                        # tries to read the model inside it
                self.model = ModelTree(filename)
                self.treeEditor.setModel(self.model)
                # self.uiBillView.setModel(self.model.bill)
                # self.refreshBillView()
                self.filename = filename
                self.treeEditor.refreshView()

            except Exception as e:                                                      # if a problem during the process occurs a message box is created
                self.msgBox = qtw.QMessageBox.critical(                                 # informing the user of the problem
                    self, 
                    'Critical Error!', 
                    f'Could not open the file at {filename}\nbecause "{e}" exception occurred!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )

    def saveFile(self):
        """Saves the current file."""

        if self.model:                                                                  # if a model is present to be saved
            if self.filename:                                                           # if a filename is present
                self.model.saveFile(self.filename)                                      # it saves the current file with this filename
                self.classes.saveModel()
                self.materials.saveModel()
                self.statuses.saveModel()
            else:                                                                       # otherwise
                self.saveAsFile()                                                       # it calls the saveAsFile() function

        else:                                                                           # if a model is not present
            self.msgBox = qtw.QMessageBox.warning(                                      # the user is notified
                self, 
                'Warning!', 
                'No file currently open.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

    def saveAsFile(self):
        """Saves the file with a different filename from the original, or a new file."""

        if self.model:                                                                  # if a model is present to be saved
            filename, _ = qtw.QFileDialog.getSaveFileName(                              # opens up a popup window to select the destination folder
                self, 
                "Select the file to save to...", 
                qtc.QDir.homePath(),
                'CSV Documents (*.csv)'
            )

            if filename:                                                                # then if a filename is given
                try:
                    self.model.saveFile(filename)                                       # the file is saved
                    self.classes.saveModel()
                    self.materials.saveModel()
                    self.statuses.saveModel()

                except Exception as e:                                                  # if a problem occurs during the operation a message box is shown
                        self.msgBox = qtw.QMessageBox.critical(                         # informing the user of the problem
                        self, 
                        'Critical Error!', 
                        f'Could not save the file at {filename}\nbecause "{e}" exception occurred!', 
                        qtw.QMessageBox.Ok, 
                        qtw.QMessageBox.Ok
                    )          

                self.filename = filename                                                    # then the filename parameter is updated

        else:                                                                           # if a model is not present
            self.msgBox = qtw.QMessageBox.warning(                                      # the user is notified
                self, 
                'Warning!', 
                'No file currently open.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

    # def exportBOM(self):
    #     if self.model:
    #         filename, _ = qtw.QFileDialog.getSaveFileName(                              # opens up a popup window to select the destination folder
    #             self, 
    #             "Select the file to save to...", 
    #             qtc.QDir.homePath(),
    #             'CSV Documents (*.csv)'
    #         )

    #         if filename:                                                                # then if a filename is given
    #             try:
    #                 self.model.bill.exportBill(filename)                                       # the file is saved
    #                 self.classes.saveModel()
    #                 self.materials.saveModel()
    #                 self.statuses.saveModel()

    #             except Exception as e:                                                  # if a problem occurs during the operation a message box is shown
    #                     self.msgBox = qtw.QMessageBox.critical(                         # informing the user of the problem
    #                     self, 
    #                     'Critical Error!', 
    #                     f'Could not save the file at {filename}\nbecause "{e}" exception occurred!', 
    #                     qtw.QMessageBox.Ok, 
    #                     qtw.QMessageBox.Ok
    #                 )          

    #     else:                                                                           # if a model is not present
    #         self.msgBox = qtw.QMessageBox.warning(                                      # the user is notified
    #             self, 
    #             'Warning!', 
    #             'No file currently open.', 
    #             qtw.QMessageBox.Ok, 
    #             qtw.QMessageBox.Ok
    #         )

    def clearFile(self):
        """Resets the current open file, as well as the components view."""

        if self.model:                                                                  # if another file is open and not saved
            self.msgBox = qtw.QMessageBox.warning(                                      # creates a message box to ask the user if the file needs to be saved
                self, 
                'File not saved...', 
                'Save changes to current file?', 
                qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel, 
                qtw.QMessageBox.Yes
            )

            if self.msgBox == qtw.QMessageBox.Yes:                                      # if the answer is yes
                self.saveFile() 
            elif self.msgBox == qtw.QMessageBox.Cancel:
                return

        self.filename = None
        self.model = None
        self.treeEditor.setModel(None)
        # self.treeEditor.componentEditor.setDisabled(True)
        # self.uiBillView.setModel(None)

# edit menu

    def addComponent(self):
        """Adds a custom component to the model."""

        currentSelection = self.treeEditor.current                      # gets the current selected item

        if currentSelection:                                                            # if an item is selected
            parentItem = currentSelection.internalPointer()                             # the item where the item has to be added is extracted
            def insertWrapper(node):
                self.model.insertRows(len(parentItem.children), node, currentSelection)
                self.treeEditor.refreshView()

            if parentItem.level < 5:                                                    # then if the level of the item is less than 5 (not a leaf node)
                self.newComponentEditor = PropEditor(parentItem)                           # opens up a popup version of PropEditor
                self.newComponentEditor.submit.connect(insertWrapper)           # connects the submit signal with the insertRows() function
                self.newComponentEditor.show()                                          # then the popup editor is shown

            else:                                                                       # if the component is not of the appropriate level
                self.msgBox = qtw.QMessageBox.warning(                                  # the user is notified
                    self, 
                    'Warning!', 
                    'The selected item is not of an appropriate level!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )

        else:                                                                           # if nothing is selected
            self.msgBox = qtw.QMessageBox.warning(                                      # the user is notified
                self, 
                'Warning!', 
                'No item currently selected.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

    def addSpecialComponent(self):
        """Adds a hardware component from the hardware archive."""

        currentSelection = self.treeEditor.current                      # gets the current selected item
        
        def insertWrapper(node):
            self.model.insertRows(currentSelection.row(), node, currentSelection)
            setattr(node, 'level', 5)
            self.treeEditor.refreshView()

        if currentSelection:                                                            # if an item is selected
            item = currentSelection.internalPointer()                                   # the item is extracted
            level = item.level                                                          # and it's level calculated

            if level < 5:                                                               # if the item is not at level 5 (leaf)
                self.hardwareSelector = HardwareSelector(self.archive)                  # a popup window containing a hardware selector is opened with the archive as model
                self.hardwareSelector.submit.connect(insertWrapper)             # then the submit signal is connected to the insertRows() function
                self.hardwareSelector.show()                                            # the popup is shown

            else:                                                                       # if the component is not of the appropriate level
                self.msgBox = qtw.QMessageBox.warning(                                  # the user is notified
                    self, 
                    'Warning!', 
                    'The selected item is not of an appropriate level!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )

        else:                                                                           # if nothing is selected
            self.msgBox = qtw.QMessageBox.warning(                                      # the user is notified
                self, 
                'Warning!', 
                'No item currently selected.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

    def addLeafComponent(self):
        currentSelection = self.treeEditor.current                      # gets the current selected item

        if currentSelection:                                                            # if an item is selected
            parentItem = currentSelection.internalPointer()                             # the item where the item has to be added is extracted
            def insertWrapper(node):
                self.model.insertRows(len(parentItem.children), node, currentSelection)
                setattr(node, 'level', 5)
                self.treeEditor.refreshView()

            if parentItem.level < 5:                                                    # then if the level of the item is less than 5 (not a leaf node)
                self.newComponentEditor = PropEditor(parentItem, 5)                           # opens up a popup version of PropEditor
                self.newComponentEditor.submit.connect(insertWrapper)           # connects the submit signal with the insertRows() function
                self.newComponentEditor.show()                                          # then the popup editor is shown

            else:                                                                       # if the component is not of the appropriate level
                self.msgBox = qtw.QMessageBox.warning(                                  # the user is notified
                    self, 
                    'Warning!', 
                    'The selected item is not of an appropriate level!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )

        else:                                                                           # if nothing is selected
            self.msgBox = qtw.QMessageBox.warning(                                      # the user is notified
                self, 
                'Warning!', 
                'No item currently selected.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

    def morphSpecialComponent(self):
        """Changes a selected hardware component with another hardware component of chice."""

        currentSelection = self.treeEditor.current                      # gets the current selected item
        def morphWrapper(node):
            self.model.swapComponent(currentSelection.row(), node, currentSelection.parent())
            setattr(node, 'level', 5)
            self.treeEditor.refreshView()

        if currentSelection:                                                            # if an item is selected
            item = currentSelection.internalPointer()                                   # the item is extracted
            level = item.level                                                          # and it's level calculated

            if level == 5:                                                              # if the item is at level 5 (leaf)
                self.hardwareSelector = HardwareSelector(self.archive)                  # a popup window containing a hardware selector is opened with the archive as model
                self.hardwareSelector.submit.connect(morphWrapper)             # then the submit signal is connected to the insertRows() function
                self.hardwareSelector.show()                                            # the popup is shown
            
            else:                                                                       # if the component is not of the appropriate level
                self.msgBox = qtw.QMessageBox.warning(                                  # the user is notified
                    self, 
                    'Warning!', 
                    'The selected item is not of an appropriate level!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )

        else:                                                                           # if nothing is selected
            self.msgBox = qtw.QMessageBox.warning(                                      # the user is notified
                self, 
                'Warning!', 
                'No item currently selected.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

    def updateSpecialComponents(self):
        """
        Iterates over the hardware/consumables components and over the archive items.
        Then updates every present item in the list with the data in the archive.
        """

        columns = {                                                                      # default values for the headers
            0: 'title', 
            1: 'description',
            2: 'type',
            3: 'manufacture',
            4: 'status',
            5: 'priceUnit',
            6: 'quantityPackage',
            7: 'seller',
            8: 'link'
        }

        sections = {
            0:2,
            1:3,
            2:4,
            3:5,
            4:6,
            5:8,
            6:10,
            7:11,
            8:13
        }

        if self.model:
            for item in self.model.rootItem.iter_leaves():                               # iterates over the hardware and the leaves
                for hardware in self.archive.hardwareList:
                    if item.number == hardware['number']:                                # if a number corresponds to the archive counterpart
                        row = item.up.children.index(item)
                        for x in range(len(columns)):                                    # iterates over the parameters of the item
                            index = self.model.createIndex(row, sections[x], item)
                            self.model.setData(index, hardware[columns[x]])              # and updates them

    def removeComponent(self):
        """Removes a component from the model."""

        currentSelection = self.treeEditor.current                      # gets the current selected item

        if currentSelection:                                                            # if an item is selected
            item = currentSelection.internalPointer()                                   # it extracts the item that needs to be removed
            row = item.up.children.index(item)                                          # it's row
            parent = currentSelection.parent()                                          # and it's parent

            if item.level != 1:                                                         # then if the item isn't at level 1 (project root)
                self.model.removeRows(row, parent)                                   # it removes it
            else:                                                                       # if the component is not of the appropriate level
                self.msgBox = qtw.QMessageBox.warning(                                  # the user is notified
                    self, 
                    'Warning!', 
                    'The selected item is not of an appropriate level!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )
        
        else:                                                                           # if nothing is selected
            self.msgBox = qtw.QMessageBox.warning(                                      # the user is notified
                self, 
                'Warning!', 
                'No item currently selected.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

# view menu

    def hideDeprecated(self):
        """Choose whether to see or not deprecated items."""

        if self.model:
            if self.uiActionHideDeprecated.isChecked():
                self.treeEditor.treeProxyModel.setFilterRegExp('Deprecated')
            else:
                self.treeEditor.treeProxyModel.setFilterRegExp('')
            self.treeEditor.refreshView()

# OTHER FUNCTIONS