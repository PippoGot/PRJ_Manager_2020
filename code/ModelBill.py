from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from ete3 import Tree
import csv
import math

class ModelBill(qtc.QAbstractItemModel):
    """
    This class manages the tree model that stores the data for every project.
    It can read and write the structure in a .csv file and can then generate a 
    tree structure from it.
    """

    def __init__(self):
        """
        Initialize the object parameters. If a filename is passed, the file is read and the data 
        structure inside that file is extracted. If nothing is passed, creates a fresh root. 

        INPUT:
            str - filename: filename to read

        PARAMETERS:
            Tree - self.rootItem: highest level object
            str - self.filename: name of the file for this model
        """

        super(ModelBill, self).__init__()

        self.rootItem = Tree()

    headers = {                                                                             # default values for the headers
        0: 'number',
        1: 'title', 
        2: 'description',
        3: 'priceUnit',
        4: 'quantity',
        5: 'quantityPackage',
        6: 'quantityOrder',
        7: 'totalPrice',
        8: 'seller',
        9: 'kit',
        10: 'link'
    }

# MODEL FUNCTIONS

    def data(self, index, role):
        """
        Returns the data stored under the given role for the item referred to by the index .
        
        PARAMETERS:
            index – QModelIndex
            role – int

        RETURN TYPE:
            object
        """

        if not index.isValid():                                                             # if the index is not valid
            return None                                                                     # returns None

        item = index.internalPointer()

        if role == qtc.Qt.DisplayRole:                                                      # then if the role is display or edit
            return getattr(item, self.headers[index.column()], None)                        # returns the data stored under the given index

    def flags(self, index):
        """
        Returns the item flags for the given index .
        The base class implementation returns a combination of flags that enables the item (ItemIsEnabled)
        and allows it to be selected (ItemIsSelectable ).

        PARAMETERS:
            index – QModelIndex

        RETURN TYPE:
            ItemFlags
        """

        if not index.isValid():                                                             # if the index is not valid                                                        
            return qtc.Qt.NoItemFlags                                                       # returns NoItemFlags
        # if index.column() == 1 or index.column() == 0:                                      # if the index column is either 0 or 1
        return qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable                           # the item is both enabled and selectable
        # else:                                                                               # otherwise
        #     return qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEditable   # the object is also editable

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

        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:                 # if the orientation is horizontal and the role is display
            return self.headers[section]                                                    # returns the root data under the given index
        return None                                                                         # otherwise returns None

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

        if not self.hasIndex(row, column, parent):                                          # if the given index doesn't exist
            return qtc.QModelIndex()                                                        # returns an invalid index
        elif not parent.isValid():                                                          # if the index is not valid
            parentItem = self.rootItem                                                      # the parent item is set to the root item
        else:                                                                               # otherwise
            parentItem = parent.internalPointer()                                           # parent item is the object at the given index

        childItem = parentItem.children[row]                                                # the child item is the child of the parent item at the given index row

        if childItem:                                                                       # if the child item exists
            return self.createIndex(row, column, childItem)                                 # creates and returns it's index

        return qtc.QModelIndex()                                                            # otherwise returns an invalid index

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

        if not index.isValid():                                                             # if the index is not valid
            return qtc.QModelIndex()                                                        # an invalid index is returned

        childItem = index.internalPointer()                                                 # otherwise the child item is the item of the given index
        parentItem = childItem.up                                                           # and the parent item is the child item parent

        if parentItem or parentItem == self.rootItem:                                       # if the parent is the root item
            return qtc.QModelIndex()                                                        # an invalid index is returned

        row = parentItem.up.children.index(parentItem)

        return self.createIndex(row, 0, parentItem)                            # otherwise it creates and returns the parent item index 

    def rowCount(self, parent):
        """
        Returns the number of rows under the given parent . When the parent is valid it means that is returning 
        the number of children of parent.

        PARAMETERS:
            parent – QModelIndex

        RETURN TYPE:
            int
        """

        if parent.column() > 0:                                                             # if the column is greater than 0
            return 0                                                                        # returns 0

        if not parent.isValid():                                                            # if the index is not valid
            parentItem = self.rootItem                                                      # the parent item is the root item
        else:                                                                               # otherwise
            parentItem = parent.internalPointer()                                           # the parent item is the item of the given index

        return len(parentItem.children)                                                     # then returns the number of children of parent item

    def columnCount(self, parent):
        """
        Returns the number of columns for the children of the given parent .
        In most subclasses, the number of columns is independent of the parent .

        PARAMETERS:
            parent – QModelIndex

        RETURN TYPE:
            int
        """

        return len(self.headers)

    def insertRows(self, item):
        """
        Insert a number of rows in the specified position.

        PARAMETERS:
            Tree - item: item to add

        RETURN TYPE:
            bool
        """

        parent = qtc.QModelIndex()
        parentItem = self.rootItem
        if item.status == 'Deprecated': return False

        p = item.up                                                                 # calculates the quantity of this item
        quantity = 1
        while p:
            status = getattr(p, 'status', '')
            if status == 'Deprecated': return False
            quantity *= int(p.quantity)
            p = p.up

        if item and self.rootItem.search_nodes(number = item.number):               # if the item is already in the list
            node = self.rootItem.search_nodes(number = item.number)[0]
            node.quantity += quantity                                               # the quantity is added

            position = node.up.children.index(node)                                 # and the item is updated
            index = self.createIndex(position, 0, node)
            self.calculatePrice(node)
            self.dataChanged.emit(index, index)

        else:                                                                       # if the item is new
            position = len(self.rootItem.children)

            self.beginInsertRows(parent.siblingAtColumn(0), position, position)

            node = Tree(name = item.number)                                         # a new item is added to the list
            for x in range(len(self.headers)):
                if x != 6 or x != 7:
                    value = getattr(item, self.headers[x], '')
                    setattr(node, self.headers[x], value)

            setattr(node, 'quantity', quantity)                                     # with the respective quantity previously calculated
            self.calculatePrice(node)
            parentItem.add_child(node)

            self.endInsertRows()

        return True

    def removeRows(self, item):
        """
        Remove a number of rows in the specified position.

        PARAMETERS:
            Tree - item: item to remove

        RETURN TYPE:
            bool
        """

        parent = qtc.QModelIndex()
        parentItem = self.rootItem

        p = item.up                                                                 # calculates the quantity of this item
        quantity = 1
        while p:
            quantity *= int(p.quantity)
            p = p.up

        if item and self.rootItem.search_nodes(number = item.number):               # if the item is already in the list
            node = self.rootItem.search_nodes(number = item.number)[0]
            node.quantity -= quantity                                               # the quantity is subtracted

            position = node.up.children.index(node)

            if node.quantity <= 0:                                                  # if the quantity reaches 0
                self.beginRemoveRows(parent.siblingAtColumn(0), position, position) # the item is removed

                parentItem.remove_child(node)

                self.endRemoveRows()
            else:                                                                   # otherwise the item is updated
                index = self.createIndex(position, 0, node)
                self.calculatePrice(node)
                self.dataChanged.emit(index, index)

        return True

# CUSTOM FUNCTIONS

    def recalculate(self, tree):
        self.rootItem = Tree()
        for leaf in tree.iter_search_nodes(level = 5):
            self.insertRows(leaf)

    def calculatePrice(self, node):
        quantityOrder = math.ceil(node.quantity / int(node.quantityPackage))

        setattr(node, 'quantityOrder', quantityOrder)

        totalPrice = quantityOrder * float(node.priceUnit)

        setattr(node, 'totalPrice', totalPrice)

    def exportBill(self, filename):

        bill = []
        line = []
        for x in range(len(self.headers)):
            line.append(self.headers[x])
        bill.append(line)

        for item in self.rootItem.iter_leaves():
            line = []
            for x in range(len(self.headers)):
                line.append(getattr(item, self.headers[x], ''))
            bill.append(line)

        with open(filename, 'w') as file:
            csv_writer = csv.writer(file)
            for line in bill:
                csv_writer.writerow(line)

