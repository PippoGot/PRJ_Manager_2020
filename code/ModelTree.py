from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import csv

from constants import HEADERS

from BaseNode import BaseNode
from CompositeNodes import ProjectNode, AssemblyNode, LeafNode, HardwareNode, MeasuredNode, JigNode, PlaceholderNode, ConsumableNode


class ModelTree(qtc.QAbstractItemModel):
    """
    This class manages the tree model that stores the data for every project.
    It can read and write the structure in a .csv file and can then generate a
    tree structure from it.
    """

    def __init__(self, filename=None):
        """
        Initialize the object parameters. If a filename is passed, the file
        is read and the data structure inside that file is extracted.
        If nothing is passed, creates a fresh root.

        INPUT:
            str - filename: filename to read
        """

        super(ModelTree, self).__init__()

        self.rootItem = BaseNode(number='root')

        if filename:
            self.first = self.readFile(filename)
        else:
            self.first = ProjectNode()

        self.rootItem.addChild(self.first)

# --- MODEL FUNCTIONS ---

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

        elif role == qtc.Qt.BackgroundRole:
            return item.getFeature('color')

    def setData(self, index, value, role=qtc.Qt.EditRole):
        """
        Sets the role data for the item at index to value .
        Returns true if successful; otherwise returns false .
        The dataChanged() signal should be emitted if the data was
        successfully set.
        The base class implementation returns false.
        This function and data() must be reimplemented
        for editable models.

        PARAMETERS:
            index – QModelIndex
            value – object
            role – int

        RETURN TYPE:
            bool
        """

        if index.isValid() and role == qtc.Qt.EditRole:
            item = index.internalPointer()
            item.updateFeature(HEADERS[index.column()], value)
            self.dataChanged.emit(index, index)
            return True
        return

    def flags(self, index):
        """
        Returns the item flags for the given index .
        The base class implementation returns a combination of flags
        that enables the item (ItemIsEnabled)
        and allows it to be selected (ItemIsSelectable ).

        PARAMETERS:
            index – QModelIndex

        RETURN TYPE:
            ItemFlags
        """

        condition = index.column() in [0, 3] or (index.column() == 4 and not index.internalPointer().getFeature('editableManufacture'))

        if not index.isValid():
            return qtc.Qt.NoItemFlags
        if condition:
            return qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable
        else:
            return qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEditable

    def headerData(self, section, orientation, role):
        """
        Turns the data for the given role and section in the header with the specified orientation .
        For horizontal headers, the section number corresponds to the column number. Similarly, for
        vertical headers, the section number corresponds to the row number.

        PARAMETERS:
            section – int
            orientation – Orientation
            role – int

        RETURN TYPE:
            object
        """

        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:
            return HEADERS[section].title()
        return None

    def index(self, row, column, parent):
        """
        Returns the index of the item in the model specified by the given row , column and parent index.
        When reimplementing this function in a subclass, call createIndex() to generate model indexes
        that other components can use to refer to items in your model.

        PARAMETERS:
            row – int
            column – int
            parent – QModelIndex

        RETURNS TYPE:
            QModelIndex
        """

        if not self.hasIndex(row, column, parent):
            return qtc.QModelIndex()
        elif not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.getChildAt(row)

        if childItem:
            return self.createIndex(row, column, childItem)

        return qtc.QModelIndex()

    def parent(self, index):
        """
        Returns the parent of the model item with the given index . If the item has no parent, an invalid
        QModelIndex is returned.
        A common convention used in models that expose tree data structures is that only items in the first
        column have children. For that case, when reimplementing this function in a subclass the column of
        the returned QModelIndex would be 0.
        When reimplementing this function in a subclass, be careful to avoid calling QModelIndex member
        functions, such as parent(), since indexes belonging to your model will simply call your implementation,
        leading to infinite recursion

        PARAMETERS:
            index – QModelIndex

        RETURN TYPE:
            QModelIndex
        """

        if not index.isValid():
            return qtc.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.getParent()

        if parentItem == self.rootItem:
            return qtc.QModelIndex()

        row = parentItem.getIndex()

        return self.createIndex(row, 0, parentItem)

    def rowCount(self, parent):
        """
        Returns the number of rows under the given parent . When the parent is valid it means that is returning
        the number of children of parent.

        PARAMETERS:
            parent – QModelIndex

        RETURN TYPE:
            int
        """

        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return len(parentItem.getChildren())

    def columnCount(self, parent):
        """
        Returns the number of columns for the children of the given parent .
        In most subclasses, the number of columns is independent of the parent .

        PARAMETERS:
            parent – QModelIndex

        RETURN TYPE:
            int
        """

        return len(HEADERS)

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

        if parent.isValid():
            parentItem = parent.internalPointer()
        else:
            parentItem = self.first

        self.beginInsertRows(parent.siblingAtColumn(0), position, position)

        success = parentItem.addChild(item)

        self.endInsertRows()

        return success

    def removeRows(self, position, parent=qtc.QModelIndex()):
        """
        Remove a number of rows in the specified position.

        PARAMETERS:
            position – int
            parent – QModelIndex

        RETURN TYPE:
            bool
        """

        if parent.isValid():
            parentItem = parent.internalPointer()
        else:
            parentItem = self.first

        self.beginRemoveRows(parent.siblingAtColumn(0), position, position)

        childItem = parentItem.getChildAt(position)
        success = childItem.detach()

        self.endRemoveRows()

        return success

