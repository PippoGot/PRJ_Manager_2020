from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from ProxyBill import ProxyBill
from ProxyBillSortFilter import ProxyBillSortFilter

class BillPage(qtw.QWidget):
    """Class for the bill page."""

    def __init__(self, model):
        """Loads the .ui file."""

        super(BillPage, self).__init__()                                       

        uic.loadUi('code/resources/UIs/ui_bill_page.ui', self)   

        self.setModel(model)

    def setModel(self, model):     
        """Sets the model for the bill page.   

        INPUT:
            QAbstractItemModel - model: the model of the page
        """
        
        self.sourceModel = model

        self.model = ProxyBill()
        self.model.setSourceModel(self.sourceModel)

        self.proxyModel = ProxyBillSortFilter()
        self.proxyModel.setSourceModel(self.model)

        self.uiBillView.setModel(self.proxyModel)

        self.refreshView()

    def refreshView(self):
        """Refreshes the bill view."""

        for column in range(self.proxyModel.columnCount(qtc.QModelIndex())):    
            if column != self.proxyModel.columnCount(qtc.QModelIndex()):
                self.uiBillView.resizeColumnToContents(column)
        
        self.uiBillView.horizontalHeader().setStretchLastSection(True)
        self.proxyModel.sort(0, qtc.Qt.AscendingOrder)    
