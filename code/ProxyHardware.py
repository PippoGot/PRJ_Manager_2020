from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from util import _36ToBase10
import re

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

        if source_column not in self.listaColonne.keys():           # if the column has to be hidden
            return False                                            # returns False
        else:                                                       # otherwise
            return True                                             # returns True

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

        regexp = re.compile(self.filterRegExp().pattern())          # gets the regular expression for the filtering
        rowString = self.sourceModel().stringAtRow(source_row)      # and the string of the current row
    
        if regexp.search(rowString):                                # if the current row matches the regular expression
            return True                                             # returns True, so the row is shown
        else:                                                       # otherwise
            return False                                            # returns false

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

        if source_left.isValid() and source_left.column() == 0:     # if the left index is valid and the column is 0
            left = source_left.internalPointer()                    # gets the left item
            left = left['number']                                   # extracts it's number
            left = left.replace('#', '')                            # removes the non-number characters
            left = left.replace('-', '')
            left = _36ToBase10(left)                                # and converts the number to decimal

            right = source_right.internalPointer()                  # repeat for the right item
            right = right['number']
            right = right.replace('#', '')
            right = right.replace('-', '')
            right = _36ToBase10(right)
            
            return left > right                                     # then return left > right
        return False                                                # otherwise returns False

    listaColonne = {                                                # the dictionary containing the columns to be shown
        0: 'number', 
        2: 'name',
        3: 'description',
        4: 'type',
        5: 'manufacture',
        8: 'price/unit',
        10: 'qtyx',
        11: 'seller',
        13: 'link'
    }