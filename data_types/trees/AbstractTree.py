from ..nodes.AbstractNode import AbstractNode

class AbstractTree():
    """
    Class to represent a generic tree data structure.

    self.root
    """

    def __init__(self):
        self.root = AbstractNode()

# COPY

    def copy(self):
        """
        Copies and returns this tree.

        Returns:
            AbstractTree: the copied tree
        """

        newTree = self.__class__()
        copiedRoot = self.root.deepCopy()
        newTree.root = copiedRoot
        return newTree

# VISIT ITERATORS

    def iterPreorder(self):
        """
        Iters through the nodes of this tree recursively from root to leaf level.

        Returns:
            Iterator: the next descendant node to visit
        """

        return self.root.iterPreorder()

    def iterPostorder(self):
        """
        Iters through the nodes of this tree recursively from leaf to root level.

        Returns:
            Iterator: the next descendant node to visit
        """

        return self.root.iterPostorder()

# GETTERS

    def getRoot(self):
        """
        Returns this tree's root by the definition:

        root = the node that has no parent (None);

        Returns:
            AbstractNode: the root of this tree
        """

        return self.root

    def getHeight(self):
        """
        Returns this tree height, with it beign the height of the root's highest
        children +1.

        Returns:
            int: the height of this tree
        """

        return self.root.getHeight()

    def getLeaves(self):
        """
        Returns a list of leaf nodes in this tree. A leaf is a node with no children.

        Returns:
            list[AbstractNode]: the list of leaf nodes
        """

        return self.root.getLeaves()

    def getNodes(self):
        """
        Returns a list of the nodes of this tree.

        Returns:
            list[AbstractNode]: the list of descendant nodes
        """

        return self.root.getDescendants()

# REPRESENTATION

    def toString(self, *featureKeys):
        """
        Returns a string version of the tree with optional features. The string is tabbed
        to represent the different tree levels.

        Args:
            tab (int): the number of spaces of indentation. Default as 0.

        Returns:
            str: the tree structure in string format.
        """

        string =''
        for node in self.iterPreorder():
            string += node.getDepth() * '   ' + f'|-- {node.getIndex()}°\n'

        return string

# DUNDERS

    def __repr__(self):
        return self.toString()

    def __str__(self):
        return self.toString()
