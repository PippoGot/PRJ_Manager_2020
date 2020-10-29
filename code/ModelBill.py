from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from ModelHardware import ModelHardware
from BaseNode import BaseNode

from constants import HEADERS


class ModelBill(ModelHardware):

    def __init__(self):
        super().__init__()
        self.rootItem = BaseNode()

# --- MODEL BILL ---

    def insertRows(self, node):
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
        parent = qtc.QModelIndex()

        self.beginRemoveRows(parent.siblingAtColumn(0), position, position)
        success = self.rootItem.popChild(position)
        self.endRemoveRows()

        return success

    def flags(self, index):
        return qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable

# REPRESENTATION

    def __repr__(self):
        """Enables the user to represent the model with the print() function."""

        return self.rootItem.toString(0, 'title', 'quantity')
