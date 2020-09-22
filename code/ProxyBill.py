from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from constants import HEADERS
from constants import TYPE_COLORS

class ProxyBill(qtc.QIdentityProxyModel):
    """
    Proxy model to remap the data of the component tree in a different view.
    Only displays one copy per element and elements of a certain type.
    """

    def __init__(self):
        super().__init__()

    def rowCount(self, parent):
        """
        Returns the number of rows under the given parent . When the parent is valid it means that is returning 
        the number of children of parent.

        PARAMETERS:
            parent – QModelIndex

        RETURN TYPE:
            int
        """
        
        return len(self.sourceModel().rootItem.search_nodes(level = 5))

    # def columnCount(self, parent):
    #     """
    #     Returns the number of columns for the children of the given parent .
    #     In most subclasses, the number of columns is independent of the parent .

    #     PARAMETERS:
    #         parent – QModelIndex

    #     RETURN TYPE:
    #         int
    #     """
    #     pass

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

        childItem = self.sourceModel().rootItem.search_nodes(level = 5)[row]                                         

        if childItem:                                                           
            return self.createIndex(row, column, childItem)                    

        return qtc.QModelIndex() 

    # def parent(self, index):
    #     """
    #     Returns the parent of the model item with the given index . If the item has no parent, an invalid 
    #     QModelIndex is returned.
    #     A common convention used in models that expose tree data structures is that only items in the first
    #     column have children. For that case, when reimplementing this function in a subclass the column of 
    #     the returned QModelIndex would be 0.
    #     When reimplementing this function in a subclass, be careful to avoid calling QModelIndex member 
    #     functions, such as parent(), since indexes belonging to your model will simply call your implementation,
    #     leading to infinite recursion
        
    #     PARAMETERS:
    #         index – QModelIndex

    #     RETURN TYPE:
    #         QModelIndex
    #     """

    def data(self, index, role):        
        """
        Returns the data stored under the given role for the item referred to by the index .
        
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
            if column == 'quantity':
                return self.sourceModel().rootItem.calc_quantity(item)
            return getattr(item, column, None)                 
        elif role == qtc.Qt.BackgroundRole:
            tp = item.type
            if tp == 'Assembly':
                tp += str(item.level - 1)
            return TYPE_COLORS[tp]

    # def headerData(self, section, orientation, role):
    #     """
    #     Turns the data for the given role and section in the header with the specified orientation .
    #     For horizontal headers, the section number corresponds to the column number. Similarly, for 
    #     vertical headers, the section number corresponds to the row number.

    #     PARAMETERS:
    #         section – int
    #         orientation – Orientation
    #         role – int

    #     RETURN TYPE:
    #         object
    #     """
    #     pass

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

        return qtc.Qt.ItemIsEnabled