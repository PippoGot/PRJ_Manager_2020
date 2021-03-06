from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from data_types.nodes import CompositeNodes as comp_nodes
from models.archive.Model import ArchiveModel
from ...widgets.component_editor.ComponentEditor import ComponentEditor
from ...widgets.archive_view.ArchiveView import ArchiveView
from ...popups.hardware_selector.HardwareSelector import HardwareSelector

from .archive_page import Ui_uiArchivePage as ui

class ArchivePage(qtw.QWidget, ui):
    """
    Main hardware editor page. Uses a ComponentEditor widget and an ArchiveView widget.
    Offers the possibility to edit the items in the current archive file, add them or
    delete them.
    """

    def __init__(self):
        """
        Loads the UI window, initialise the class variables and connects
        the buttons to the proper slots.
        """

        super(ArchivePage, self).__init__()
        self.setupUi(self)

        self.uiArchiveView = ArchiveView()
        self.uiEditor = ComponentEditor()

        self.model = None
        self.manufactureModel = None
        self.statusModel = None
        self.currentIndex = qtc.QModelIndex()
        self.currentSelection = None
        self.newNode = None
        self.prefix = 'MEH'
        self.filename = None

        self.layout().insertWidget(1, self.uiArchiveView)
        self.layout().insertWidget(2, self.uiEditor)

        self.uiAddBtn.clicked.connect(self._addNode)
        self.uiDelBtn.clicked.connect(self._deleteNode)
        self.uiArchiveView.indexChanged.connect(self.setCurrentIndex)
        self.uiArchiveView.selectionChanged.connect(self.setCurrentSelection)
        self.uiArchiveView.filterChanged.connect(self._updateNewNode)

        self._disableRemove()

# --- MODELS ---

    def setModel(self, model):
        """
        Sets the editor's and view's model.

        Args:
            model (ModelTree): the model of the view and editor widget
            filename (str): the archive path or name. Default to None.
        """

        self.model = model
        self.uiArchiveView.setModel(self.model)
        self.uiEditor.setModel(self.model)

        if self.model:
            self.model.dataChanged.connect(self._saveArchive)

        self._updateNewNode()

    def setManufactureModel(self, manufactureModel):
        """
        Sets the editor's manufacture combobox model.

        Args:
            manufactureModel (ModelCombobox): the model of the combobox
        """

        self.manufactureModel = manufactureModel
        self.uiEditor.setManufactureModel(manufactureModel)
        self.editable.setModel(self.manufactureModel)

    def setStatusModel(self, statusModel):
        """
        Sets the editor's status combobox model.

        Args:
            statusModel (ModelCombobox): the model of the combobox
        """

        self.statusModel = statusModel
        self.uiEditor.setStatusModel(statusModel)
        self.uiStatus.setModel(self.statusModel)

# --- SELECTION ---

    def setCurrentIndex(self, index):
        """
        Updates the currently selected model index for the editor.

        Args:
            index (QModelIndex): the new index
        """

        self.uiEditor.setCurrentSelection(index)
        self.currentIndex = index
        self._disableRemove()

    def setCurrentSelection(self, selectionList):
        """
        Updates the currently selected list of indexes.

        Args:
            selectionList (list[QModelIndex]): the list of selected indexes
        """

        self.currentSelection = selectionList

# --- NODES ---

    def _addNode(self):
        """
        Adds a node to the archive model. The node will have the values on the editor
        when the add button is pressed. Then a new node replaces the one just added.
        """

        dataDict = self._gatherData()
        self.newNode.addFeatures(**dataDict)
        self.model.insertRows(len(self.model.rootItem), self.newNode)

        self._updateNewNode()
        self._saveArchive()

    def _gatherData(self):
        """
        Gathers all the current data in the new node editor in a dictionary.

        Returns:
            dict[str, PyObject]: the dictionary with all the gathered data
        """

        data = {
            'name': self.uiName.text(),
            'description': self.uiDescription.toPlainText(),
            'status': self.uiStatus.currentText(),
            'comment': self.uiComment.toPlainText(),
            'price': self.uiPrice.text(),
            'quantity': self.uiQuantity.text(),
            'package': self.uiQuantityPackage.text(),
            'seller': self.uiSeller.text(),
            'link': self.uiLink.toPlainText()
        }

        if self.newNode.isEditable():
            data['manufacture'] = self.editable.currentText()

        return data

    def _deleteNode(self):
        """
        Removes the currently selected node from the archive model.
        Then the indexes are reset, the widgets disabled and the new node
        updated.
        """

        indexes = []
        if not self.currentSelection:
            indexes.append(self.currentIndex)
        else:
            for index in self.currentSelection:
                newIndex = index.siblingAtColumn(0)
                if newIndex not in indexes:
                    indexes.append(newIndex)

        self.model.removeRows(indexes)

        self.currentIndex = qtc.QModelIndex()
        self.currentSelection = None

        self.uiEditor.setCurrentSelection(self.currentIndex)
        self._disableRemove()
        self._updateNewNode()
        self._saveArchive()

# --- GETTERS ---

    def getModel(self):
        """
        Returns the current model.

        Returns:
            ArchiveModel: the current model
        """

        return self.model

    def getNodes(self):
        """
        Returns a list of the nodes inside the archive model.

        Returns:
            list[ComponentNode]: the list of nodes inside the model
        """

        return self.model.rootItem.getChildren()

# --- UTILITY ---

    def _disableRemove(self):
        """
        Disables the delete button based on the current selection.
        """

        self.uiDelBtn.setDisabled(not self.currentIndex)

    def _updateNewNode(self, prefix = None):
        """
        Updates the fields with a fresh node that follows the order or replaces
        a gap of the already inserted ones.

        Args:
            prefix (str): the string that will determine the type of the node. Defaults to None.
        """

        if prefix:
            self.prefix = prefix

        classes = {
            'MEH': 'MechanicalNode',
            'ELH': 'ElectricalNode',
            'EMH': 'ElectromechanicalNode',
            'MMH': 'MeasuredNode',
            'PRO': 'ProductNode'
        }
        parent = self.currentIndex.internalPointer()

        self.newNode = self.model.getNewNode(parent, classes[self.prefix])

        self.uiNumberID.setText(self.newNode.getFeature('ID'))
        self.uiName.setText(self.newNode.getFeature('name'))
        self.uiDescription.setPlainText(self.newNode.getFeature('description'))
        self.uiComment.setPlainText(self.newNode.getFeature('comment'))
        self.uiPrice.setText(self.newNode.getFeature('price'))
        self.noneditable.setText(self.newNode.getFeature('manufacture'))
        self.uiType.setText(self.newNode.getFeature('type'))
        self.uiSeller.setText(self.newNode.getFeature('seller'))
        self.uiLink.setText(self.newNode.getFeature('link'))

    def _saveArchive(self):
        """
        Saves the arcvhive file.
        """

        self.model.saveFile(self.filename)

    def readArchive(self, filename = None):
        """
        Reads a file if one is passed in, and converts it to an archive model.

        Args:
            filename (str): the filename of the file to read. Defaults to None.
        """

        self.filename = filename
        self.setModel(ArchiveModel(filename))

    def getSelector(self):
        """
        Returns a hardware selector with the same model of the archive page.

        Returns:
            QWidget: the hardware selector
        """

        selector = HardwareSelector()
        selector.setModel(self.model)
        return selector
