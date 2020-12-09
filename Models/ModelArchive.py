from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from Data.Trees.ComponentTree import ComponentTree
from Data.Nodes.ComponentNode import ComponentNode

from Models.ModelTree import ModelTree

class ModelArchive(ModelTree):
    def __init__(self, filename = None):
        super().__init__()

        self.rootItem = ComponentNode()
        self.tree = ComponentTree(self.rootItem)

        if filename:
            self.readFile(filename)

    def data(self, index, role):
        """
        Returns the data stored under the given role for the item referred to
        by the index.

        Args:
            index (QModelIndex): the index of the item currently examined.
            role (int): the enum to apply to the item.

        Returns:
            PyObject: the object to display or the thing to do.
        """

        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == qtc.Qt.DisplayRole or role == qtc.Qt.EditRole:
            column = self.HEADERS[index.column()]
            return item.getFeature(column)

    def removeRows(self, index, parent = qtc.QModelIndex()):
        """
        Removes the selected rows from the archive model.

        Args:
            index (QModelIndex): the index of the item to remove
            parent (QModelIndex): the index of the parent of the node to delete. Defaults to qtc.QModelIndex().

        Returns:
            bool: the success of the operation
        """

        parentItem = self.rootItem
        item = index.internalPointer()
        position = item.getIndex()

        self.beginRemoveRows(parent.siblingAtColumn(0), position, position)
        parentItem.removeChild(item)
        self.endRemoveRows()

        return True