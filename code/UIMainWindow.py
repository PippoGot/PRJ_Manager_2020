from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from UIComponentsPage import ComponentsPage
from UIHardwareEditor import HardwareEditor
from UIBillPage import BillPage
from UIComponentEditor import ComponentEditor
from UIHardwareSelector import HardwareSelector

from ModelHardware import ModelHardware
from ModelTreeETE import ModelTree
from ModelCombobox import ModelCombobox

from ComponentTree import ComponentTree

from constants import SECTIONS_TO_UPDATE
from constants import COLUMNS_TO_UPDATE

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

        super(MainWindow, self).__init__()
        
        uic.loadUi('code/resources/UIs/ui_main_window.ui', self)

        self.filename = None     
        self.archive = ModelHardware()
        self.model = None 
        self.copied = None
        self.statuses = ModelCombobox('code/resources/archive/statuses.csv')
        self.manufactures = ModelCombobox('code/resources/archive/manufactures.csv')


        self.treeEditor = ComponentsPage(self.manufactures) 
        self.uiTreePage.layout().addWidget(self.treeEditor)
        self.treeEditor.uiStatus.setModel(self.statuses)

        self.hardwareEditor = HardwareEditor(self.archive)
        self.hardwareEditor.uiCurrentStatus.setModel(self.statuses)
        self.hardwareEditor.uiNewStatus.setModel(self.statuses)
        self.uiHardwarePage.layout().addWidget(self.hardwareEditor)

        self.billPage = BillPage(self.model)
        self.uiBillPage.layout().addWidget(self.billPage)

        # FILE MENU ACTIONS
        self.uiActionNew.triggered.connect(self.newFile)
        self.uiActionOpen.triggered.connect(self.openFile)
        self.uiActionSave.triggered.connect(self.saveFile)
        self.uiActionSaveAs.triggered.connect(self.saveAsFile)
        self.uiActionClear.triggered.connect(self.clearFile)
        self.uiActionExportBOM.triggered.connect(self.exportBOM)

        # EDIT MENU ACTIONS
        self.uiActionAddComponent.triggered.connect(self.addComponent)
        self.uiActionAddSpecialComponent.triggered.connect(self.addSpecialComponent)
        self.uiActionAddLeafComponent.triggered.connect(self.addLeafComponent)
        self.uiActionAddJig.triggered.connect(self.addJig)
        self.uiActionAddPlaceholder.triggered.connect(self.addPlaceholder)

        self.uiActionMorphSpecialComponent.triggered.connect(self.morphSpecialComponent)
        self.uiActionUpdateSpecialComponents.triggered.connect(self.updateSpecialComponents)
        self.uiActionRemoveComponent.triggered.connect(self.removeComponent)

        self.uiActionCut.triggered.connect(self.cut)
        self.uiActionCopy.triggered.connect(self.copy)
        self.uiActionPaste.triggered.connect(self.paste)
        # self.uiActionUndo.triggered.connect(self.undo)
        # self.uiActionRedo.triggered.connect(self.redo)

        # VIEW MENU ACTIONS
        self.uiActionHideDeprecated.triggered.connect(self.hideDeprecated)
        self.uiActionExpandAll.triggered.connect(self.treeEditor.uiComponentsView.expandAll)
        self.uiActionCollapseAll.triggered.connect(self.treeEditor.uiComponentsView.collapseAll)

        self.showMaximized()

