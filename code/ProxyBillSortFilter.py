from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from constants import COLUMN_LIST_BILL

class ProxyBillSortFilter(qtc.QSortFilterProxyModel):
    """Class for the filtering of unwanted columns for the bill page."""

    def __init__(self):
        super().__init__()
        self.numbers = []

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

    def filterAcceptsRow(self, source_row, source_parent):
        root = self.sourceModel().sourceModel().rootItem
        item = root.getDescendants()[source_row]
        level = getattr(item, 'level', 0)

        if level != 5:
            return False

        elif item.number in self.numbers:
            return False

        else:
            self.numbers.append(item.number)
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
                left = source_left.internalPointer().getSize()
                right = source_right.internalPointer().getSize()

                return left < right
        return False