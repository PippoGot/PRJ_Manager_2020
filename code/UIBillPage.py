from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from ProxyBill import ProxyBill
from ModelBill import ModelBill

class BillPage(qtw.QWidget):
    """Class for the bill page."""

    def __init__(self):
        """Loads the .ui file."""

        super(BillPage, self).__init__()

        uic.loadUi('code/resources/UIs/ui_bill_page.ui', self)

        self.model = ModelBill()
        self.proxyModel = ProxyBill()
        self.proxyModel.setSourceModel(self.model)

        self.uiBillView.setModel(self.proxyModel)
        self.refreshView()

    def refreshModel(self, nodesList):
        if nodesList:
            for node in nodesList:
                self.model.insertRows(node)

        self.refreshView()

    def refreshView(self):
        """Refreshes the bill view."""

        for column in range(self.proxyModel.columnCount(qtc.QModelIndex())):
            if column != self.proxyModel.columnCount(qtc.QModelIndex()):
                self.uiBillView.resizeColumnToContents(column)

        self.uiBillView.horizontalHeader().setStretchLastSection(True)
        self.proxyModel.sort(0, qtc.Qt.AscendingOrder)