# ACTION FUNCTIONS
# file menu

    def newFile(self):
        """Creates a new model, for a new file."""

        if not self.filename and self.model:
            dialog = self.cancelDialog('File not saved...', 'Save changes to current file?')

            if dialog == qtw.QMessageBox.Yes:
                self.saveFile()                    
            elif dialog == qtw.QMessageBox.Cancel:
                return

        self.setModel(ModelTree())

    def openFile(self):
        """Opens and read a .csv file, then creates the corresponding model."""

        if not self.filename and self.model:
            dialog = self.choiceDialog('File not saved...', 'Save changes to current file?')

            if dialog == qtw.QMessageBox.Yes:                         
                self.saveFile()                                               

        filename, _ = qtw.QFileDialog.getOpenFileName(                        
            self, 
            "Select a file to open...", 
            qtc.QDir.homePath(), 
            'CSV Documents (*.csv) ;; All Files (*)', 
            'CSV Documents (*.csv)'
        )

        if filename:                                                                 
            try:           
                self.setModel(ModelTree(filename), filename)

            except Exception as e:
                self.okDialog('Critical Error!', f'Could not open the file at {filename}\nbecause " {e} " exception occurred!')

    def saveFile(self):
        """Saves the current file."""

        if self.model:                                                            
            if self.filename:                                                   
                self.model.saveFile(self.filename)                                    
            else:                                                         
                self.saveAsFile()                                                    

        else:
            self.okDialog('Warning!', 'No file currently open.')

    def saveAsFile(self):
        """Saves the file with a different filename from the original, or a new file."""

        if self.model:                                                
            filename, _ = qtw.QFileDialog.getSaveFileName(                  
                self, 
                "Select the file to save to...", 
                qtc.QDir.homePath(),
                'CSV Documents (*.csv)'
            )

            if filename:                                                        
                try:
                    self.model.saveFile(filename)                      

                except Exception as e:   
                    self.okDialog('Critical Error!', f'Could not save the file at {filename}\nbecause " {e} " exception occurred!')     

                self.filename = filename                                         

        else:     
            self.okDialog('Warning!', 'No file currently open.')

    def exportBOM(self):
        """Exports the bill of material of the current project"""
        
        if self.model:
            filename, _ = qtw.QFileDialog.getSaveFileName(              
                self, 
                "Select the file to save to...", 
                qtc.QDir.homePath(),
                'CSV Documents (*.csv)'
            )

            if filename:                                                    
                try:
                    self.model.exportBOM(filename)

                except Exception as e:    
                    self.okDialog('Critical Error!', f'Could not save the file at {filename}\nbecause " {e} " exception occurred!')        

        else:    
            self.okDialog('Warning!', 'No file currently open.')

    def clearFile(self):
        """Resets the current open file, as well as the components view."""

        if self.model:    
            dialog = self.cancelDialog('File not saved...', 'Save changes to current file?')

            if dialog == qtw.QMessageBox.Yes:                                 
                self.saveFile() 
            elif dialog == qtw.QMessageBox.Cancel:
                return

        self.setModel()

