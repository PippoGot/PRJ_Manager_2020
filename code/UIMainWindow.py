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
from constants import SECTIONS_TO_UPDATE as sections
from constants import COLUMNS_TO_UPDATE as columns

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
        
        uic.loadUi('D:/Data/_PROGETTI/Apps/PRJ_Manager/UIs/ui_main_window.ui', self)

        self.filename = None     
        self.archive = ModelHardware()
        self.model = None 
        self.copied = None
        self.statuses = ModelCombobox('D:/Data/_PROGETTI/APPS/PRJ_Manager/archive/statuses.csv')
        self.manufactures = ModelCombobox('D:/Data/_PROGETTI/APPS/PRJ_Manager/archive/manufactures.csv')


        self.treeEditor = ComponentsPage(self.manufactures) 
        self.uiTreePage.layout().addWidget(self.treeEditor)
        self.treeEditor.uiStatus.setModel(self.statuses)

        self.hardwareEditor = HardwareEditor(self.archive)
        self.hardwareEditor.uiCurrentStatus.setModel(self.statuses)
        self.hardwareEditor.uiNewStatus.setModel(self.statuses)
        self.uiHardwarePage.layout().addWidget(self.hardwareEditor)

        # self.billPage = BillPage(self.model)
        # self.uiBillPage.layout().addWidget(self.billPage)

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
            self.msgBox = qtw.QMessageBox.warning(      
                self, 
                'File not saved...', 
                'Save changes to current file?', 
                qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel, 
                qtw.QMessageBox.Yes
            )

            if self.msgBox == qtw.QMessageBox.Yes:
                self.saveFile()                    
            elif self.msgBox == qtw.QMessageBox.Cancel:
                return

        self.model = ModelTree()                                                
        self.treeEditor.setModel(self.model)                                     
        self.filename = None                                                     
        self.treeEditor.current = None
        # self.billPage.setModel(self.model)

    def openFile(self):
        """Opens and read a .csv file, then creates the corresponding model."""

        if not self.filename and self.model:                                      
            self.msgBox = qtw.QMessageBox.warning(                                      
                self, 
                'File not saved...', 
                'Save changes to current file?', 
                qtw.QMessageBox.Yes | qtw.QMessageBox.No, 
                qtw.QMessageBox.Yes
            )

            if self.msgBox == qtw.QMessageBox.Yes:                         
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
                self.model = ModelTree(filename)
                self.treeEditor.setModel(self.model)
                self.filename = filename
                self.treeEditor.current = None
                # self.billPage.setModel(self.model)

            except Exception as e:                                           
                self.msgBox = qtw.QMessageBox.critical(                         
                    self, 
                    'Critical Error!', 
                    f'Could not open the file at {filename}\nbecause "{e}" exception occurred!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )

    def saveFile(self):
        """Saves the current file."""

        if self.model:                                                            
            if self.filename:                                                   
                self.model.saveFile(self.filename)                                    
            else:                                                         
                self.saveAsFile()                                                    

        else:                                                              
            self.msgBox = qtw.QMessageBox.warning(                            
                self, 
                'Warning!', 
                'No file currently open.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

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
                        self.msgBox = qtw.QMessageBox.critical(                   
                        self, 
                        'Critical Error!', 
                        f'Could not save the file at {filename}\nbecause "{e}" exception occurred!', 
                        qtw.QMessageBox.Ok, 
                        qtw.QMessageBox.Ok
                    )          

                self.filename = filename                                         

        else:                                                                    
            self.msgBox = qtw.QMessageBox.warning(                             
                self, 
                'Warning!', 
                'No file currently open.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

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
                        self.msgBox = qtw.QMessageBox.critical(                 
                        self, 
                        'Critical Error!', 
                        f'Could not save the file at {filename}\nbecause "{e}" exception occurred!', 
                        qtw.QMessageBox.Ok, 
                        qtw.QMessageBox.Ok
                    )          

        else:                                                                    
            self.msgBox = qtw.QMessageBox.warning(                                   
                self, 
                'Warning!', 
                'No file currently open.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

    def clearFile(self):
        """Resets the current open file, as well as the components view."""

        if self.model:                                                            
            self.msgBox = qtw.QMessageBox.warning(                               
                self, 
                'File not saved...', 
                'Save changes to current file?', 
                qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel, 
                qtw.QMessageBox.Yes
            )

            if self.msgBox == qtw.QMessageBox.Yes:                                 
                self.saveFile() 
            elif self.msgBox == qtw.QMessageBox.Cancel:
                return

        self.filename = None
        self.model = None
        self.treeEditor.setModel(None)
        self.treeEditor.current = None
        # self.billPage.setModel(self.model)

# edit menu

    def addComponent(self):
        """Adds a custom component to the model."""

        if self.uiTabWidget.currentIndex() != 0:
            self.msgBox = qtw.QMessageBox.warning(                     
                self, 
                'Warning!', 
                'You are not in the proper page!', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )
            return

        currentSelection = self.treeEditor.current                          

        if currentSelection:                                               
            parentItem = currentSelection.internalPointer()              
            def insertWrapper(node):
                node.add_feature('level', parentItem.level + 1)
                self.model.insertRows(len(parentItem.children), node, currentSelection)
                self.treeEditor.refreshView()

            if parentItem.level < 5:                                         
                self.newComponentEditor = ComponentEditor(parentItem, self.manufactures)        
                self.newComponentEditor.uiStatus.setModel(self.statuses)
                self.newComponentEditor.submit.connect(insertWrapper)               
                self.newComponentEditor.show()                               

            else:                                                                     
                self.msgBox = qtw.QMessageBox.warning(                                 
                    self, 
                    'Warning!', 
                    'The selected item is not of an appropriate level!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )

        else:                                                     
            self.msgBox = qtw.QMessageBox.warning(                 
                self, 
                'Warning!', 
                'No item currently selected.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

    def addSpecialComponent(self):
        """Adds a hardware component from the hardware archive."""

        if self.uiTabWidget.currentIndex() != 0:
            self.msgBox = qtw.QMessageBox.warning(       
                self, 
                'Warning!', 
                'You are not in the proper page!', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )
            return

        currentSelection = self.treeEditor.current                 
        
        def insertWrapper(node):
            node.add_feature('level', 5)
            self.model.insertRows(currentSelection.row(), node, currentSelection)
            node.update_hash(self.model.rootItem)
            self.treeEditor.refreshView()

        if currentSelection:                                  
            item = currentSelection.internalPointer()                 
            level = item.level                                                      

            if level < 5:                                                          
                self.hardwareSelector = HardwareSelector(self.archive)           
                self.hardwareSelector.submit.connect(insertWrapper)                 
                self.hardwareSelector.show()                         

            else:                                                        
                self.msgBox = qtw.QMessageBox.warning(                
                    self, 
                    'Warning!', 
                    'The selected item is not of an appropriate level!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )

        else:                                                                
            self.msgBox = qtw.QMessageBox.warning(                            
                self, 
                'Warning!', 
                'No item currently selected.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

    def addLeafComponent(self):
        """Adds a level 5 component to the tree:"""

        if self.uiTabWidget.currentIndex() != 0:
            self.msgBox = qtw.QMessageBox.warning(                    
                self, 
                'Warning!', 
                'You are not in the proper page!', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )
            return

        currentSelection = self.treeEditor.current                             

        if currentSelection:                                             
            parentItem = currentSelection.internalPointer()                       
            def insertWrapper(node):
                node.add_feature('level', 5)
                self.model.insertRows(len(parentItem.children), node, currentSelection)
                node.update_hash(self.model.rootItem)
                self.treeEditor.refreshView()

            if parentItem.level < 5:                                              
                parentItem = parentItem.copy()
                parentItem.level = 4
                self.newComponentEditor = ComponentEditor(parentItem, self.manufactures, 5)  
                self.newComponentEditor.uiStatus.setModel(self.statuses)
                self.newComponentEditor.submit.connect(insertWrapper)             
                self.newComponentEditor.show()                                

            else:                                                                  
                self.msgBox = qtw.QMessageBox.warning(                         
                    self, 
                    'Warning!', 
                    'The selected item is not of an appropriate level!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )

        else:                                                                     
            self.msgBox = qtw.QMessageBox.warning(                            
                self, 
                'Warning!', 
                'No item currently selected.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

    def addJig(self):
        """Adds a jig component to the tree."""

        if self.uiTabWidget.currentIndex() != 0:
            self.msgBox = qtw.QMessageBox.warning(       
                self, 
                'Warning!', 
                'You are not in the proper page!', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )
            return

        currentSelection = self.treeEditor.current                        

        if currentSelection:                                        
            parentItem = currentSelection.internalPointer()                          
            def insertWrapper(node):
                node.add_feature('level', 4)
                self.model.insertRows(len(parentItem.children), node, currentSelection)
                node.update_hash(self.model.rootItem)
                self.treeEditor.refreshView()

            if parentItem.level < 5:                                     
                jigsList = self.model.rootItem.search_nodes(type = 'Jig')
                dummyParent = ComponentTree('', {'number': '#JIG-000', 'level': -1, 'children': jigsList})

                self.newComponentEditor = ComponentEditor(dummyParent, self.manufactures, 5)           
                self.newComponentEditor.uiStatus.setModel(self.statuses)
                self.newComponentEditor.submit.connect(insertWrapper)         
                self.newComponentEditor.show()                                

            else:                                                                   
                self.msgBox = qtw.QMessageBox.warning(                 
                    self, 
                    'Warning!', 
                    'The selected item is not of an appropriate level!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )

        else:                                                                 
            self.msgBox = qtw.QMessageBox.warning(                   
                self, 
                'Warning!', 
                'No item currently selected.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )
    
    def addPlaceholder(self):
        """Adds a placeholder component to the tree."""

        if self.uiTabWidget.currentIndex() != 0:
            self.msgBox = qtw.QMessageBox.warning(               
                self, 
                'Warning!', 
                'You are not in the proper page!', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )
            return

        currentSelection = self.treeEditor.current                            

        if currentSelection:                                     
            parentItem = currentSelection.internalPointer()  
            def insertWrapper(node):
                node.add_feature('level', 4)
                self.model.insertRows(len(parentItem.children), node, currentSelection)
                node.update_hash(self.model.rootItem)
                self.treeEditor.refreshView()

            if parentItem.level < 5:                                          
                placeholderList = self.model.rootItem.search_nodes(type = 'Placeholder')
                dummyParent = ComponentTree('', {'number': '#PLC-000', 'level': 5, 'children': placeholderList})

                self.newComponentEditor = ComponentEditor(dummyParent, self.manufactures, 5)          
                self.newComponentEditor.uiStatus.setModel(self.statuses)
                self.newComponentEditor.submit.connect(insertWrapper)               
                self.newComponentEditor.show()                                  

            else:                                                                  
                self.msgBox = qtw.QMessageBox.warning(             
                    self, 
                    'Warning!', 
                    'The selected item is not of an appropriate level!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )

        else:                                                                 
            self.msgBox = qtw.QMessageBox.warning(                               
                self, 
                'Warning!', 
                'No item currently selected.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

    def morphSpecialComponent(self):
        """Changes a selected hardware component with another hardware component of choice."""

        if self.uiTabWidget.currentIndex() != 0:
            self.msgBox = qtw.QMessageBox.warning(                 
                self, 
                'Warning!', 
                'You are not in the proper page!', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )
            return

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
                self.msgBox = qtw.QMessageBox.warning(                 
                    self, 
                    'Warning!', 
                    'The selected item is not of an appropriate level!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )

        else:                                                                   
            self.msgBox = qtw.QMessageBox.warning(                       
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

        if self.uiTabWidget.currentIndex() != 0:
            self.msgBox = qtw.QMessageBox.warning(         
                self, 
                'Warning!', 
                'You are not in the proper page!', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )
            return

        if self.model:
            for item in self.model.rootItem.iter_leaves():                         
                for hardware in self.archive.hardwareList:
                    if item.number == hardware['number']:                       
                        row = item.up.children.index(item)
                        for x in range(len(columns)):                                 
                            index = self.model.createIndex(row, sections[x], item)
                            self.model.setData(index, hardware[columns[x]])        

    def removeComponent(self):
        """Removes a component from the model."""

        if self.uiTabWidget.currentIndex() != 0:
            self.msgBox = qtw.QMessageBox.warning(                    
                self, 
                'Warning!', 
                'You are not in the proper page!', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )
            return

        currentSelection = self.treeEditor.current                              

        if currentSelection:                                               
            item = currentSelection.internalPointer()                                  
            row = item.up.children.index(item)                         
            parent = currentSelection.parent()                               

            if item.level != 1:                         
                self.model.removeRows(row, parent)                             
            else:                                                                  
                self.msgBox = qtw.QMessageBox.warning(                    
                    self, 
                    'Warning!', 
                    'The selected item is not of an appropriate level!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )
        
        else:                                                                 
            self.msgBox = qtw.QMessageBox.warning(                              
                self, 
                'Warning!', 
                'No item currently selected.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

    def cut(self):
        """Removes and store a component for later pasting."""

        if self.uiTabWidget.currentIndex() != 0:
            self.msgBox = qtw.QMessageBox.warning(                         
                self, 
                'Warning!', 
                'You are not in the proper page!', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )
            return

        currentSelection = self.treeEditor.current

        if currentSelection:                                                    
            item = currentSelection.internalPointer()                               
            row = item.up.children.index(item)                            
            parent = currentSelection.parent()                              

            if item.level != 1:                                                      
                self.copied = self.model.removeRows(row, parent)
            else:                                                                
                self.msgBox = qtw.QMessageBox.warning(                        
                    self, 
                    'Warning!', 
                    'The selected item is not of an appropriate level!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )
        
        else:                                                     
            self.msgBox = qtw.QMessageBox.warning(                                
                self, 
                'Warning!', 
                'No item currently selected.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

    def copy(self):
        """Creates and stores a copy of a component to paste it in another component."""

        if self.uiTabWidget.currentIndex() != 0:
            self.msgBox = qtw.QMessageBox.warning(                            
                self, 
                'Warning!', 
                'You are not in the proper page!', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )
            return

        currentSelection = self.treeEditor.current

        if currentSelection:                                                   
            item = currentSelection.internalPointer()       

            if item.level != 1:                                                                                         
                self.copied = item.copy()
            else:                                                            
                self.msgBox = qtw.QMessageBox.warning(                             
                    self, 
                    'Warning!', 
                    'The selected item is not of an appropriate level!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )
        
        else:                                                     
            self.msgBox = qtw.QMessageBox.warning(                              
                self, 
                'Warning!', 
                'No item currently selected.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

    def paste(self):
        """Adds the cut or copied component to this components' children."""

        if self.uiTabWidget.currentIndex() != 0:
            self.msgBox = qtw.QMessageBox.warning(                    
                self, 
                'Warning!', 
                'You are not in the proper page!', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )
            return

        currentSelection = self.treeEditor.current                           

        if currentSelection:                                              
            parentItem = currentSelection.internalPointer()                           

            if parentItem.level < 5:                                              
                self.model.insertRows(len(parentItem.children), self.copied, currentSelection)
                self.copied.update_hash(self.model.rootItem)
                self.copied = self.copied.copy()
                self.treeEditor.refreshView()

            else:                                                               
                self.msgBox = qtw.QMessageBox.warning(                           
                    self, 
                    'Warning!', 
                    'The selected item is not of an appropriate level!', 
                    qtw.QMessageBox.Ok, 
                    qtw.QMessageBox.Ok
                )

        else:                                                                 
            self.msgBox = qtw.QMessageBox.warning(                              
                self, 
                'Warning!', 
                'No item currently selected.', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )

# view menu

    def hideDeprecated(self):
        """Choose whether to see or not deprecated items."""

        if self.uiTabWidget.currentIndex() != 0:
            self.msgBox = qtw.QMessageBox.warning(                    
                self, 
                'Warning!', 
                'You are not in the proper page!', 
                qtw.QMessageBox.Ok, 
                qtw.QMessageBox.Ok
            )
            return

        if self.model:
            if self.uiActionHideDeprecated.isChecked():
                self.treeEditor.treeProxyModel.setFilterRegExp('Deprecated')
            else:
                self.treeEditor.treeProxyModel.setFilterRegExp(None)
            self.treeEditor.refreshView()

# OTHER FUNCTIONS

def checkPage(self):
    #checks if we are in the right page before performing the action
    pass

def checkModel(self):
    #checks if a model is present
    pass