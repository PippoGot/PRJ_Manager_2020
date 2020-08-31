from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from constants import HEADERS as headers

class ProxyBill(qtc.QIdentityProxyModel):
    def __init__(self):
        super().__init__()

    def mapFromSource(self, sourceIndex):

        if not sourceIndex.isValid(): return qtc.QModelIndex()

        element = sourceIndex.internalPointer()
        leafList = self.sourceModel().rootItem.get_unique_leaves_list()

        if element not in leafList: return qtc.QModelIndex()

        row = leafList.index(element)
        return self.sourceModel().createIndex(row, sourceIndex.column(), element)

    def mapToSource(self, proxyIndex):

        if not proxyIndex.isValid(): return qtc.QModelIndex()
        
        element = proxyIndex.internalPointer()

        if not element or not element.up: return qtc.QModelIndex()

        row = element.up.children.index(element)
        
        return self.sourceModel().createIndex(row, proxyIndex.column(), element)

    def rowCount(self, parent):
        if not parent.isValid():
            sourceModel = self.sourceModel()
            if sourceModel:
                leafList = sourceModel.rootItem.get_unique_leaves_list()
                return len(leafList)
        return 0

    def columnCount(self, parent):
        return len(headers)

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):                                          # if the given index doesn't exist
            return qtc.QModelIndex()                                                        # returns an invalid index
        else:                                                                               # if the index is not valid
            parentItem = self.sourceModel().rootItem                                        # the parent item is set to the root item

        leafList = parentItem.get_unique_leaves_list()
        if row >= len(leafList) or row < 0: return qtc.QModelIndex()

        childItem = leafList[row]                                                           # the child item is the child of the parent item at the given index row

        if childItem:                                                                       # if the child item exists
            return self.createIndex(row, column, childItem)                                 # creates and returns it's index

        return qtc.QModelIndex()

    def parent(self, index):
        return qtc.QModelIndex()                                                            # an invalid index is return

    def data(self, index, role):
        if not index.isValid():                                                             # if the index is not valid
            return None                                                                     # returns None

        element = index.internalPointer()
        quantity = self.sourceModel().rootItem.calc_quantity(element)

        if role == qtc.Qt.DisplayRole or role == qtc.Qt.EditRole:                           # then if the role is display or edit
            if index.column() == 9:
                return quantity
            return getattr(element, headers[index.column()], None)                             # returns the data stored under the given index

    def headerData(self, section, orientation, role):
        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:                 # if the orientation is horizontal and the role is display
            return headers[section].title()                                                 # returns the root data under the given index
        return None  

    def flags(self, index):
        if not index.isValid():                                                             # if the index is not valid                                                        
            return qtc.Qt.NoItemFlags                                                       # returns NoItem
        else:
            return qtc.Qt.ItemIsEnabled