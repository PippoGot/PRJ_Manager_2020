from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from ProxyBill import ProxyBill as Bill
from ProxyBillSortFilter import ProxyBillSortFilter as ProxyBill

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

        self.model = Bill()
        self.model.setSourceModel(self.sourceModel)
        
        self.proxyModel = ProxyBill()
        self.proxyModel.setSourceModel(self.model)

        self.uiBillView.setModel(self.proxyModel)
