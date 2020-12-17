from .NODESutil import unpackID, toBase10
from .AbstractNode import AbstractNode

class ComponentNode(AbstractNode):
    """
    Class that describes the behaviour of a component node.
    Extends the AbstractNode class, provides getters and editable boolean.
    """

    HEADERS = [
        'ID',
        'name',
        'description',
        'comment',
        'packageQuantity',
        'quantity',
        'price',
        'type',
        'manufacture',
        'status',
        'seller',
        'link'
    ]

    def __init__(self, *keys, **features):
        """
        Initializes some defalut features to None, adds the passed features
        and sets the editable parameter to True.
        """

        self.HEADERS.extend(keys)
        super().__init__(*self.HEADERS, **features)

        self.editable = True

# GETTERS

    def getLevel(self):
        """
        Returns this nodes level inside the tree. Equivalent of the depth.

        Returns:
            int: the level of this node
        """

        return self.getDepth()

    def getSize(self):
        """
        Returns the ID of this node in decimal base.

        Returns:
            int: the converted ID
        """

        ID = self.getFeature('ID')
        if not ID: return 0

        ID = unpackID(ID)
        return toBase10(ID)

    def getPrefix(self):
        """
        Returns the first 3 digits of the ID.

        Returns:
            str: the first 3 digits of the ID
        """

        ID = self.getFeature('ID')
        if not ID: return

        ID = unpackID(ID)
        return ID[:3]

# BOOLEANS

    def setEditable(self, boolean):
        """
        Changes the editable property of this node.

        Args:
            boolean (bool): if this node is editable or not
        """

        self.editable = boolean

    def isEditable(self):
        """
        Returns the editable property of this node.

        Returns:
            True: editable node
            False: not editable node
        """

        return self.editable