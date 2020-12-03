from random import randint

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

        while self.root.searchNode(selfHash = newHash):
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

        while self.searchNode(number = number):
            ct += 1
            number = incrementID(prefix, suffix, level, ct)

        return number

    def getNewNode(self, parentNode, tp):
        types = {
            'Assembly': comp_nodes.AssemblyNode,
            'Leaf': comp_nodes.LeafNode,
            'Jig': comp_nodes.JigNode,
            'Placeholder': comp_nodes.PlaceholderNode
        }

        newNumber = self.getNewNumber(parentNode.getPrefix(), parentNode.getLevel() + 1)

        return types[tp](parentNode.getLevel() + 1, numberID = newNumber)

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
