from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import csv

from ModelTree import ModelTree
from BaseNode import BaseNode

from constants import HEADERS


class ModelHardware(ModelTree):
    """
    Subclass of ModelTree.

    This class create a model from the hardware archive file. It also manages the
    data inside the model and let the user edit the archive file through the
    hardware editor.

    The tree structure is different from the original ModelTree. Every item
    of the hardware archive is a child of rootItem, so this model can be displayed
    (and should be dislpayed) in a TableView.

    Reimplements data(), insertRows(), removeRows(), readFile() ans saveFile().
    Adds getFilename()
    """

    def __init__(self, filename = None):
        """
        Reads the archive file and fills the model with the read data.

        Custom functions:
            self.readFile()

        Args:
            filename (str): the file name/path to read. Default at None.
        """

        super().__init__()

        if filename:
            self.filename = filename
        else:
            self.filename = 'code/resources/archive/HardwareArchive.csv'

        self.rootItem = self.readFile(self.filename)

    def data(self, index, role):
        """
        Returns the data stored under the given role for the item referred to
        by the index.

        Custom functions:
            BaseNode.getFeature()

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
            column = HEADERS[index.column()]
            return item.getFeature(column)

    def insertRows(self, position, item, parent = qtc.QModelIndex()):
        """
        Insert a node in the specified position.

        Custom functions:
            BaseNode.addChild()

        Args:
            position (int): the position where the item should be added.
            item (BaseNode): the item to add.
            parent (QModelIndex): the index of the parent of the item. Default at an invalid index.

        Returns:
            bool: the success of the operation.
        """

        parentItem = self.rootItem

        self.beginInsertRows(parent.siblingAtColumn(0), position, position)
        success = parentItem.addChild(item)
        self.endInsertRows()

        return success

    def removeRows(self, indexes, parent = qtc.QModelIndex()):
        """
        Remove the given indexes if present.

        Custom functions:
            BaseNode.getIndex()
            BaseNode.removeChild()

        Args:
            indexes (list[QModelIndex]): the list of indexes to remove.
            parent (QModelIndex): the index of the parent of the item. Default at an invalid index.

        Returns:
            bool: the result of the operation.
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

        Custom functions:
            BaseNode.addFeatures()
            BaseNode.copy()
            BaseNode.addChild()
            self.fillNode()

        Args:
            filename (str): name or path of the file to read.

        Returns:
            BaseNode: the tree extracted from the file.
        """

        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)

            first = BaseNode()
            first.addFeatures(**next(csv_reader))

            for line in csv_reader:
                features = line.copy()
                del features['number']
                del features['level']
                features['selfHash'] = int(features['selfHash'])
                features['parentHash'] = int(features['parentHash'])

                new = self.fillNode(line['number'], line['level'], **features)
                first.addChild(new)

            return first

    def saveFile(self, filename):
        """
        Saves the tree structure in a .csv file, given a proper filename.

        Custom functions:
            BaseNode.iterDescendants()
            BaseNode.getNodeDictionary()

        Args:
            filename (str): name of the file to save.
        """

        with open(filename, 'w') as file:
            csv_writer = csv.DictWriter(file, fieldnames=self.fieldnames)

            csv_writer.writeheader()

            for node in self.rootItem.iterDescendants():
                nodeDict = node.getNodeDictionary(*self.fieldnames)
                csv_writer.writerow(nodeDict)

    def getFilename(self):
        """
        Returns the filename of this model.

        Returns:
            str: the filename of this model.
        """

        return self.filename




# HELPER CODE

if __name__ == '__main__':
    archive = ModelHardware()
    print(archive)
    archive.saveFile('archive.csv')
    newArchive = ModelHardware('archive.csv')
    print(newArchive)