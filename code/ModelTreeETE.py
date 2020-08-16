from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from ComponentTree import ComponentTree
import csv
from util import increment_number, headers
from ModelBill import ModelBill

class ModelTree(qtc.QAbstractItemModel):
    """
    This class manages the tree model that stores the data for every project.
    It can read and write the structure in a .csv file and can then generate a 
    tree structure from it.
    """

    def __init__(self, filename = None):
        """
        Initialize the object parameters. If a filename is passed, the file is read and the data 
        structure inside that file is extracted. If nothing is passed, creates a fresh root. 

        INPUT:
            str - filename: filename to read

        PARAMETERS:
            Tree - self.rootItem: highest level object
            str - self.filename: name of the file for this model
        """

        super(ModelTree, self).__init__()

        # self.bill = ModelBill()
        self.rootItem = ComponentTree('root')
        # setattr(self.rootItem, 'quantity', 1)

        if filename:                                                                        # creates the first item in one of two ways
            self.first = self.readFile(filename)                                            # from a file
        else:
            self.first = ComponentTree('#000-000', self.base)                                                             # or by deafult
            
        setattr(self.first, 'level', 1)

        self.rootItem.add_child(self.first)

        # self.bill.recalculate(self.first)

    headers = headers

    base = {                                                                                # default values for the first node
        'number': '#000-000', 
        'parent': '',
        'title': 'no name', 
        'description': 'no description',
        'type': 'no class',
        'manufacture': 'no material',
        'status': 'no status',
        'comment':'...',
        'priceUnit': 0,
        'quantity': 1,
        'quantityPackage': 1,
        'seller': '...',
        'kit': '-',
        'link': '-'
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

        if role == qtc.Qt.DisplayRole or role == qtc.Qt.EditRole:                           # then if the role is display or edit
            return getattr(item, self.headers[index.column()], None)                        # returns the data stored under the given index

    def setData(self, index, value, role = qtc.Qt.EditRole):
        """
        Sets the role data for the item at index to value .
        Returns true if successful; otherwise returns false .
        The dataChanged() signal should be emitted if the data was successfully set.
        The base class implementation returns false . This function and data() must be reimplemented
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
            setattr(item, self.headers[index.column()], value)
            # self.bill.recalculate(self.first)
            self.dataChanged.emit(index, index)
            return True
        return 

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
        if index.column() == 1 or index.column() == 0:                                      # if the index column is either 0 or 1
            return qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable                           # the item is both enabled and selectable
        else:                                                                               # otherwise
            return qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEditable   # the object is also editable

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
            return self.headers[section].title()                                                    # returns the root data under the given index
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

        if parentItem == self.rootItem:                                                     # if the parent is the root item
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

    def insertRows(self, position, item, parent = qtc.QModelIndex()):
        """
        Insert a number of rows in the specified position.

        PARAMETERS:
            position – int
            rows – int
            parent – QModelIndex

        RETURN TYPE:
            bool
        """

        if parent.isValid():
            parentItem = parent.internalPointer()
        else:
            parentItem = self.first

        self.beginInsertRows(parent.siblingAtColumn(0), position, position)

        setattr(item, 'level', parentItem.level + 1)
        setattr(item, 'parent', parentItem.number)
        success = parentItem.add_child(item)

        self.endInsertRows()

        return success

    def removeRows(self, position, parent = qtc.QModelIndex()):
        """
        Remove a number of rows in the specified position.

        PARAMETERS:
            position – int
            rows – int
            parent – QModelIndex

        RETURN TYPE:
            bool
        """

        if parent.isValid():
            parentItem = parent.internalPointer()
        else:
            parentItem = self.first

        self.beginRemoveRows(parent.siblingAtColumn(0), position, position)

        childItem = parentItem.children[position]
        parentItem.remove_child(childItem)

        self.endRemoveRows()

        return True

# CUSTOM FUNCTIONS

    def saveFile(self, filename):
        """
        Saves the tree structure in a .csv file, given a proper filename.
        
        INPUT:
            str - filename: name of the file to read
        """

        self.rootItem.save_file(filename)

    def readFile(self, filename):
        """
        Reads a .csv file and transforms it, if possible, into a tree data structure.

        INPUT:
            str - filename: name of the file to read

        OUTPUT:
            Tree: tree extracted from thew file
        """

        return self.rootItem.read_file(filename)

    def __repr__(self):
        """Enables the user to represent the model with the print() function."""

        return str(self.rootItem.get_ascii(attributes=['name', 'number', 'level'], show_internal=True))