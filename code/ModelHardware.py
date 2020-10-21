from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import csv

from ModelTree import ModelTree
from BaseNode import BaseNode

from constants import HEADERS


class ModelHardware(ModelTree):
    """
    This class create a model from the hardware archive file. It also manages the
    data inside the model and let the user edit the archive file from the hardware editor.
    """

    def __init__(self):
        """Reads the archive file."""

        super().__init__()

        self.rootItem = self.readFile('code/resources/archive/HardwareArchive.csv')

    def data(self, index, role):
        """
        Returns the data stored under the given role for the item referred to
        by the index .

        PARAMETERS:
            index – QModelIndex
            role – int

        RETURN TYPE:
            object
        """

        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == qtc.Qt.DisplayRole or role == qtc.Qt.EditRole:
            column = HEADERS[index.column()]
            return item.getFeature(column)

    def insertRows(self, position, item, parent=qtc.QModelIndex()):
        """
        Insert a number of rows in the specified position.

        PARAMETERS:
            position – int
            item – ComponentTree
            parent – QModelIndex

        RETURN TYPE:
            bool
        """

        parentItem = self.rootItem

        self.beginInsertRows(parent.siblingAtColumn(0), position, position)

        success = parentItem.addChild(item)

        self.endInsertRows()

        return success

    def removeRows(self, indexes, parent=qtc.QModelIndex()):
        """
        Remove a number of rows in the specified position.

        PARAMETERS:
            position – int
            parent – QModelIndex

        RETURN TYPE:
            bool
        """

        parentItem = self.rootItem

        for index in indexes:
            item = index.internalPointer()
            position = item.getIndex()

            self.beginRemoveRows(parent.siblingAtColumn(0), position, position)

            parentItem.removeChild(item)

            self.endRemoveRows()

        return True

    def readFile(self, filename):
        """
        Reads a .csv file and transforms it, if possible, into a tree data structure.

        INPUT:
            str - filename: name of the file to read

        RETURN TYPE:
            ComponentTree: the tree extracted from the file
        """

        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)

            first = BaseNode()
            first.addFeatures(**next(csv_reader))

            for line in csv_reader:
                features = line.copy()
                del features['number']
                del features['level']
                new = self.fillNode(line['number'], line['level'], **features)
                new.addFeatures(**line)
                first.addChild(new)

            return first


if __name__ == '__main__':
    archive = ModelHardware()
    print(archive)