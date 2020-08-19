from ete3 import Tree
import csv
from util import increment_number, special, headers

class ComponentTree(Tree):
    """Adds some specific functions for the managing of the components tree."""

    def __init__(self, name, attrs = {}):
        """
        Initializes a component node.

        INPUT:
            object - name: the name of the node
            optional dict - attrs: the attributes to set
        """

        super().__init__(name = name)

        if attrs:
            self.init_node_attrs(attrs)

    def calc_number(self, parent, level = None):
        """
        Calculates the number of the first free space available in the given node.

        INPUT:
            ComponentTree - parent: the node from which the number is calculated
            optional int - level: overwriting of the level

        RETURN TYPE:
            str: the calculated number
        """

        ct = 1
        numbers = []
        if not level:
            level = parent.level + 1

        for child in parent.children:
            numbers.append(child.number)

        parentNumber = parent.number

        number = increment_number(parentNumber, ct, level)
        while number in numbers:
            ct += 1
            number = increment_number(parentNumber, ct, level)
        
        return number

    def save_file(self, filename):
        """
        Saves a tree in a .csv file.

        INPUT:
            str - filename: the name of the file that will be saved
        """

        with open(filename, 'w') as file:
            fieldnames = headers
            csv_writer = csv.DictWriter(file, fieldnames = fieldnames)

            csv_writer.writeheader()

            for item in self.iter_descendants():
                line = {}
                for key in fieldnames:
                    line[key] = getattr(item, key, None)
                csv_writer.writerow(line)

    def read_file(self, filename):
        """
        Reads a .csv file and converts it in a tree data structure.

        INPUT:
            str - filename: the name of the file to read 
        """

        missingList = []                                                                    # empty list for the vacant items

        with open(filename, 'r') as file:                                                   # opens the file in read mode
            csv_reader = csv.DictReader(file)                                               # creates a csv reader

            firstItem = next(csv_reader)
            first = ComponentTree(firstItem['number'], firstItem)

            setattr(first, 'level', 1)
            
            for item in csv_reader:
                parentList = first.search_nodes(name = item['parent'])
                if len(parentList) > 0:
                    self.addInto(parentList[0], item)
                else:
                    missingList.append(item)

            while len(missingList) > 0:
                for item in missingList:
                    parentList = first.search_nodes(name = item['parent'])
                    if len(parentList) > 0:
                        self.addInto(parentList[0], item)
                        missingList.remove(item)
        return first

    def addInto(self, parent, childDict):
        """
        Adds a tree item to the given parent and then adds the given parameters to 
        the new tree item.

        INPUT:
            ComponentTree - parent: the parent of the item to add
            dict - childDict: dictionary with the new item parameters
        """

        childItem = ComponentTree('new', childDict)
        setattr(childItem, 'level', parent.level + 1)
        number = getattr(childItem, 'number')
        setattr(childItem, 'name', number)
        parent.add_child(childItem)

    def init_node_attrs(self, attrs_dict):
        """
        Initializes all the given attributes to the node.
        
        INPUT:
            dict - attrs_dict: dictionary with the attributes names and values
        """

        for key in attrs_dict.keys():
            setattr(self, key, attrs_dict[key])