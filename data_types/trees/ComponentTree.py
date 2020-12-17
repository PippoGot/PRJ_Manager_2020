from ..nodes.NODESutil import incrementID
from .TREEutil import strToClass

from .AbstractTree import AbstractTree
from ..nodes.CompositeNodes import ProjectNode

class ComponentTree(AbstractTree):
    """
    Class that describes the behaviour of a component tree.
    Extends AbstractTree class and provides nodes research, and specific getters.
    """

    def __init__(self, root = None):
        super().__init__(root)
        if not root: self.root = ProjectNode()

# RESEARCH

    def searchNode(self, **parameters):
        """
        Search for a node with the specified parameters. If more than one is present in
        the tree, only the first occurrence is returnded.

        Returns:
            ComponentNode: the first occurrence that respects the given parameters
        """

        for node in self.iterPreorder():
            check = True

            for key, value in parameters.items():
                checkingValue = node.getFeature(key)
                if not checkingValue == value:
                    check = False
                    break

            if check: return node
        return None

    def searchNodes(self, **parameters):
        """
        Returns a list of nodes with the specified parameters. If nothing is specified,
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

# GETTERS

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

        while self.searchNode(ID = number):
            ct += 1
            number = incrementID(prefix, suffix, level, ct)

        return number

    def getNewNode(self, parent, classname):
        """
        Returns a new node given the parent and the type. The node isn't inserted in the
        tree, it is a temporary node instead, that has the values of the one that should
        be inserted as next with the given properties.

        Args:
            parent (ComponentNode): the future parent of this node
            classname (str): the classname of the node to be returned

        Returns:
            ComponentNode: the future node to be added
        """

        newNode = strToClass(classname)()

        if classname == 'LeafNode':
            parentPrefix = parent.getPrefix()
            ID = self.getNewNumber(parentPrefix, 5)
        elif classname == 'JigNode':
            ID = self.getNewNumber('JIG', 5)
        elif classname == 'PlaceholderNode':
            ID = self.getNewNumber('PLC', 5)
        elif classname == 'AssemblyNode':
            parentPrefix = parent.getPrefix()
            ID = self.getNewNumber(parentPrefix, parent.getLevel() + 1)
            newNode.setLevel(parent.getLevel() + 1)
        elif classname == 'MechanicalNode':
            ID = self.getNewNumber('MEH', 5)
        elif classname == 'ElectricalNode':
            ID = self.getNewNumber('ELH', 5)
        elif classname == 'ElectromechanicalNode':
            ID = self.getNewNumber('EMH', 5)
        elif classname == 'ProductNode':
            ID = self.getNewNumber('PRO', 5)
        elif classname == 'MeasuredNode':
            ID = self.getNewNumber('MMH', 5)
        else:
            ID = 'ERR'

        newNode.addFeatures(ID = ID)
        return newNode
