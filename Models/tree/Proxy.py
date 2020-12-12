from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

class TreeProxy(qtc.QSortFilterProxyModel):
    """This class provides sorting and filtering for the unwanted items."""

    HEADERS = [
        0, # numberID
        1, # name
        2, # description
        3, # type
        4, # manufacture
        5, # status
        6, # comment
        8, # quantity
        10 # seller
    ]

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

        if source_column not in self.HEADERS:
            return False
        else:
            return True

    def filterAcceptsRow(self, source_row, source_parent):
        """
        Selects the rows to show from the original model.
        If the row is a deprecated item and the option is on, the row is not displayed.

        Custom functions:
            BaseNode.getChildAt()
            BaseNode.getFeature()

        Args:
            source_row (int): current row index.
            source_parent (QModelIndex): index of the current parent item.

        Returns:
            bool: whether to show or hide the row.
        """

        if source_parent.isValid():
            status = source_parent.internalPointer().getChildAt(source_row).getFeature('status')
            if status == self.filterRegExp().pattern():
                return False
        return True

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