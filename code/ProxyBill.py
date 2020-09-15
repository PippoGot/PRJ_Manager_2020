from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from constants import HEADERS as headers

class ProxyBill(qtc.QIdentityProxyModel):
    """
    Proxy model to remap the data of the component tree in a different view.
    Only displays one copy per element and elements of a certain type.
    """

    def __init__(self):
        super().__init__()

    def mapFromSource(self, sourceIndex):
        """
        Maps a source index to a proxy index.

        INPUT:
            QModelIndex - sourceIndex: the source index to map
        """

        if not sourceIndex.isValid(): return qtc.QModelIndex()

        element = sourceIndex.internalPointer()
        leafList = self.sourceModel().rootItem.get_unique_leaves_list()

        if element not in leafList: return qtc.QModelIndex()

        row = leafList.index(element)
        return self.createIndex(row, sourceIndex.column(), element)

    def mapToSource(self, proxyIndex):
        """
        Maps a proxy index to a source index.

        INPUT:
            QModelIndex - proxyIndex: the proxy index to map
        """

        if not proxyIndex.isValid(): return qtc.QModelIndex()
        
        element = proxyIndex.internalPointer()

        if not element or not element.up: return qtc.QModelIndex()

        row = element.up.children.index(element)
        
        return self.createIndex(row, proxyIndex.column(), element)

    def rowCount(self, parent):
        """
        Returns the number of rows under the given parent . When the parent is valid it means that is returning 
        the number of children of parent.

        PARAMETERS:
            parent – QModelIndex

        RETURN TYPE:
            int
        """

        if not parent.isValid():
            sourceModel = self.sourceModel()
            if sourceModel:
                leafList = sourceModel.rootItem.get_unique_leaves_list()
                return len(leafList)
        return 0

    def columnCount(self, parent):
        """
        Returns the number of columns for the children of the given parent .
        In most subclasses, the number of columns is independent of the parent .

        PARAMETERS:
            parent – QModelIndex

        RETURN TYPE:
            int
        """

        return len(headers)

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
        else:                                                                               # if the index is not valid
            parentItem = self.sourceModel().rootItem                                        # the parent item is set to the root item

        leafList = parentItem.get_unique_leaves_list()
        if row >= len(leafList) or row < 0: return qtc.QModelIndex()

        childItem = leafList[row]                                                           # the child item is the child of the parent item at the given index row

        if childItem:                                                                       # if the child item exists
            return self.createIndex(row, column, childItem)                                 # creates and returns it's index

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

        return qtc.QModelIndex()                                                            # an invalid index is return

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

        element = index.internalPointer()
        if element.level == 5:
            quantity = self.sourceModel().rootItem.calc_quantity(element)
        else:
            quantity = element.quantity

        if role == qtc.Qt.DisplayRole or role == qtc.Qt.EditRole:                           # then if the role is display or edit
            if index.column() == 9:
                return quantity
            return getattr(element, headers[index.column()], None)                             # returns the data stored under the given index

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
            return headers[section].title()                                                 # returns the root data under the given index
        return None  

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
            return qtc.Qt.NoItemFlags                                                       # returns NoItem
        else:
            return qtc.Qt.ItemIsEnabled