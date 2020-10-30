from PyQt5 import QtCore as qtc
import re

from constants import COLUMN_LIST_HARDWARE


class HardwareProxyModel(qtc.QSortFilterProxyModel):
    """
    This class filters out the unwanted items (columns and rows) to display
    and also performs sorting.
    """

    def __init__(self):
        super().__init__()

    def filterAcceptsColumn(self, source_column, source_parent):
        """
        Selects the column to show from the original model.

        Args:
            source_column (int): current column index.
            source_parent (QModelIndex): index of the current parent item.

        Returns:
            bool: whether to show or hide the column.
        """

        if source_column not in COLUMN_LIST_HARDWARE.keys():
            return False
        else:
            return True

    def filterAcceptsRow(self, source_row, source_parent):
        """
        Selects the row to show from the original model.
        A regular expression selects the wanted rows.

        Custom functions:
            BaseNode.getChildAt()
            BaseNode.getNodeString()

        Args:
            source_row (int): current row index.
            source_parent (QModelIndex): index of the current parent item.

        Returns:
            bool: whether to show or hide the row.
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

        Custom functions:
            BaseNode.getSize()

        Args:
            source_left (QModelIndex): the left item of the model.
            source_right (QModelIndex): the right item of the model.

        Returns:
            bool: left > right.
        """

        if source_left.isValid() and source_left.column() == 0:
            left = source_left.internalPointer().getSize()
            right = source_right.internalPointer().getSize()

            return left > right
        return False
