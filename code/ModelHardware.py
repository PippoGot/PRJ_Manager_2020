from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import csv
from util import increment_number, headers

class ModelHardware(qtc.QAbstractItemModel):
    """
    This class create a model from the hardware archive file. It also manages the 
    data inside the model and let the user edit the archive file from the hardware editor.
    """

    def __init__(self):
        """Reads the archive file.""" 

        super(ModelHardware, self).__init__()                                                   # superclass constructor

        self.hardwareList = []                                                                  # model data structure
        self.filename = 'D:/Data/_PROGETTI/APPS/PRJ_Manager/archive/HardwareArchive.csv'        # this is the file location
        self.readArchive()                                                                      # reads the archive file

# MODEL FUNCTIONS

    def data(self, index, role):
        """
        Returns the data stored under the given role for the item referred to by the index .
        
        PARAMETERS:
            index – QModelIndex
            role – int

        RETURN TYPE:
            object
        """

        if not index.isValid():                                                                 # if the index isn't valid
            return None                                                                         # returns None
        
        row = index.row()                                                                       # otherwise gets the index row
        column = headers[index.column()]                                                        # converts the column to a keyword argument

        if role == qtc.Qt.DisplayRole or role == qtc.Qt.EditRole:                               # and then if the role is display or edit
            data = self.hardwareList[row][column]                                               # extract the corresponding data
            return data                                                                         # and returns it

    def setData(self, index, value, role = qtc.Qt.EditRole):
        """
        Sets the role data for the item at index to value .
        Returns true if successful; otherwise returns false .
        The dataChanged() signal should be emitted if the data was successfully set.
        The base class implementation returns false . This function and data() must be reimplemented
        for editable models.

        PARAMETERS:
            index – QModelIndex
            value – object
            role – int

        RETURN TYPE:
            bool
        """

        if index.isValid():                                                                     # if the index isn't valid
            if role == qtc.Qt.EditRole:                                                         # and role is Edit
                row = index.row()                                                               # gets the index row
                column = headers[index.column()]                                                # and converts the index column

                self.hardwareList[row][column] = value                                          # changes the data in the given location

                self.dataChanged.emit(index, index)                                             # sends the signal that the data in the given location has changed
                return True                                                                     # and returns True

        return False                                                                            # otherwise returns False

    def flags(self, index):
        """
        Returns the item flags for the given index .
        The base class implementation returns a combination of flags that enables the item (ItemIsEnabled)
        and allows it to be selected (ItemIsSelectable ).

        PARAMETERS:
            index – QModelIndex

        RETURN TYPE:
            ItemFlags
        """

        if not index.isValid():                                                                 # if the index isn't valid                                                       
            return qtc.Qt.NoItemFlags                                                           # returns NoItemFlags
        if index.column() == 1 or index.column() == 0:                                          # if the index column is either 0 or 1
            return qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable                               # the item is enabled and selectable
        else:                                                                                   # otherwise
            return qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEditable       # the item is also editable

    def headerData(self, section, orientation, role):
        """
        Turns the data for the given role and section in the header with the specified orientation .
        For horizontal headers, the section number corresponds to the column number. Similarly, for 
        vertical headers, the section number corresponds to the row number.

        PARAMETERS:
            section – int
            orientation – Orientation
            role – int

        RETURN TYPE:
            object
        """

        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:                     # if the orientation is horizontal and role is display
            return headers[section]                                                             # returns the corresponding header
        return None                                                                             # otherwise returns None

    def index(self, row, column, parent):
        """
        Returns the index of the item in the model specified by the given row , column and parent index.
        When reimplementing this function in a subclass, call createIndex() to generate model indexes 
        that other components can use to refer to items in your model.

        PARAMETERS:
            row – int
            column – int
            parent – QModelIndex

        RETURNS TYPE:
            QModelIndex
        """

        if not self.hasIndex(row, column, parent):                                              # if the model doesn't have this index
            return qtc.QModelIndex()                                                            # returns an invalid index

        item = self.hardwareList[row]                                                           # otherwise get the item in the structure at the selected row

        if item:                                                                                # if such item exist
            return self.createIndex(row, column, item)                                          # returns it's index which is just generated

        return qtc.QModelIndex()                                                                # otherwise returns and invalid index

    def parent(self, index):
        """
        Returns the parent of the model item with the given index . If the item has no parent, an invalid 
        QModelIndex is returned.
        A common convention used in models that expose tree data structures is that only items in the first
        column have children. For that case, when reimplementing this function in a subclass the column of 
        the returned QModelIndex would be 0.
        When reimplementing this function in a subclass, be careful to avoid calling QModelIndex member 
        functions, such as parent(), since indexes belonging to your model will simply call your implementation,
        leading to infinite recursion
        
        PARAMETERS:
            index – QModelIndex

        RETURN TYPE:
            QModelIndex
        """

        return qtc.QModelIndex()                                                                # returns an invalide index in any case

    def rowCount(self, parent):
        """
        Returns the number of rows under the given parent . When the parent is valid it means that is returning 
        the number of children of parent.

        PARAMETERS:
            parent – QModelIndex

        RETURN TYPE:
            int
        """

        return len(self.hardwareList)                                                           # returns the length of the list

    def columnCount(self, parent):
        """
        Returns the number of columns for the children of the given parent .
        In most subclasses, the number of columns is independent of the parent .

        PARAMETERS:
            parent – QModelIndex

        RETURN TYPE:
            int
        """

        return len(headers)                                                                     # returns the number of item in the first row

    def insertRows(self, item, parent = qtc.QModelIndex()):
        """
        Insert a row in the specified position.

        PARAMETERS:
            item - dict
            parent – QModelIndex

        RETURN TYPE:
            bool
        """

        position = len(self.hardwareList)                                                       # gets the position of where to insert the new data

        self.beginInsertRows(parent, position, position)                                        # signals that it's starting to insert data

        self.hardwareList.append(item)                                                          # adds the item to the data structure

        self.endInsertRows()                                                                    # signals that it has finished inserting data

        self.saveArchive()                                                                      # saves the data in the archive file

        return True                                                                             # returns True, the operation has been successful

    def removeRows(self, indexList, parent = qtc.QModelIndex()):
        """
        Remove a row in the specified position.

        PARAMETERS:
            item - dict
            parent – QModelIndex

        RETURN TYPE:
            bool
        """

        rows = len(indexList)                                                                   # gets the number of items to remove

        for item in range(rows):                                                                # for each item
            if indexList[item].internalPointer() in self.hardwareList:
                position = self.hardwareList.index(indexList[item].internalPointer())           # gets the position of the item
                self.beginRemoveRows(parent, position, position)                                # signals that it's starting to remove data

                current = indexList[item]                                                       # the current item is extracted from the list
                current = current.internalPointer()                                             # and from the index
                self.hardwareList.remove(current)                                               # then the item is removed from the data structure

                self.endRemoveRows()                                                            # signals that it has finished removing data
            
        self.saveArchive()                                                                      # saves the data in the archive file

        return True                                                                             # returns True, the operation has been successful

