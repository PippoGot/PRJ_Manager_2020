from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import csv

from Data.Nodes import CompositeNodes as cnode
from Data.Nodes.ComponentNode import ComponentNode
from Data.Trees.ComponentTree import ComponentTree

HEADERS = [
    'numberID',
    'name',
    'description',
    'type',
    'manufacture',
    'status',
    'comment',
    'price',
    'quantity',
    'packageQuantity',
    'seller',
    'link',
]

class ModelTree(qtc.QAbstractItemModel):
    """
    This class manages the tree model that stores the data for every project.
    It writes the structure in a .csv file and can also generate a tree structure
    reading the created file.
    """

    def __init__(self, filename = None):
        """
        Initialise the object parameters.
        If a filename is passed, the file is read and the data structure inside
        that file is extracted. If nothing is passed, creates a new root.

        Args:
            filename (str): name or path of the file to read. Default is None.
        """

        super(ModelTree, self).__init__()

        self.rootItem = ComponentNode()

        # if filename:
        #     self.first = self.readFile(filename)
        # else:
        #     self.first = ProjectNode()
        self.first = cnode.ProjectNode()
        self.tree = ComponentTree(self.first)

        self.rootItem.addChild(self.first)

# --- MODEL FUNCTIONS ---

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
            column = HEADERS[index.column()]
            return item.getFeature(column)

        elif role == qtc.Qt.BackgroundRole:
            return item.color

        elif role == qtc.Qt.DecorationRole and index.column() == 0:
            return item.icon

    def setData(self, index, value, role = qtc.Qt.EditRole):
        """
        Used to edit and update the model items values.

        Args:
            index (QModelIndex): the index of the edited item.
            value (PyObject): the new field value.
            role (int): the action currently performed to the item. Default is EditRole.

        Returns:
            bool: the success of the operation.
        """

        if index.isValid() and role == qtc.Qt.EditRole:
            item = index.internalPointer()
            item.updateFeature(HEADERS[index.column()], value)
            self.dataChanged.emit(index, index)
            return True
        return

    def flags(self, index):
        """
        Returns the item flags for the given index. This tells the program
        what can be done with the model items.
        Numbers, types and some manufactures of the items are non-editable fields,
        the other fields are editable.

        Args:
            index – QModelIndex

        Returns:
            ItemFlags
        """

        if not index.isValid():
            return qtc.Qt.NoItemFlags
        if index.column() in [0, 3]:
            return qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable
        elif index.column() == 4 and not index.internalPointer().isEditable():
            return qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable
        else:
            return qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEditable

    def headerData(self, section, orientation, role):
        """
        Turns the data for the given role and section in the header with the specified orientation.
        For horizontal headers, the section number corresponds to the column number. Similarly, for
        vertical headers, the section number corresponds to the row number.
        The headers are taken from a list of string values.

        Args:
            section (int): the current column.
            orientation (Orientation): horizontal or vertical.
            role (int): the action currently performed.

        Returns:
            PyObject: the object to display or the action to perform.
        """

        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:
            return HEADERS[section].title()
        return None

    def index(self, row, column, parent):
        """
        Returns the index of the item in the model specified by the given row, column and parent index.
        When reimplementing this function in a subclass, call createIndex() to generate model indexes
        that other components can use to refer to items in your model.

        Args:
            row (int): the item row.
            column (int): the item column.
            parent (QModelIndex): the item parent index.

        Returns:
            QModelIndex: the new index created.
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
        Returns the parent index of the model item with the given index. If the item has no parent,
        an invalid QModelIndex is returned.
        A common convention used in models that expose tree data structures is that only items in the first
        column have children. For that case, when reimplementing this function in a subclass the column of
        the returned QModelIndex would be 0.
        When reimplementing this function in a subclass, be careful to avoid calling QModelIndex member
        functions, such as parent(), since indexes belonging to your model will simply call your implementation,
        leading to infinite recursion.

        Args:
            index (QModelIndex): the index of the child item.

        Returns:
            QModelIndex: the index of the parent node for the given item.
        """

        if not index.isValid():
            return qtc.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.getParent()

        if parentItem:
            row = parentItem.getIndex()
            return self.createIndex(row, 0, parentItem)

        return qtc.QModelIndex()

    def rowCount(self, parent):
        """
        Returns the number of rows under the given parent. When the parent is valid it means
        that is returning the number of children of parent.

        Args:
            parent (QModelIndex): the index of the current item.

        Returns:
            int: the number of children of the current item.
        """

        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return len(parentItem)

    def columnCount(self, parent):
        """
        Returns the number of columns for the children of the given parent.
        In most subclasses, the number of columns is independent of the parent.

        Args:
            parent (QModelIndex): the currently examined item.

        Returns:
            int: the number of columns of this item.
        """

        return len(HEADERS)

    def insertRows(self, position, item, parent = qtc.QModelIndex()):
        """
        Insert a node row in the specified position.

        Args:
            position (int): the index where the item will be added.
            item (BaseNode): the node to add to the model.
            parent (QModelIndex): the index of the parent item. Default is an invalid index.

        Returns:
            bool: the success of the operation.
        """

        if parent.isValid():
            parentItem = parent.internalPointer()
        else:
            parentItem = self.first

        self.beginInsertRows(parent.siblingAtColumn(0), position, position)

        success = parentItem.addChild(item)
        self.tree.updateHashes(parentItem)

        self.endInsertRows()

        return success

    def removeRows(self, position, parent = qtc.QModelIndex()):
        """
        Remove the row in the specified position.

        Args:
            position (int): the index of the node to remove.
            parent (QModelIndex): the index of the parent item.

        Returns:
            bool: the success of the operation.
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

    def getNewNode(self, parent, tp):
        """
        Returns the next new node to be added to the tree with the right number and level.

        Args:
            parent (ComponentNode): the parent of the node that would be added
            tp (str): the type of node to be added

        Returns:
            ComponentNode: the node that would be added with default values and the correct number and level
        """

        return self.tree.getNewNode(parent, tp)

# FILE MANAGEMENT

    # fieldnames = [
    #     'parentHash',   # identity hash of the parent
    #     'selfHash',     # identity hash of this node
    #     'level',        # level of the node in the tree
    #     'number',       # number of the node
    #     'title',        # name of the node
    #     'description',  # description of the node
    #     'type',         # type of the node
    #     'manufacture',  # fabrication specifications
    #     'status',       # advancement of the node
    #     'comment',      # optional comment
    #     'price',        # the price of this node
    #     'quantity',     # the quantity of this node
    #     'package',      # the quantity per package of this node
    #     'seller',       # the seller of this component node
    #     'link',         # the link to the shopping website
    #     'length'        # for the measured hardware
    # ]

    # def saveFile(self, filename):
    #     """
    #     Saves the tree structure in a .csv file, given a proper filename.

    #     Custom functions:
    #         BaseNode.iterDescendants()
    #         BaseNode.getNodeDictionary()

    #     Args:
    #         filename (str): name or path of the file to save.
    #     """

    #     with open(filename, 'w') as file:
    #         csv_writer = csv.DictWriter(file, fieldnames = self.fieldnames)

    #         csv_writer.writeheader()

    #         for node in self.first.iterDescendants():
    #             nodeDict = node.getNodeDictionary(*self.fieldnames)
    #             csv_writer.writerow(nodeDict)

    def readFile(self, filename):
        """
        Reads a .csv file and transforms it, if possible, into a tree data structure.

        Args:
            filename (str): name or path of the file to read.
        """

        self.tree = self.tree.readFile(filename)
        self.rootItem = self.tree.getRoot()

# UTILITY

    def swapComponent(self, position, newNode, parent = qtc.QModelIndex()):
        """
        Removes a component and then adds another component in it's place.

        Custom functions:
            self.removeRows()
            self.insertRows()

        Args:
            position (int): the position of the component to swap.
            newNode (BaseNode): the new component to add.
            parent (QModelIndex): the index of the parent item. Default is an invalid index.
        """

        self.removeRows(position, parent)
        self.insertRows(position, newNode, parent)

    # def getBillNodes(self):
    #     """
    #     Returns a list of nodes to save in the bill of materials. Children of deprecated
    #     nodes wont be included.

    #     Returns:
    #         list[BaseNode]: the list of nodes to write in the bill of material.
    #     """

    #     nodesList = self.rootItem.getNodesList(level = 5)

    #     for node in nodesList:
    #         for parentNode in node.iterAncestor():
    #             if parentNode.getFeature('status') == 'Deprecated': nodesList.remove(node)

    #     return nodesList

# REPRESENTATION

    def __repr__(self):
        """
        Enables the user to represent the model with the print() function.

        Custom functions:
            BaseNode.toString()

        Returns:
            str: the string of the current rootItem object.
        """

        return self.tree.toString()
