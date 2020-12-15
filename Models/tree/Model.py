from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import csv

from data_types.nodes import CompositeNodes as comp_nodes
from data_types.nodes.ComponentNode import ComponentNode
from data_types.trees.ComponentTree import ComponentTree

class TreeModel(qtc.QAbstractItemModel):
    """
    This class manages the tree model that stores the data for every project.
    It writes the structure in a .csv file and can also generate a tree structure
    reading the created file.
    """

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

    def __init__(self, filename = None):
        """
        Initialise the object parameters.
        If a filename is passed, the file is read and the data structure inside
        that file is extracted. If nothing is passed, creates a new root.

        Args:
            filename (str): name or path of the file to read. Default is None.
        """

        super(TreeModel, self).__init__()

        self.rootItem = ComponentNode()

        if filename:
            self.first = self.readFile(filename)
        else:
            self.first = comp_nodes.ProjectNode()

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
            column = self.HEADERS[index.column()]
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
            item.updateFeature(self.HEADERS[index.column()], value)
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
            return self.HEADERS[section].title()
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

        if parentItem == self.rootItem:
            return qtc.QModelIndex()

        row = parentItem.getIndex()
        return self.createIndex(row, 0, parentItem)

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

        return len(self.HEADERS)

    def insertRows(self, position, item, parent = qtc.QModelIndex()):
        """
        Insert a node row in the specified position.

        Args:
            position (int): the index where the item will be added
            item (ComponentNode): the node to add to the model
            parent (QModelIndex): the index of the parent item. Default is an invalid index

        Returns:
            bool: the success of the operation
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

    def saveFile(self, filename):
        """
        Saves the tree structure in a .csv file, given a proper filename.

        Args:
            filename (str): name or path of the file to save.
        """

        with open(filename, 'w') as file:
            fieldnames = self.HEADERS
            fullFieldnames = fieldnames.copy()
            fullFieldnames.extend(['selfHash', 'parentHash'])

            csv_writer = csv.DictWriter(file, fieldnames = fullFieldnames)
            csv_writer.writeheader()

            iterator = self.tree.iterPreorder()
            for node in iterator:
                nodeDict = node.getNodeDictionary(*fieldnames)
                nodeDict['selfHash'] = node.selfHash
                nodeDict['parentHash'] = node.parentHash

                csv_writer.writerow(nodeDict)

    def readFile(self, filename):
        """
        Reads a .csv file and transforms it, if possible, into a tree data structure.

        Args:
            filename (str): name or path of the file to read.
        """

        if filename:
            with open(filename, 'r') as file:
                csv_reader = csv.DictReader(file)

                firstLine = next(csv_reader)
                first = comp_nodes.ProjectNode()
                first.selfHash = int(firstLine['selfHash'])
                del firstLine['selfHash']
                del firstLine['parentHash']
                first.addFeatures(**firstLine)

                tempTree = ComponentTree(first)

                for line in csv_reader:
                    line = line.copy()
                    prefix = line['numberID'][1:4]
                    parent = tempTree.searchByHash(int(line['parentHash']))

                    newNode = self.getNodeByType(line['type'], prefix)
                    newNode = self.fillNode(newNode, line, parent)
                    parent.addChild(newNode)

            return first

    def getNodeByType(self, tp, prefix):
        """
        Returns the class of the correct node based on the type and the prefix
        of the node.

        Args:
            tp (str): the type of the node
            prefix (str): the prefix of the node

        Returns:
            class: the right class to initialize
        """

        nodes = {
            'Project': comp_nodes.ProjectNode,
            'Assembly': comp_nodes.AssemblyNode,
            'Part': comp_nodes.LeafNode,
            'Jig': comp_nodes.JigNode,
            'Placeholder': comp_nodes.PlaceholderNode,
            'Product': comp_nodes.ProductNode,
            'Hardware': self.chooseHardware(prefix)
        }

        return nodes[tp]

    def chooseHardware(self, prefix):
        """
        Returns the correct type of hardware node based on the pefix given.

        Args:
            prefix (str): the prefix of the node

        Returns:
            class: the class of the node to initialise
        """

        nodes = {
            'MEH': comp_nodes.HardwareNode,
            'ELH': comp_nodes.HardwareNode,
            'EMH': comp_nodes.HardwareNode,
            'MMH': comp_nodes.MeasuredNode
        }
        if prefix in nodes.keys():
            return nodes[prefix]

    def fillNode(self, nodeType, dataDict, parent = None):
        """
        Fills up a node with all the data needed.

        Args:
            nodeType (class): the class of the node
            dataDict (dict[str, str]): the dictionary with all the data
            parent (ComponentNode): the parent of the current node. Defaults to None.

        Returns:
            ComponentNode: the complete node with all the data
        """

        if dataDict['parentHash']:
            parentHash = int(dataDict['parentHash'])
        else: parentHash = 0

        if dataDict['selfHash']:
            selfHash = int(dataDict['selfHash'])
        else: selfHash = 0

        del dataDict['selfHash']
        del dataDict['parentHash']

        if dataDict['type'] in ['Assembly', 'Jig', 'Placeholder']:
            node = nodeType(parent.getLevel() + 1, **dataDict)
        else:
            node = nodeType(**dataDict)

        node.selfHash = selfHash
        node.parentHash = parentHash

        return node

# UTILITY

    def swapComponent(self, position, newNode, parent = qtc.QModelIndex()):
        """
        Removes a component and then adds another component in it's place.

        Args:
            position (int): the position of the component to swap.
            newNode (ComponentNode): the new component to add.
            parent (QModelIndex): the index of the parent item. Default is an invalid index.
        """

        self.removeRows(position, parent)
        self.insertRows(position, newNode, parent)

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
