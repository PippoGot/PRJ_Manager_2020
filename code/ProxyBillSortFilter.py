from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from constants import COLUMN_LIST_BILL

class ProxyBillSortFilter(qtc.QSortFilterProxyModel):
    """Class for the filtering of unwanted columns for the bill page."""

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

        if source_column not in COLUMN_LIST_BILL.keys():                    
            return False                                                 
        else:                                                           
            return True                                                  
