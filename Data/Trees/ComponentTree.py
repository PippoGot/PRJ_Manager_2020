from random import randint
import csv

from ..Nodes.ADTutil import incrementID
from ..Nodes import CompositeNodes as comp_nodes

from .AbstractTree import AbstractTree

class ComponentTree(AbstractTree):
    def __init__(self, root):
        super().__init__()
        self.root = root

# INDEXING

    def updateHashes(self, node):
        """
        Updates the hashes numbers of the descendants of node checking that the number
        doesn't repeat. Also updates the childrens parentHashes.

        Args:
            node (ComponentNode): where to start the update
        """

        newHash = randint(0, 99999)

        while self.searchByHash(newHash):
            newHash = randint(0, 99999)

        node.selfHash = newHash

        for child in node.children:
            child.parentHash = node.selfHash
            self.updateHashes(child)

# SEARCH

    def searchNode(self, **parameters):
        """
        Search for a node with the specified features. If more than one is present in
        the tree, only the first occurrence is returnded.

        Returns:
            ComponentNode: the first occurrence that respects the given attributes
        """

        for node in self.iterPreorder():
            check = True

            for featureKey, featureValue in parameters.items():
                checkingValue = node.getFeature(featureKey)
                if not checkingValue == featureValue:
                    check = False
                    break

            if check: return node
        return None

    def searchByHash(self, nextHash):
        """
        Search for a node with the specified hash.

        Returns:
            ComponentNode: the node with the given hash
        """

        for node in self.iterPreorder():
            currentHash = getattr(node, 'selfHash')
            if currentHash == nextHash: return node
        return None

    def searchNodes(self, **parameters):
        """
        Returns a list of nodes with the specified features value. If nothing is specified,
        all of the nodes in the subtree will be returned.

        Returns:
            list[ComponentNode]: the list of the corresponding nodes found
        """

        searchList = []

        for node in self.iterPreorder():
            check = True

            for featureKey, featureValue in parameters.items():
                checkingValue = node.getFeature(featureKey)
                if not checkingValue == featureValue:
                    check = False
                    break

            if check:
                searchList.append(node)

        return searchList

# PROPERTIES

    def getNodeCost(self, node):
        pass

    def getNodeQuantity(self, node):
        pass

    def getNewNumber(self, prefix, level):
        """
        Calculates and returns the next available number for the specified prefix and level.

        Args:
            prefix (str): the prefix of the parent of the new item
            level (int): the level of the new item
            root (ComponentNode): root of the tree to search to speed up the process

        Returns:
            str: the next available number
        """

        suffix = '000'
        ct = 1
        number = incrementID(prefix, suffix, level, ct)

        while self.searchNode(numberID = number):
            ct += 1
            number = incrementID(prefix, suffix, level, ct)

        return number

    def getNewNode(self, parentNode, tp):
        """
        Returns a new node given the parent and the type. The node isn't inserted in the
        tree, it is a temporary node instead, that has the values of the one that should
        be inserted as next with the given properties.

        Args:
            parentNode (ComponentNode): the node that will be the parent of the returned node
            tp (str): the node type of the new node

        Returns:
            ComponentNode: the next node
        """

        types = {
            'Assembly': comp_nodes.AssemblyNode,
            'Leaf': comp_nodes.LeafNode,
            'Jig': comp_nodes.JigNode,
            'Placeholder': comp_nodes.PlaceholderNode
        }

        if tp == 'Leaf':
            newNumber = self.getNewNumber(parentNode.getPrefix(), 5)
            return types[tp](numberID = newNumber)
        elif tp == 'Jig':
            newNumber = self.getNewNumber('JIG', parentNode.getLevel() + 1)
            return types[tp](parentNode.getLevel() + 1, numberID = newNumber)
        elif tp == 'Placeholder':
            newNumber = self.getNewNumber('PLC', parentNode.getLevel() + 1)
            return types[tp](parentNode.getLevel() + 1, numberID = newNumber)
        else:
            newNumber = self.getNewNumber(parentNode.getPrefix(), parentNode.getLevel() + 1)
            return types[tp](parentNode.getLevel() + 1, numberID = newNumber)

# FILE MANAGEMENT

    def readFile(self, filename):
        """
        Reads a file to get the component tree stored inside it.

        Args:
            filename (str): the name of the file to read

        Returns:
            ComponentTree: the file in component tree structure
        """

        if filename:
            with open(filename, 'r') as file:
                csv_reader = csv.DictReader(file)
                firstNode = comp_nodes.ProjectNode
                firstNode = self.fillNode(firstNode, next(csv_reader))
                self.root.addChild(firstNode)

                for line in csv_reader:
                    prefix = line['numberID'][1:4]
                    parent = self.searchByHash(int(line['parentHash']))
                    newNode = self.getNodeByType(line['type'], prefix)

                    newNode = self.fillNode(newNode, line, parent)
                    parent.addChild(newNode)

                return self

    def getNodeByType(self, tp, prefix):
        """
        Returns the class of the correct node based on the type and the prefix
        of the node.

        Args:
            tp (str): the type of the node
            prefix (str): the prefix of the node

        Returns:
            class: the right class to initialize
        """

        nodes = {
            'Project': comp_nodes.ProjectNode,
            'Assembly': comp_nodes.AssemblyNode,
            'Part': comp_nodes.LeafNode,
            'Jig': comp_nodes.JigNode,
            'Placeholder': comp_nodes.PlaceholderNode,
            'Product': comp_nodes.ProductNode,
            'Hardware': self.chooseHardware(prefix)
        }

        return nodes[tp]

    def chooseHardware(self, prefix):
        """
        Returns the correct type of hardware node based on the pefix given.

        Args:
            prefix (str): the prefix of the node

        Returns:
            class: the class of the node to initialise
        """

        nodes = {
            'MEH': comp_nodes.HardwareNode,
            'ELH': comp_nodes.HardwareNode,
            'EMH': comp_nodes.HardwareNode,
            'MMH': comp_nodes.MeasuredNode
        }
        if prefix in nodes.keys():
            return nodes[prefix]

    def fillNode(self, nodeType, dataDict, parent = None):
        """
        Fills up a node with all the data needed.

        Args:
            nodeType (class): the class of the node
            dataDict (dict[str, str]): the dictionary with all the data
            parent (ComponentNode): the parent of the current node. Defaults to None.

        Returns:
            ComponentNode: the complete node with all the data
        """

        selfHash = int(dataDict['selfHash'])
        parentHash = int(dataDict['parentHash'])
        del dataDict['selfHash']
        del dataDict['parentHash']

        if dataDict['type'] in ['Assembly', 'Jig', 'Placeholder']:
            node = nodeType(parent.getLevel() + 1, **dataDict)
        else:
            node = nodeType(**dataDict)

        node.selfHash = selfHash
        node.parentHash = parentHash

        return node

# REPRESENTATION

    def toString(self, *featureKeys):
        """
        Returns a string version of the tree with optional features. The string is tabbed
        to represent the different tree levels.

        Returns:
            str: the tree structure in string format
        """

        string = ''

        for node in self.iterPreorder():
            string += node.getDepth() * '   ' + str(node)

            for featureKey in featureKeys:
                featureValue = node.getFeature(featureKey)
                string += f' - {featureValue}'

            string += '\n'
        return string

# DUNDERS

    def __repr__(self):
        self.toString()
