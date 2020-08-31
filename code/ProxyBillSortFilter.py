from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from constants import COLUMN_LIST_BILL as listaColonne

class ProxyBillSortFilter(qtc.QSortFilterProxyModel):

    def __init__(self):
        super().__init__()

    def filterAcceptsColumn(self, source_column, source_parent):
        if source_column not in listaColonne.keys():                       # if the column has to be hidden
            return False                                                        # returns False
        else:                                                                   # otherwise
            return True                                                         # returns True

    def lessThan(self, source_left, source_right):      
        pass