# CUSTOM FUNCTIONS

    def readArchive(self):
        """
        Reads the archive file under the class parameter filename. To change the file location you have
        to manually change the filename.
        """

        with open(self.filename, 'r') as archive:                                               # opens the file
            csv_reader = csv.DictReader(archive)                                                # creates a csv reader

            for line in csv_reader:                                                             # then for every line in the file
                self.insertRows(line)                                                           # it inserts a row in the file with the data contained in that line

    def saveArchive(self):
        """
        Saves the archive file under the class parameter filename. To change the file location you
        have to manually change the filename.
        """

        with open(self.filename, 'w') as archive:                                               # opens the file
            csv_writer = csv.DictWriter(archive, fieldnames = headers)                          # creates a csv writer with the previously stored headers

            csv_writer.writeheader()                                                            # writes the headers at the top of the file

            for line in self.hardwareList:                                                      # then for every item in the list
                csv_writer.writerow(line)                                                       # it writes a row in the file

    def calculateNumber(self, number):
        """
        Calculates the number that an item should have, given a certain number prefix. 
        It returns the first free number for the given prefix type.

        INPUT:
            str - number: the number to increment

        RETURN TYPE:
            str: the calculated number
        """

        ct = 1                                                                                  # initialize a counter to 0
        hardwareList = self.hardwareList                                                        # gets the list where the data will be stored
        hardwareNumbers = []                                                                    # and an empty list

        for item in hardwareList:                                                               # for every item in the data list
            hardwareNumbers.append(item['number'])                                              # adds it's number to the empty list

        newNumber = increment_number(number, ct, 5)                                             # then generates the first number
        while newNumber in hardwareNumbers:                                                     # and while the number is in the list
            ct += 1                                                                             # increments the counter
            newNumber = increment_number(number, ct, 5)                                         # and regenerates the number

        return newNumber                                                                        # when a non existing number is found it returns it

    def changeFilename(self, filename):
        """
        Change the model filename.

        INPUT:
            str - filename: the new filename of the model
        """

        self.filename = filename                                                                # updates the filename parameter