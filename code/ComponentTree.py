from ete3 import Tree
import csv
from util import increment_number, special, headers

class ComponentTree(Tree):
    def __init__(self, name, attrs = {}):
        super().__init__(name = name)

        if attrs:
            self.init_node_attrs(attrs)

    def calc_number(self, parent, level = None):
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
            Tree - parent: the parent of the item to add
            dict - childDict: dictionary with the new item parameters
        """

        childItem = ComponentTree('new')
        setattr(childItem, 'level', parent.level + 1)
        childItem.init_node_attrs(childDict)
        number = getattr(childItem, 'number')
        prefix = number[1:4]
        if prefix in special:
            setattr(childItem, 'level', 5)
        else:
            setattr(childItem, 'number', childItem.calc_number(parent))
            
        number = getattr(childItem, 'number')
        setattr(childItem, 'name', number)
        parent.add_child(childItem)

    def init_node_attrs(self, attrs_dict):
        for key in attrs_dict.keys():
            setattr(self, key, attrs_dict[key])