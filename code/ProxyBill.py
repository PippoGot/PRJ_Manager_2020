from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class ProxyBill(qtc.QSortFilterProxyModel):
    """Class for the filtering and sorting of unwanted columns/rows for the bill page."""

    def __init__(self):
        super().__init__()

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
            bool: left < right.
        """

        if source_left.column() == 0 and source_right.column() == 0:
            if source_left.isValid() and source_right.isValid():
                left = source_left.internalPointer().getSize()
                right = source_right.internalPointer().getSize()

                return left < right
        return False