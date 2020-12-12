from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import csv

class ComboboxModel(qtc.QStringListModel):
    """
    This class is a simple subclass of the combobox model, only write and read
    capabilities are added to save presets to a file.
    """

    def __init__(self, filename):
        """
        Reads a passed file for the item to insert in the combobox.

        Custom functions:
            self.readFile()

        Args:
            filename (str): the file to read.
        """

        self.filename = filename
        data = self.readFile()
        super(ComboboxModel, self).__init__(data)

    def saveModel(self):
        """Saves the items of this combobox in a .csv file."""

        with open(self.filename, 'w') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(self.stringList())

    def readFile(self):
        """
        Opens a .csv file with stored values.

        Returns:
            list[str]: the list of items for the combobox
        """

        with open(self.filename, 'r') as file:
            csv_reader = csv.reader(file)
            return next(csv_reader)