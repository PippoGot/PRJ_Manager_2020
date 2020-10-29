from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class ProxyBill(qtc.QSortFilterProxyModel):
    """Class for the filtering of unwanted columns for the bill page."""

    def __init__(self):
        super().__init__()

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