# edit menu

    def addComponent(self):
        """Adds a custom component to the model."""

        if self.checkPage(0): return

        currentSelection = self.treeEditor.current                          

        if currentSelection:                                               
            parentItem = currentSelection.internalPointer()    
            
            def wrapper(node):
                self.insertWrapper(node, parentItem.level + 1, currentSelection, len(parentItem.children))

            if parentItem.level < 5:                                         
                self.newComponentEditor = ComponentEditor(parentItem, self.manufactures)        
                self.newComponentEditor.uiStatus.setModel(self.statuses)
                self.newComponentEditor.submit.connect(wrapper)               
                self.newComponentEditor.show()                               

            else:    
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else: 
            self.okDialog('Warning!', 'No item currently selected.')

    def addSpecialComponent(self):
        """Adds a hardware component from the hardware archive."""

        if self.checkPage(0): return

        currentSelection = self.treeEditor.current                 
        
        def wrapper(node):
            self.insertWrapper(node, 5, currentSelection, currentSelection.row())

        if currentSelection:                                  
            item = currentSelection.internalPointer()                 
            level = item.level                                                      

            if level < 5:                                                          
                self.hardwareSelector = HardwareSelector(self.archive)           
                self.hardwareSelector.submit.connect(wrapper)                 
                self.hardwareSelector.show()                         

            else:    
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else: 
            self.okDialog('Warning!', 'No item currently selected.')

    def addLeafComponent(self):
        """Adds a level 5 component to the tree:"""

        if self.checkPage(0): return

        currentSelection = self.treeEditor.current                             

        if currentSelection:                                             
            parentItem = currentSelection.internalPointer()                       
            def wrapper(node):
                self.insertWrapper(node, 5, currentSelection, len(parentItem.children))

            if parentItem.level < 5:                                              
                parentItem = parentItem.copy()
                parentItem.level = 4
                self.newComponentEditor = ComponentEditor(parentItem, self.manufactures, 5)  
                self.newComponentEditor.uiStatus.setModel(self.statuses)
                self.newComponentEditor.submit.connect(wrapper)             
                self.newComponentEditor.show()                                

            else:    
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else: 
            self.okDialog('Warning!', 'No item currently selected.')

    def addJig(self):
        """Adds a jig component to the tree."""

        if self.checkPage(0): return

        currentSelection = self.treeEditor.current                        

        if currentSelection:                                        
            parentItem = currentSelection.internalPointer()                          
            def wrapper(node):
                self.insertWrapper(node, 4, currentSelection, len(parentItem.children))

            if parentItem.level < 5:                                     
                jigsList = self.model.rootItem.search_nodes(type = 'Jig')
                dummyParent = ComponentTree('', {'number': '#JIG-000', 'level': -1, 'children': jigsList})

                self.newComponentEditor = ComponentEditor(dummyParent, self.manufactures, 5)           
                self.newComponentEditor.uiStatus.setModel(self.statuses)
                self.newComponentEditor.submit.connect(wrapper)         
                self.newComponentEditor.show()                                

            else:    
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else: 
            self.okDialog('Warning!', 'No item currently selected.')

    def addPlaceholder(self):
        """Adds a placeholder component to the tree."""

        if self.checkPage(0): return

        currentSelection = self.treeEditor.current                            

        if currentSelection:                                     
            parentItem = currentSelection.internalPointer()  
            def wrapper(node):
                self.insertWrapper(node, 4, currentSelection, len(parentItem.children))

            if parentItem.level < 5:                                          
                placeholderList = self.model.rootItem.search_nodes(type = 'Placeholder')
                dummyParent = ComponentTree('', {'number': '#PLC-000', 'level': 5, 'children': placeholderList})

                self.newComponentEditor = ComponentEditor(dummyParent, self.manufactures, 5)          
                self.newComponentEditor.uiStatus.setModel(self.statuses)
                self.newComponentEditor.submit.connect(wrapper)               
                self.newComponentEditor.show()                                  

            else:    
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else: 
            self.okDialog('Warning!', 'No item currently selected.')

    def morphSpecialComponent(self):
        """Changes a selected hardware component with another hardware component of choice."""

        if self.checkPage(0): return

        currentSelection = self.treeEditor.current                          
        def morphWrapper(node):
            self.model.swapComponent(currentSelection.row(), node, currentSelection.parent())
            node.add_feature('level', 5)
            node.update_hash(self.model.rootItem)
            self.treeEditor.refreshView()

        if currentSelection:                                                    
            item = currentSelection.internalPointer()                          
            level = item.level                                    

            if level == 5:                                              
                self.hardwareSelector = HardwareSelector(self.archive)           
                self.hardwareSelector.submit.connect(morphWrapper)                  
                self.hardwareSelector.show()                               
            
            else:    
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else: 
            self.okDialog('Warning!', 'No item currently selected.')

    def updateSpecialComponents(self):
        """
        Iterates over the hardware/consumables components and over the archive items.
        Then updates every present item in the list with the data in the archive.
        """

        if self.checkPage(0): return

        if self.model:
            for item in self.model.rootItem.iter_leaves():                         
                for hardware in self.archive.hardwareList:
                    if item.number == hardware['number']:                       
                        row = item.up.children.index(item)
                        for x in range(len(COLUMNS_TO_UPDATE)):                                 
                            index = self.model.createIndex(row, SECTIONS_TO_UPDATE[x], item)
                            self.model.setData(index, hardware[COLUMNS_TO_UPDATE[x]])        

    def removeComponent(self):
        """Removes a component from the model."""

        if self.checkPage(0): return

        currentSelection = self.treeEditor.current                              

        if currentSelection:                                               
            item = currentSelection.internalPointer()                                  
            row = item.up.children.index(item)                         
            parent = currentSelection.parent()                               

            if item.level != 1:                         
                self.model.removeRows(row, parent)                             
            else:    
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else: 
            self.okDialog('Warning!', 'No item currently selected.')

    def cut(self):
        """Removes and stores a component for later pasting."""

        if self.checkPage(0): return

        currentSelection = self.treeEditor.current

        if currentSelection:                                                    
            item = currentSelection.internalPointer()                               
            row = item.up.children.index(item)                            
            parent = currentSelection.parent()                              

            if item.level != 1:                                                      
                self.copied = self.model.removeRows(row, parent)
            else:    
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else: 
            self.okDialog('Warning!', 'No item currently selected.')

    def copy(self):
        """Creates and stores a copy of a component to paste it in another component."""

        if self.checkPage(0): return

        currentSelection = self.treeEditor.current

        if currentSelection:                                                   
            item = currentSelection.internalPointer()       

            if item.level != 1:                                                                                         
                self.copied = item.copy()
            else:    
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else: 
            self.okDialog('Warning!', 'No item currently selected.')

    def paste(self):
        """Adds the cut or copied component to this components' children."""

        if self.checkPage(0): return

        currentSelection = self.treeEditor.current                           

        if currentSelection:                                              
            parentItem = currentSelection.internalPointer()                           

            if parentItem.level < 5:                                              
                self.model.insertRows(len(parentItem.children), self.copied, currentSelection)
                self.copied.update_hash(self.model.rootItem)
                self.copied = self.copied.copy()
                self.treeEditor.refreshView()
                
            else:    
                self.okDialog('Warning!', 'The selected item is not of an appropriate level!')

        else: 
            self.okDialog('Warning!', 'No item currently selected.')

