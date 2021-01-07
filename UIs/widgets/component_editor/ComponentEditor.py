from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from .component_editor import  Ui_uiComponentEditor as ui

class ComponentEditor(qtw.QWidget, ui):
    """
    General purpose component node editor. Used to edit nodes in a
    tree or archive model.
    """

    def __init__(self):
        """
        Loads the UI window and initialise the class variables.
        """

        super(ComponentEditor, self).__init__()
        self.setupUi(self)

        self.model = None
        self.manufactureModel = None
        self.statusModel = None
        self.currentIndex = qtc.QModelIndex()
        self.mapper = qtw.QDataWidgetMapper()

        self._enableSelf()

# --- MODELS ---

    def setModel(self, model):
        """
        Sets the editor model and initialize the mapper.

        Args:
            model (ModelTree): the model of the editor widget
        """

        self.model = model
        self.currentIndex = qtc.QModelIndex()

        self.mapper.setModel(self.model)

        if self.model:
            self.mapper.addMapping(self.uiNumberID, 0)
            self.mapper.addMapping(self.uiName, 1)
            self.mapper.addMapping(self.uiDescription, 2)
            self.mapper.addMapping(self.uiType, 3)
            self.mapper.addMapping(self.noneditable, 4)
            self.mapper.addMapping(self.editable, 4)
            self.mapper.addMapping(self.uiStatus, 5)
            self.mapper.addMapping(self.uiComment, 6)
            self.mapper.addMapping(self.uiPrice, 7)
            self.mapper.addMapping(self.uiQuantity, 8)
            self.mapper.addMapping(self.uiQuantityPackage, 9)
            self.mapper.addMapping(self.uiSeller, 10)
            self.mapper.addMapping(self.uiLink, 11)

            self.model.dataChanged.connect(self.mapper.revert)
        else:
            self._enableSelf()

    def setManufactureModel(self, manufactureModel):
        """
        Sets the editor's manufacture combobox model.

        Args:
            manufactureModel (ModelCombobox): the model of the combobox
        """

        self.manufactureModel = manufactureModel
        self.editable.setModel(self.manufactureModel)

    def setStatusModel(self, statusModel):
        """
        Sets the editor's status combobox model.

        Args:
            statusModel (ModelCombobox): the model of the combobox
        """

        self.statusModel = statusModel
        self.uiStatus.setModel(self.statusModel)

# --- SELECTION ---

    def setCurrentSelection(self, newIndex):
        """
        The index is set as the current index of the editor.

        Args:
            index (QModelIndex): the index to update
        """

        self.currentIndex = newIndex
        self._enableSelf()
        if not self.currentIndex.isValid(): return

        self.currentNode = self.currentIndex.internalPointer()

        indexParent = newIndex.parent()
        self.mapper.setRootIndex(indexParent)
        self.mapper.setCurrentModelIndex(self.currentIndex)

        self._changeManufacture()

# --- UTILITY

    def _changeManufacture(self):
        """
        Changes dinamically the manufacture widget. The editable nodes will
        have a combo box, while non-editable nodes will have a read-only line edit.
        """

        editable = self.currentNode.isEditable()

        if editable:
            self.uiManufacture.setCurrentIndex(1)
        else:
            self.uiManufacture.setCurrentIndex(0)

    def _enableSelf(self):
        """
        Enables or disables the widget based on the selection.
        """

        if self.currentIndex.isValid():
            self.setDisabled(False)
        else:
            self.setDisabled(True)