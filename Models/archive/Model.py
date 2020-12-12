from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import csv

from data_types.trees.ComponentTree import ComponentTree
from data_types.nodes.ComponentNode import ComponentNode
from data_types.nodes.CompositeNodes import ProjectNode

from models.tree.Model import TreeModel as TreeModel

class ArchiveModel(TreeModel):
    """
    Model for the hardware archive view. Subclass of ModelTree, reimplements
    data, remove/insert Rows and getNewNode to better suit the model and it's logic.
    """

    def __init__(self, filename = None):
        """
        Initialise the model. An optional filename can be passed to read a file.

        Args:
            filename (str): the name or path of the file. Defaults to None.
        """

        super().__init__(filename)
        self.rootItem = self.first

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

    def removeRows(self, indexes, parent = qtc.QModelIndex()):
        """
        Removes the selected rows from the archive model.

        Args:
            index (QModelIndex): the index of the item to remove
            parent (QModelIndex): the index of the parent of the node to delete. Defaults to qtc.QModelIndex().

        Returns:
            bool: the success of the operation
        """

        parentItem = self.rootItem

        for index in indexes:
            item = index.internalPointer()
            position = item.getIndex()

            self.beginRemoveRows(parent.siblingAtColumn(0), position, position)
            parentItem.removeChild(item)
            self.endRemoveRows()

        return True

    def insertRows(self, position, item, parent = qtc.QModelIndex()):
        """
        Insert a node row in the specified position.

        Args:
            node (ComponentNode): the node to add to the model

        Returns:
            bool: the success of the operation.
        """

        parentItem = self.rootItem

        self.beginInsertRows(qtc.QModelIndex(), position, position)
        success = parentItem.addChild(item)
        self.endInsertRows()

        return success

    def getNewNode(self, prefix):
        """
        Returns the new correct node to insert.

        Args:
            prefix (str): the prefix of the node to add

        Returns:
            ComponentNode: the next node to be added
        """

        return self.tree.getNewHardwareNode(prefix)