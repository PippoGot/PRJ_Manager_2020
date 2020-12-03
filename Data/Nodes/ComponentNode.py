from random import randint

from .ADTutil import unpackID, toBase10

from .AbstractNode import AbstractNode
from .Bundles.ComponentFeatureBundle import ComponentFeatureBundle

class ComponentNode(AbstractNode):
    """
    self.selfHash
    self.parentHash
    self.level
    self.editable
    """

    def __init__(self, **features):
        super().__init__()
        self.bundle = ComponentFeatureBundle(**features)

        self.selfHash = randint(0, 99999)
        self.parentHash = None
        self.level = 0
        self.editable = True

# UTILITY GETTERS

    def getPrefix(self):
        """
        Returns the first 3 digits of the number of this node.

        Returns:
            str: the prefix number in base 36
        """

        numberID = self.bundle.getFeature('numberID')
        if not numberID: return

        return numberID[1:4]

    def getSize(self):
        """
        Returns this node's size. The size is defined by the item number.
        Each digit has the following weigth:

              X      X      X             X      X      X
            36^5 + 36^4 + 36^3      +   36^2 + 36^1 + 36^0

        Returns:
            int: the size of this node
        """

        numberID = unpackID(self.bundle.getFeature('numberID'))

        if numberID:
            prefix = numberID[:4]
            suffix = numberID[4:]

            numberID = prefix + suffix

            return toBase10(numberID)
        return 0

    def getLevel(self):
        """
        Returns this node's level.

        Returns:
            int: the level of this node
        """

        return self.level

    def isEditable(self):
        """
        Returns the editability of this node

        Returns:
            bool: if this node's manufacture can be edited
        """

        return self.editable

# REPRESENTATION GETTERS

    def getNodeString(self):
        """
        Returns a string of the current node features, except for hashes, level and gui
        properties. Used for model filtering in the application.

        Returns:
            str: the node string
        """

        valuesList = self.bundle.getBundleValues()
        return ' '.join(valuesList)

    def getNodeDictionary(self, *featureKeys):
        """
        Returns a dictionary with every feature as key and it's value.

        Returns:
            dict: the dictionary {features: values}
        """

        return self.bundle.getSelectedFeatures(*featureKeys)

    def toString(self, *featureKeys):
        """
        Returns a string version of the tree with optional features. The string is tabbed
        to represent the different tree levels.

        Args:
            tab (int): the number of spaces of indentation. Default as 0.

        Returns:
            str: the tree structure in string format
        """

        string = f'|-- {self.getIndex()}°'

        for featureKey in featureKeys:
            featureValue = self.bundle.getFeature(featureKey)
            string += f' - {featureValue}'

        return string

# DUNDERS

    def __str__(self):
        return self.toString(*self.bundle.getBundleKeys())

    def __repr__(self):
        return self.toString(*self.bundle.getBundleKeys())

    def __eq__(self, other):
        """
        Enables the "==" operator.

        Args:
            other (PyObject): the item to compare this item with

        Returns:
            bool: the result of the comparison
        """

        if isinstance(other, ComponentNode):
            return other.getSize() == self.getSize()
        return False


if __name__ == '__main__':
    pass