from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import csv

from ModelHardware import ModelHardware
from BaseNode import BaseNode


class ModelBill(ModelHardware):
    """
    Subclass of ModelHardware.

    This class reimplements insertRows() and flags() and adds removeRowsAtPosition().
    Items in the Bill list are not editable through their view!

    This is the model class for the list of the bill of material. Every item is taken only
    once and stored in the BaseNode rootItem children.
    """

    def __init__(self):
        """
        Calls the superclass constructor and resets the rootItem.
        """

        super().__init__()
        self.rootItem = BaseNode()

# --- MODEL BILL ---

    def insertRows(self, node):
        """
        Inserts a new component in the model or updates the existing one.
        If the new component has a quantity value of 0 the node is removed.

        Custom functions:
            BaseNode.getRoot()
            BaseNode.getFeature()
            BaseNode.searchNode()
            BaseNode.getTotalQuantity()
            BaseNode.getTotalCost()
            BaseNode.getIndex()
            BaseNode.getLength()
            BaseNode.copy()
            BaseNode.addFeatures()
            BaseNode.addChild()

            self.removeAtPosition()
            self.insertRows()

        Args:
            node (BaseNode): the node to add/update.

        Returns:
            bool: the success of the operation.
        """

        parent = qtc.QModelIndex()
        parentItem = self.rootItem

        number = node.getFeature('number')
        exists = self.rootItem.searchNode(number = number)

        root = node.getRoot()
        quantity = node.getTotalQuantity(root)
        price = node.getTotalCost(root)

        if exists:
            position = exists.getIndex()
            self.removeAtPosition(position)

            if quantity == 0: return

            return self.insertRows(node)

        else:
            position = self.rootItem.getLength()
            newNode = node.copy()
            newNode.addFeatures(
                quantity = quantity,
                price = price
            )

            self.beginInsertRows(parent.siblingAtColumn(0), position, position)
            success = parentItem.addChild(newNode)
            self.endInsertRows()
            return success
        return False

    def removeAtPosition(self, position):
        """
        Remove the node at the specified position.

        Custom functions:
            BaseNode.popChild()

        Args:
            position (int): the position of the node to remove.

        Returns:
            bool: the success of the removal.
        """

        parent = qtc.QModelIndex()

        self.beginRemoveRows(parent.siblingAtColumn(0), position, position)
        success = self.rootItem.popChild(position)
        self.endRemoveRows()

        return success

    def flags(self, index):
        """
        Defines what can be done with the model's items. In this case they are enabled
        and selectable.

        Args:
            index (QModelIndex): the index of the current.

        Returns:
            qtc.Flags: what can be done with the current item.
        """

        return qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable

    def saveFile(self, filename):
        """
        Exports the bill of material of this model. The output file is a .csv file.

        Custom functions:
            BaseNode.getNodesList()
            BaseNode.getNodeDictionary()

        Args:
            filename (str): the name or path of the file to create.
        """

        fieldnames = [
            'number',
            'title',
            'description',
            'type',
            'quantity',
            'price',
            'seller'
        ]

        with open(filename, 'w') as file:
            csv_writer = csv.DictWriter(file, fieldnames = fieldnames)

            csv_writer.writeheader()

            for node in self.rootItem.iterDescendants():
                line = node.getNodeDictionary(*fieldnames)
                csv_writer.writerow(line)

# REPRESENTATION

    def __repr__(self):
        """
        Enables the user to represent the model with the print() function.
        Prints the title and quantity value.

        Custom functions:
            BaseNode.toString()
        """

        return self.rootItem.toString(0, 'title', 'quantity')
