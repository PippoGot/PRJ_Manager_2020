from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from ProxyBill import ProxyBill
from ModelBill import ModelBill

class BillPage(qtw.QWidget):
    """Class for the bill page. Provides a UI for the Bill page."""

    def __init__(self):
        """
        Loads the UI window, creates and sets the models, then refreshes the view

        Custom functions:
            self.refreshView()
            self.setModel()
        """

        super(BillPage, self).__init__()

        uic.loadUi('code/resources/UIs/ui_bill_page.ui', self)

        self.setModel()
        self.refreshView()

    def refreshModel(self, nodesList):
        """
        Resets the model with the latest data.

        Custom functions:
            ModelBill.insertRows()

        Args:
            nodesList (list[BaseNode]): the list of nodes to update or add.
        """

        for node in nodesList:
            self.model.insertRows(node)

    def refreshView(self):
        """
        Refreshes the bill view, resizing the columns to their content and
        sorts the rows.
        """

        for column in range(self.proxyModel.columnCount(qtc.QModelIndex())):
            if column != self.proxyModel.columnCount(qtc.QModelIndex()):
                self.uiBillView.resizeColumnToContents(column)

        self.uiBillView.horizontalHeader().setStretchLastSection(True)
        self.proxyModel.sort(0, qtc.Qt.AscendingOrder)

    def exportBOM(self, filename):
        """
        Saves the bill of materials in a .csv file.

        Args:
            filename (str): the name or path of the file.
        """

        self.model.saveFile(filename)

    def setModel(self, nodesList = None):
        """
        Resets the model if no nodes are passed in, fills and updates the model if
        a list of nodes is passed.

        Args:
            nodesList (list[BaseNode]): the list of nodes to add. Defaults to None.
        """

        self.proxyModel = ProxyBill()

        if nodesList and len(nodesList) > 0 :
            self.refreshModel(nodesList)
        else:
            self.model = ModelBill()

        self.proxyModel.setSourceModel(self.model)
        self.uiBillView.setModel(self.proxyModel)
        self.refreshView()