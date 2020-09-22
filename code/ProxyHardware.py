from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import re

from util import _36ToBase10
from constants import COLUMN_LIST_HARDWARE

class HardwareProxyModel(qtc.QSortFilterProxyModel):
    """This class filters out the unwanted items to display and also performs sorting."""

    def __init__(self):
        super().__init__()

    def filterAcceptsColumn(self, source_column, source_parent):
        """
        Selects the column to show from the original model.

        INPUT:
            int - source_column: current column
            QModelIndex - source_parent: index of the parent item

        OUTPUT:
            bool: whether to show or hide the column
        """

        if source_column not in COLUMN_LIST_HARDWARE.keys():      
            return False                                    
        else:                                                 
            return True                               

    def filterAcceptsRow(self, source_row, source_parent):
        """
        Selects the row to show from the original model.
        A regular expression selects the wanted rows.

        INPUT:
            int - source_row: current row
            QModelIndex - source_parent: index of the parent item

        OUTPUT:
            bool: whether to show or hide the row
        """

        regexp = re.compile(self.filterRegExp().pattern(), re.I)      
        rowString = self.stringAtRow(source_row)               

        if regexp.search(rowString):                         
            return True                                           
        else:                                               
            return False                                   

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

        if source_left.isValid() and source_left.column() == 0:    
            left = source_left.internalPointer()                
            left = left['number']                                 
            left = left.replace('#', '')                       
            left = left.replace('-', '')
            left = _36ToBase10(left)                           

            right = source_right.internalPointer()        
            right = right['number']
            right = right.replace('#', '')
            right = right.replace('-', '')
            right = _36ToBase10(right)
            
            return left > right                                
        return False                                         

    def stringAtRow(self, row):
        """
        Returns a string of the current row, with a space separating each data field.
        This function is used to filter out the unwanted rows in the proxy model.

        INPUT:
            int - row: the selected row for the method to return the string

        RETURN TYPE:
            str: the returned row in string form
        """

        hList = self.sourceModel().hardwareList

        output = ''                                        
        if row < len(hList) and len(hList) > 0:            
            for key in hList[row].keys():                  
                output += ' ' + hList[row][key]                  
        return output                                          