from ete3 import Tree
import csv
import math
from util import increment_number, calc_hash
from constants import HEADERS as headers
from constants import BILL_HEADERS

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
            first.add_feature('level', 1)

            for item in csv_reader:
                parentList = first.search_nodes(hashn = item['parent'])
                if len(parentList) > 0:
                    self.addInto(parentList[0], item)
                else:
                    missingList.append(item)

            while len(missingList) > 0:
                for item in missingList:
                    parentList = first.search_nodes(hashn = item['parent'])
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

        childItem = ComponentTree(childDict['number'], childDict)
        childItem.add_feature('level', parent.level + 1)
        parent.add_child(childItem)

    def init_node_attrs(self, attrs_dict):
        """
        Initializes all the given attributes to the node.
        
        INPUT:
            dict - attrs_dict: dictionary with the attributes names and values
        """

        for key in attrs_dict.keys():
            self.add_feature(key, attrs_dict[key])

    def update_hash(self):
        """Updates the hash numbers of this component and of all of his children recursively."""

        self.add_feature('parent', self.up.hashn)
        self.add_feature('hashn', calc_hash(self.up.hashn, self.number))

        for child in self.children:
            child.update_hash()

    def copy(self):
        """
        Returns a copy of this component. Copies all of his features and childrens.

        RETURN TYPE:
            ComponentTree: copy of the component
        """

        newNode = ComponentTree(self.number)

        for feature in self.features:
            newNode.add_feature(feature, getattr(self, feature, None))

        for child in self.children:
            newChild = child.copy()
            newNode.add_child(newChild)

        return newNode

    def calc_quantity(self, node):
        """
        Calculates and returns the quantity of a given node inside this subtree.

        INPUT:
            ComponentTree - node: component to search

        RETURN TYPE:
            int: calculated quantity of the given component
        """

        sameNodeList = self.get_valid_leaves_list(number = node.number)

        quantity = 0
        for element in sameNodeList:
            elementQuantity = int(getattr(element, 'quantity', 1))
            
            for p in element.iter_ancestors():
                elementQuantity *= int(getattr(p, 'quantity', 1))

            quantity += elementQuantity

        return quantity

    def calc_price(self, node):
        """
        Calculates and returns the total price of the component based on the total quantity needed.

        INPUT:
            ComponentTree - node: the component to calculate the price of

        RETURN TYPE:
            float: the calculated total price
        """

        quantity = self.calc_quantity(node)
        singlePrice = int(node.price)
        singleQuantity = int(node.quantityPackage)

        totalPrice = math.ceil(quantity / singleQuantity) * singlePrice

        return totalPrice

    def get_valid_leaves_list(self, **kwargs):
        """
        Returns a list of components of level 5 and with no deprecated ancestors.

        INPUT:
            **kwargs: other searching criteria

        RETURN TYPE:
            list: the list with the found elements
        """

        leavesList = self.search_nodes(level = 5, **kwargs)

        for element in leavesList:
            if element.status == 'Deprecated':
                leavesList.remove(element)
            else:
                for p in element.iter_ancestors():
                    status = getattr(p, 'status', '')
                    if status == 'Deprecated':
                        sameNodeList.remove(element)
                        break

        return leavesList

    def get_unique_leaves_list(self):
        """
        Returns a list of components of level 5 and with no deprecated ancestors and also with
        no duplicates, based on the numbers.

        RETURN TYPE:
            list: the list with the matching elements
        """

        validLeaves = self.get_valid_leaves_list()
        uniqueLeaves = []
        uniqueNumbers = []

        for element in validLeaves:
            if element.number not in uniqueNumbers:
                uniqueLeaves.append(element)
                uniqueNumbers.append(element.number)

        return uniqueLeaves

    def export_bill(self, filename):
        """
        Saves a .csv file with the classic bill of material data inside.

        INPUT:
            str - filename: the name of the file to save
        """

        componentsList = self.get_unique_leaves_list()
        billList = []
        billElement = {}

        for element in componentsList:
            for header in BILL_HEADERS:
                billElement[header] = getattr(element, header)
            
            billElement['quantity'] = self.calc_quantity(element)
            billElement['totalPrice'] = self.calc_price(element)

            billList.append(billElement)

        with open(filename, 'w') as file:
            fieldnames = BILL_HEADERS + ['totalPrice']
            csv_writer = csv.DictWriter(file, fieldnames = fieldnames)

            csv_writer.writeheader()

            for item in billList:
                csv_writer.writerow(item)