# --- CUSTOM FUNCTIONS ---

# FILE MANAGEMENT

    fieldnames = [
        'parentHash',   # identity hash of the parent
        'selfHash',     # identity hash of this node
        'level',        # level of the node in the tree
        'number',       # number of the node
        'title',        # name of the node
        'description',  # description of the node
        'type',         # type of the node
        'manufacture',  # fabrication specifications
        'status',       # advancement of the node
        'comment',      # optional comment
        'price',        # the price of this node
        'quantity',     # the quantity of this node
        'package',      # the quantity per package of this node
        'seller',       # the seller of this component node
        'kit',          # group of component sold together
        'link',         # the link to the shopping website
        'length'        # for the measured hardware
    ]

    def saveFile(self, filename):
        """
        Saves the tree structure in a .csv file, given a proper filename.

        INPUT:
            str - filename: name of the file to read
        """

        with open(filename, 'w') as file:
            csv_writer = csv.DictWriter(file, fieldnames=self.fieldnames)

            csv_writer.writeheader()

            for node in self.first.iterDescendants():
                nodeDict = node.getNodeDictionary(*self.fieldnames)
                csv_writer.writerow(nodeDict)

    def exportBOM(self, filename):
        """
        Exports the bill of material of this model.

        INPUT:
            str - filename: the name of the file to create
        """

        # self.rootItem.export_bill(filename)
        pass

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

            first = ProjectNode()
            first.addFeatures(**next(csv_reader))

            for line in csv_reader:
                features = line.copy()
                del features['number']
                del features['level']

                new = self.fillNode(line['number'], line['level'], **features)
                new.addFeatures(**line)
                parent = first.searchNode(selfHash=line['parentHash'])

                if parent:
                    parent.addChild(new)

            return first

# UTILITY

    def swapComponent(self, position, newNode, parent=qtc.QModelIndex()):
        """
        Removes a component and then adds another component in it's place.

        INPUT:
            int - position: the position of the component to remove and to add
            ComponentTree - newNode: the component to add
            QModelIndex - parent: the index of the parent
        """

        self.removeRows(position, parent)
        self.insertRows(position, newNode, parent)

    def fillNode(self, number, level, **features):
        """
        Returns a filled node of the read type.

        Args:
            number (str): the number of the node
            level (int): the level of the node
            **features (kwargs): additional features to add

        Returns:
            BaseNode: the filled node
        """

        if level:
            level = int(level)
        else:
            level = 5

        tp = features['type']
        if number[1:4] == 'MMH':
            tp = 'Measured'

        typeDict = {
            'Project': ProjectNode(),
            'Assembly': AssemblyNode(number, level),
            'Part': LeafNode(number),
            'Hardware': HardwareNode(number),
            'Measured': MeasuredNode(number),
            'Consumable': ConsumableNode(number),
            'Jig': JigNode(number, level),
            'Placeholder': PlaceholderNode(number, level)
        }

        node = typeDict[tp]
        node.addFeatures(**features)

        return node

# REPRESENTATION

    def __repr__(self):
        """Enables the user to represent the model with the print() function."""

        return self.rootItem.toString(0, 'title')


if __name__ == '__main__':
    archive = ModelTree('code/resources/archive/HardwareArchive.csv')
    print(archive)

    archive.saveFile('archive.csv')
    newArchive = ModelTree('archive.csv')
    print(newArchive)
