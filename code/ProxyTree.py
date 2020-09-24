from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from util import _36ToBase10
from constants import COLUMN_LIST_TREE

class ProxyTree(qtc.QSortFilterProxyModel):
    """
    This class changes the way the tree data is displayed on the view. Only important
    information is shown in this page. A dictionary decides the columns to display.
    This class also provides sorting and filtering.
    """

    def __init__(self):
        super().__init__()

    def filterAcceptsColumn(self, source_column, source_parent):
        """
        Selects the columns to show from the original model.
        Filters out the unimportant columns.

        INPUT:
            int - source_column: current column
            QModelIndex - source_parent: index of the parent item

        RETURN TYPE:
            bool: whether to show or hide the column
        """

        if source_column not in COLUMN_LIST_TREE.keys():                       # if the column has to be hidden
            return False                                                        # returns False
        else:                                                                   # otherwise
            return True                                                         # returns True
    
    def filterAcceptsRow(self, source_row, source_parent):
        """
        Selects the rows to show from the original model.
        If the row is a deprecated item it is not displayed, when the option is toggled.

        INPUT:
            int - source_row: current row
            QModelIndex - source_parent: index of the parent item

        RETURN TYPE:
            bool: whether to show or hide the column
        """

        if source_parent.isValid() and self.filterRegExp().pattern() == 'Deprecated':
            status = source_parent.internalPointer().children[source_row].status
            if status == 'Deprecated':
                return False
            
        return True

    def lessThan(self, source_left, source_right):        
        """
        Returns true if the value of the item referred to by the given index source_left
        is less than the value of the item referred to by the given index source_right,
        otherwise returns false.

        INPUT:
            source_left – QModelIndex
            source_right – QModelIndex

        RETURN TYPE:
            bool
        """

        if source_left.column() == 0 and source_right.column() == 0:
            if source_left.isValid() and source_right.isValid():
                left = source_left.internalPointer() 
                left = left.number      
                left = left.replace('#', '')                         
                left = left.replace('-', '')
                left = _36ToBase10(left)                         

                right = source_right.internalPointer()
                right = right.number
                right = right.replace('#', '')
                right = right.replace('-', '')
                right = _36ToBase10(right)
                
                return left < right             
        return False                                    