# view menu

    def hideDeprecated(self):
        """Choose whether to see or not deprecated items."""

        if self.model:
            if self.uiActionHideDeprecated.isChecked():
                self.treeEditor.treeProxyModel.setFilterRegExp('Deprecated')
            else:
                self.treeEditor.treeProxyModel.setFilterRegExp(None)
            self.treeEditor.refreshView()

# OTHER FUNCTIONS

    def checkPage(self, page):
        """
        Checks if the user is in the correct page and notify with a dialog if it's not.

        INPUT
            int - page: the page to check for

        RETURN TYPE:
            bool: whether the user is in the correct page orr not
        """

        if self.uiTabWidget.currentIndex() != page:
            self.msgBox = qtw.QMessageBox.warning(                    
                self, 
                'Warning!', 
                'You are not in the proper page!', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok            
            )
            return True
        return False

    def setModel(self, model = None, filename = None):
        """
        Sets the window model for all the different pages. Also if the model is from an external file
        the filename is updated.
        
        INPUT:
            QAbstractItemModel - model: the model to set
            str - filename: the filename of the file
        """

        self.model = model
        self.filename = filename
        self.treeEditor.setModel(self.model)
        self.treeEditor.current = None
        self.billPage.setModel(self.model)

    def insertWrapper(self, node, level, currentSelection, position):
        """
        Template for the insertion function in the model.

        INPUT:
            ComponentTree - node: the item to add to the tree
            int - level: the level of the new component
            QModelIndex - currentSelection: the index where to add the node
            int - position: the position where to add the node
        """

        node.add_feature('level', level)
        self.model.insertRows(position, node, currentSelection)
        node.update_hash(self.model.rootItem)
        self.treeEditor.refreshView()

    def okDialog(self, title, message):
        """
        Creates a dialog window with an OK button.

        INPUT:
            str - title: the title of the dialog
            str - message: the message of the dialog

        RETURN TYPE:
            enum: the button pressed by the user
        """

        self.msgBox = qtw.QMessageBox.warning(      
            self, 
            title, 
            message, 
            qtw.QMessageBox.Ok,
            qtw.QMessageBox.Ok
        )

        return self.msgBox

    def choiceDialog(self, title, message):        
        """
        Creates a dialog window with a YES/NO choice.

        INPUT:
            str - title: the title of the dialog
            str - message: the message of the dialog

        RETURN TYPE:
            enum: the button pressed by the user
        """

        self.msgBox = qtw.QMessageBox.warning(      
            self, 
            title, 
            message, 
            qtw.QMessageBox.Yes | qtw.QMessageBox.No,
            qtw.QMessageBox.Yes
        )

        return self.msgBox

    def cancelDialog(self, title, message):
        """
        Creates a dialog window with an YES/NO/CANCEL choice.

        INPUT:
            str - title: the title of the dialog
            str - message: the message of the dialog

        RETURN TYPE:
            enum: the button pressed by the user
        """

        self.msgBox = qtw.QMessageBox.warning(      
            self, 
            title, 
            message, 
            qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel, 
            qtw.QMessageBox.Yes
        )

        return self.msgBox