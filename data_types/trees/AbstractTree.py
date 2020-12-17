import json

from .TREEutil import extractNode, strToClass, classToStr
from ..nodes.AbstractNode import AbstractNode

class AbstractTree():
    """
    Class that describes the basic behaviour of a tree.
    Provides copying, nodes traversal, representation, basic getters
    and json file reading and saving.
    """

# INIT

    def __init__(self, root = None):
        if root:
            self.root = root
        else:
            self.root = AbstractNode()

# COPY

    def copy(self):
        """
        Copies and returns this tree.

        Returns:
            AbstractTree: the copied tree
        """

        copiedTree = self.__class__()
        copiedRoot = self.root.deepCopy()
        copiedTree.root = copiedRoot
        return copiedTree

# TRAVERSAL

    def iterPreorder(self):
        """
        Iters through the nodes of this tree from root to leaf level.

        Returns:
            Iterator: the next descendant node to visit
        """

        if not self.root: return

        return self._iterPreorder(self.root)

    def _iterPreorder(self, root):
        """
        Private recursive function.
        Iters through the nodes of this tree from root to leaf level.

        Yields:
            AbstractNode: the next node to visit
        """

        yield root
        for child in root.getChildren():
            yield  from self._iterPreorder(child)

    def iterPostorder(self):
        """
        Iters through the nodes of this tree from leaf to root level.

        Returns:
            Iterator: the next descendant node to visit
        """

        if not self.root: return

        return self._iterPostorder(self.root)

    def _iterPostorder(self, root):
        """
        Private recursive function.
        Iters through the nodes of this tree from leaf to root level.

        Yields:
            AbstractNode: the next descendant node to visit
        """

        for child in root.getChildren():
            yield  from self._iterPostorder(child)
        yield root

# GETTERS

    def getRoot(self):
        """
        Returns this tree's root. The root is the highest node with no parent.

        Returns:
            AbstractNode: the root of this tree
        """

        return self.root

    def getNodes(self):
        """
        Returns a list of the nodes of this tree.

        Returns:
            list[AbstractNode]: the list of the tree nodes
        """

        if not self.root: return

        descendants = []
        for node in self.iterPreorder():
            descendants.append(node)

        return descendants

    def getLeaves(self):
        """
        Returns a list of leaf nodes in this tree. A leaf is a node with no children.

        Returns:
            list[AbstractNode]: the list of leaf nodes
        """

        if not self.root: return

        leaves = []
        for node in self.iterPreorder():
            if not node.getChildren():
                leaves.append(node)

        return leaves

    def getHeight(self):
        """
        Returns this tree height, with it being the height of the root's highest
        children +1.

        Returns:
            int: the height of this tree
        """

        if not self.root: return

        return self.root.getHeight()

# REPRESENTATION

    def toString(self, tab = 0):
        """
        Returns a string version of the tree with all the nodes features. The string is tabbed
        to represent the different tree levels.

        Args:
            tab (int): the number of spaces of indentation. Default as 0.

        Returns:
            str: the tree structure in string format.
        """

        string = json.dumps(self.toDict(), indent=4)
        return string

    def toDict(self):
        """
        Returns a nested dictionaries structure compatible with json objects.

        Returns:
            dict[str, PyObject]: the dictionary sructure
        """

        if not self.root: return

        return self._toDict(self.root)

    def _toDict(self, node):
        """
        Private recursive function.
        Returns a nested dictionaries structure compatible with json objects.

        Returns:
            dict[str, PyObject]: the dictionary sructure
        """

        data = {}
        data['class'] = classToStr(node)
        if classToStr(node) == 'AssemblyNode': data['level'] = node.level
        data.update(node.items())

        data['children'] = []
        for child in node.getChildren():
            data['children'].append(self._toDict(child))

        return data

# FILE MANAGEMENT

    @staticmethod
    def jsonRead(filename):
        """
        Converts a .json file to an AbstractNode data structure.

        Args:
            filename (str): the name or path of the file

        Returns:
            AnstractNode: the root of the resulting tree
        """

        with open(filename, 'r') as file:
            data = json.load(file)

        root = extractNode(data)
        return root

    @staticmethod
    def jsonParse(string):
        """
        Converts a json type string to an AbstractNode data structure.

        Args:
            filename (str): the name or path of the file

        Returns:
            AbstractNode: the root of the resulting tree
        """

        data = json.loads(string)
        root = extractNode(data)
        return root

    def jsonSave(self, filename):
        """
        Converts an AbstractTree to a .json file.

        Args:
            filename (str): the name or path of the file
        """

        with open(filename, 'w') as file:
            data = self.toDict()
            json.dump(data, file, indent = 4)

# DUNDERS

    def __repr__(self):
        return self.toString()

    def __str__(self):
        return self.toString()
