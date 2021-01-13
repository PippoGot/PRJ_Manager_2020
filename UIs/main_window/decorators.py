from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from functools import wraps

from . import dialogs

# PAGE SELECTION

def componentsAction(func):
    """
    Executes a function only if the current page is the components page.

    Args:
        func (PyFunction): the functions to execute if the page is correct
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if self._checkPage(0): return
        return func(*args, **kwargs)

    return wrapper

# --- BOOLEANS ---

# DATA SELECTED

def ifHasModel(func):
    """
    Executes a function only if a model is present.

    Args:
        func (PyFunction): the function to execute if the model is present
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.componentsPage.getModel():
            return func(*args, **kwargs)
        else:
            return dialogs.noFileError()

    return wrapper

def ifNodeSelected(func):
    """
    Executes the passed function only if a node is currently selected.

    Args:
        func (PyFunction): the function to execute if a node is selected
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        currentNode = self.componentsPage.getCurrentNode()
        if currentNode:
            return func(*args, **kwargs)
        else:
            return dialogs.noSelectionError()

    return wrapper

# NODE TYPING

def ifNotRoot(func):
    """
    Executes the passed funtion if the current node is not the root.

    Args:
        func (PyFunction): the function to execute if the node is not a root
    """

    @componentsAction
    @ifNodeSelected
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        currentNode = self.componentsPage.getCurrentNode()
        if currentNode.getLevel() != 1:
            return func(*args, **kwargs)
        else:
            return dialogs.levelError()

    return wrapper

def ifLeaf(func):
    """
    Executes the passed funtion if the current node is a leaf.

    Args:
        func (PyFunction): the function to execute if the node is a leaf
    """

    @componentsAction
    @ifNodeSelected
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        currentNode = self.componentsPage.getCurrentNode()
        if currentNode.getLevel() == 5:
            return func(*args, **kwargs)
        else:
            return dialogs.levelError()

    return wrapper

def ifNotLeaf(func):
    """
    Executes the passed funtion if the current node is not a leaf node.

    Args:
        func (PyFunction): the function to execute if the node is not a root
    """

    @componentsAction
    @ifNodeSelected
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        currentNode = self.componentsPage.getCurrentNode()
        if currentNode.getLevel() < 5:
            return func(*args, **kwargs)
        else:
            return dialogs.levelError()

    return wrapper

def ifIsHardware(func):
    """
    Executes the passed funtion if the current node is of hardware type.

    Args:
        func (PyFunction): the function to execute if the node is hardware
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        currentNode = self.componentsPage.getCurrentNode()
        if currentNode.getFeature('type') == 'Hardware':
            return func(*args, **kwargs)
        else:
            return dialogs.typeError()

    return wrapper

# FILE MANAGING

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

    @undoable
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]

        if not self.componentsPage.getModel(): return func(*args, **kwargs)
        if not self.unsavedChanges: return func(*args, **kwargs)

        dialog = dialogs.askSave()

        if dialog == qtw.QMessageBox.Yes:
            self.saveFile()
            return func(*args, **kwargs)
        elif dialog == qtw.QMessageBox.No:
            return func(*args, **kwargs)
        elif dialog == qtw.QMessageBox.Cancel:
            return

    return wrapper

def producesChanges(func):
    """
    Updates the variable for unsaved changes.

    Args:
        func (PyFunction): the function that produces unsaved changes
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]

        val = func(*args, **kwargs)
        self.unsavedChanges = True
        return val

    return wrapper

def undoable(func):
    """
    Adds a snapshot to the UndoStack to undo the currently performed action.

    Args:
        func (PyFunction): the function that is undoable
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]

        val = func(*args, **kwargs)

        data = str(self.componentsPage.getModel())
        name = func.__name__
        self.undoStack.addSnapshot(data, name)

        return val

    return wrapper

def undoableAction(func):
    """
    Composite decorator, produces changes + undoable.
    """

    @producesChanges
    @undoable
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
