from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import csv
from util import increment_number
from ComponentTree import ComponentTree
from constants import HEADERS
from constants import NOT_EDITABLE_TYPES
from constants import NOT_EDITABLE_COLUMNS

class ModelHardware(qtc.QAbstractItemModel):
    """
    This class create a model from the hardware archive file. It also manages the 
    data inside the model and let the user edit the archive file from the hardware editor.
    """

    def __init__(self):
        """Reads the archive file.""" 

        super(ModelHardware, self).__init__()                                         

        self.hardwareList = []                                                             
        self.filename = 'code/resources/archive/HardwareArchive.csv' 
        self.readArchive()                                                                   

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

        if not index.isValid():                                                            
            return None                                                         
        
        row = index.row()                                                               
        column = HEADERS[index.column()]                                                 

        if role == qtc.Qt.DisplayRole or role == qtc.Qt.EditRole:                         
            data = self.hardwareList[row][column]                                      
            return data                                                              

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

        if index.isValid():                                                            
            if role == qtc.Qt.EditRole:                                      
                row = index.row()                                                   
                column = HEADERS[index.column()]                                       

                self.hardwareList[row][column] = value                                   

                self.dataChanged.emit(index, index)                                        
                return True                                                         

        return False                                                             

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

        condition = (index.column() in NOT_EDITABLE_COLUMNS) or (index.column() == 5 and self.data(index.siblingAtColumn(4), qtc.Qt.DisplayRole) in NOT_EDITABLE_TYPES)

        if not index.isValid():                                                                                                         
            return qtc.Qt.NoItemFlags                                              
        if condition:                                                                    
            return qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable                           
        else:                                                                      
            return qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEditable      

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

        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:              
            return HEADERS[section].title()                                              
        return None                                                                        

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

        if not self.hasIndex(row, column, parent):                                       
            return qtc.QModelIndex()                                             

        item = self.hardwareList[row]                                                        

        if item:                                                              
            return self.createIndex(row, column, item)                               

        return qtc.QModelIndex()                                                         

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

        return qtc.QModelIndex()                                                           

    def rowCount(self, parent):
        """
        Returns the number of rows under the given parent . When the parent is valid it means that is returning 
        the number of children of parent.

        PARAMETERS:
            parent – QModelIndex

        RETURN TYPE:
            int
        """

        return len(self.hardwareList)                                                       

    def columnCount(self, parent):
        """
        Returns the number of columns for the children of the given parent .
        In most subclasses, the number of columns is independent of the parent .

        PARAMETERS:
            parent – QModelIndex

        RETURN TYPE:
            int
        """

        return len(HEADERS)                                                    

    def insertRows(self, item, parent = qtc.QModelIndex()):
        """
        Insert a row in the specified position.

        PARAMETERS:
            item - dict
            parent – QModelIndex

        RETURN TYPE:
            bool
        """

        position = len(self.hardwareList)                                                  

        self.beginInsertRows(parent, position, position)                                  

        self.hardwareList.append(item)                                                      

        self.endInsertRows()                                                                   

        self.saveArchive()                                                     

        return True                                                                  

    def removeRows(self, indexList, parent = qtc.QModelIndex()):
        """
        Remove a row in the specified position.

        PARAMETERS:
            item - dict
            parent – QModelIndex

        RETURN TYPE:
            bool
        """

        rows = len(indexList)                                                              

        for item in range(rows):                                                    
            if indexList[item].internalPointer() in self.hardwareList:
                position = self.hardwareList.index(indexList[item].internalPointer())        
                self.beginRemoveRows(parent, position, position)                       

                current = indexList[item]                                                       
                current = current.internalPointer()                                       
                self.hardwareList.remove(current)                                       

                self.endRemoveRows()                                                   
            
        self.saveArchive()                                                           

        return True                                                    

# CUSTOM FUNCTIONS

    def readArchive(self):
        """
        Reads the archive file under the class parameter filename. To change the file location you have
        to manually change the filename.
        """

        with open(self.filename, 'r') as archive:                              
            csv_reader = csv.DictReader(archive)                                         

            for line in csv_reader:                                                       
                self.insertRows(line)                                                    

    def saveArchive(self):
        """
        Saves the archive file under the class parameter filename. To change the file location you
        have to manually change the filename.
        """

        with open(self.filename, 'w') as archive:                                   
            csv_writer = csv.DictWriter(archive, fieldnames = HEADERS)                     

            csv_writer.writeheader()                                                     

            for line in self.hardwareList:                                                
                csv_writer.writerow(line)                                        

    def calculateNumber(self, number):
        """
        Calculates the number that an item should have, given a certain number prefix. 
        It returns the first free number for the given prefix type.

        INPUT:
            str - number: the number to increment

        RETURN TYPE:
            str: the calculated number
        """

        ct = 1                                                                          
        hardwareList = self.hardwareList                                                       
        hardwareNumbers = []                                                     

        for item in hardwareList:                                                          
            hardwareNumbers.append(item['number'])                                      

        newNumber = increment_number(number, ct, 5)                                     
        while newNumber in hardwareNumbers:                                              
            ct += 1                                                                     
            newNumber = increment_number(number, ct, 5)                              

        return newNumber                                                                     

    def changeFilename(self, filename):
        """
        Change the model filename.

        INPUT:
            str - filename: the new filename of the model
        """

        self.filename = filename                                                        