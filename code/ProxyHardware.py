from PyQt5 import QtCore as qtc
import re

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
        root = self.sourceModel().rootItem
        item = root.getChildAt(source_row)
        rowString = ''

        if item:
            rowString = item.getNodeString()

        if regexp.search(rowString) or item == root:
            return True
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
            left = source_left.internalPointer().getSize()
            right = source_right.internalPointer().getSize()

            return left > right
        return False
