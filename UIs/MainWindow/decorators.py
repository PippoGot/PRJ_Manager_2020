from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

def ComponentsAction(func):
    """
    Executes a function only if the current page is the components page.

    Args:
        func (PyFunction): the functions to execute if the page is correct
    """

    def wrapper(*args, **kwargs):
        self = args[0]
        if self._checkPage(0): return
        return func(*args, **kwargs)

    return wrapper

def ifHasModel(func):
    """
    Executes a function only if a model is present.

    Args:
        func (PyFunction): the function to execute if the model is present
    """

    def wrapper(*args, **kwargs):
        self = args[0]
        if self.treeModel:
            return func(*args, **kwargs)

    return wrapper

def ifNodeSelected(func):
    """
    Executes the passed function only if a node is currently selected.

    Args:
        func (PyFunction): the function to execute if a node is selected.
    """

    def wrapper(*args, **kwargs):
        self = args[0]
        currentNode = self.componentsPage.getCurrentNode()
        if currentNode:
            return func(*args, **kwargs)
        else:
            self._okDialog('Warning!', 'No item currently selected.')

    return wrapper

def ifNotRoot(func):
    """
    Executes the passed funtion if the current node is not the root.

    Args:
        func (PyFunction): the function to execute if the node is not a root
    """

    def wrapper(*args, **kwargs):
        self = args[0]
        currentNode = self.componentsPage.getCurrentNode()
        if currentNode.getLevel() != 1:
            return func(*args, **kwargs)
        else:
            self._okDialog('Warning!', 'The selected item is not of an appropriate level!')

    return wrapper

def ifNotLeaf(func):
    """
    Executes the passed funtion if the current node is not a leaf node.

    Args:
        func (PyFunction): the function to execute if the node is not a root
    """

    def wrapper(*args, **kwargs):
        self = args[0]
        currentNode = self.componentsPage.getCurrentNode()
        if currentNode.getLevel() < 5:
            return func(*args, **kwargs)
        else:
            self._okDialog('Warning!', 'The selected item is not of an appropriate level!')

    return wrapper

def askSave(func):
    """
    Checks for a model, if a model is not present executes the function.
    otherwise, checks for unsaved changes, if no changes are present
    excecutes the function, otherwise asks for saving.
    If the user chooses yes, the file is saved, then the function is run.
    If the user chooses no, the file is not saved and the function is run.
    If the user chooses cancel, the file is not saved and the function is not run.

    Args:
        func (PyFunction): the function to run in yes/no cases
    """

    def wrapper(*args, **kwargs):
        self = args[0]

        if not self.treeModel: return func(*args, **kwargs)
        if not self.unsavedChanges: return func(*args, **kwargs)

        dialog = self._cancelDialog('File not saved...', 'Save changes to current file?')

        if dialog == qtw.QMessageBox.Yes:
            self.saveFile()
            return func(*args, **kwargs)
        elif dialog == qtw.QMessageBox.No:
            return func(*args, **kwargs)
        elif dialog == qtw.QMessageBox.Cancel:
            return

    return wrapper

def produceChanges(func):
    """
    Updates the variable for unsaved changes.

    Args:
        func (PyFunction): the function that produces unsaved changes
    """

    def wrapper(*args, **kwargs):
        self = args[0]

        val = func(*args, **kwargs)
        self.unsavedChanges = True
        print(self.unsavedChanges)
        return val

    return wrapper
