from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

# BASE

# templates
def _okDialog(title, message):
    """
    Creates a dialog window with an OK button.

    Args:
        title (str): the title of the dialog.
        message (str): the message of the dialog.

    Returns:
        enum: the button pressed by the user
    """

    msgBox = qtw.QMessageBox.warning(
        None,
        title,
        message,
        qtw.QMessageBox.Ok,
        qtw.QMessageBox.Ok
    )

    return msgBox

def _choiceDialog(title, message):
    """
    Creates a dialog window with a YES/NO choice.

    Args:
        title (str): the title of the dialog.
        message (str): the message of the dialog.

    Returns:
        enum: the button pressed by the user.
    """

    msgBox = qtw.QMessageBox.warning(
        None,
        title,
        message,
        qtw.QMessageBox.Yes | qtw.QMessageBox.No,
        qtw.QMessageBox.Yes
    )

    return msgBox

def _cancelDialog(title, message):
    """
    Creates a dialog window with an YES/NO/CANCEL choice.

    Args:
        title (str): the title of the dialog.
        message (str): the message of the dialog.

    Returns:
        enum: the button pressed by the user.
    """

    msgBox = qtw.QMessageBox.warning(
        None,
        title,
        message,
        qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel,
        qtw.QMessageBox.Yes
    )

    return msgBox

# file
def openDialog():
    """
    Returns a filename if a file is selected from the browser.

    Returns:
        str: the filename selected
    """

    filename, _ = qtw.QFileDialog.getOpenFileName(
        None,
        "Select a file to open...",
        qtc.QDir.homePath(),
        'JSON Documents (*.json) ;; All Files (*)',
        'JSON Documents (*.json)'
    )

    return filename

def saveDialog():
    """
    Returns a filename if a file is selected from the browser.

    Returns:
        str: the filename selected
    """

    filename, _ = qtw.QFileDialog.getSaveFileName(
        None,
        "Select the file to save to...",
        qtc.QDir.homePath(),
        'JSON Documents (*.json)'
    )

    return filename

# ERRORS

def pageError():
    return _okDialog('Warning!', 'You are not in the proper page!')

def noFileError():
    return _okDialog('Warning!', 'No file currently open!')

def fileReadError():
    return _okDialog('Warning!', 'The file you tried to open either does not exist or can\'t be read')

def noSelectionError():
    return _okDialog('Warning!', 'No item currently selected!')

def levelError():
    return _okDialog('Warning!', 'The selected item is not of an appropriate level!')

def typeError():
    return _okDialog('Warning!', 'The selected item is not of the correct type!')

# QUESTIONS

def askSave():
    return _cancelDialog('File not saved...', 'Save changes to current file?')