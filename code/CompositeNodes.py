from PyQt5 import QtGui as qtg
from BaseNode import BaseNode


class ProjectNode(BaseNode):
    """
    Subclass the BaseNode class.
    This class adds some default values valid only for this specific type of component.

    The Project node represents the whole project, it includes every component, assembly,
    jig or product used to build the final piece.

    Default values:
        level = 1
        number = #000-000
        type = Project
        manufacture = Assembled
    """

    def __init__(self, **features):
        """
        Calls the superclass constructor passing every kwargs passed to this constructor
        and the default kwargs of this particular node.

        Args:
            **features (kwargs): the arguments of this node.
        """

        super().__init__(
            level = 1,
            number = '#000-000',
            type = 'Project',
            manufacture = 'Assembled',
            color = qtg.QColor(255, 121, 65),
            icon = qtg.QIcon('code/resources/icons/project.png'),
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features.
        The parent and children are not copied.
        This replaces the superclass method changing the type of object copied.

        Custom functions:
            self.getFeature()

        Returns:
            ProjectNode: the copied node.
        """

        newNode = ProjectNode()

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode


class AssemblyNode(BaseNode):
    """
    Subclass the BaseNode class.
    This class adds some default values valid only for this specific type of component.

    The Assembly node includes the next levels of assembly of the project, from level 2
    to level 5. Level 5 corresponds to a Part node.
    """

    def __init__(self, number, level, **features):
        """
        Calls the superclass constructor passing every kwargs passed to this constructor
        and the default kwargs of this particular node.

        The values for type and manufacture are calculated before they are set.
        By that depends also the node icon, color and editability.

        Args:
            number (str): the number of this node.
            level (int): the level of this node.
            **features (kwargs): the arguments of this node.
        """

        if level == 5:
            tp = 'Part'
            manufacture = None
            manufactureEditable = True
            icon = qtg.QIcon('code/resources/icons/part.png')
        else:
            tp = 'Assembly'
            manufacture = 'Assembled'
            manufactureEditable = False
            icon = qtg.QIcon('code/resources/icons/assembly.png')

        colors = [
            qtg.QColor(255, 159, 81),
            qtg.QColor(255, 198, 77),
            qtg.QColor(255, 225, 93),
            qtg.QColor(179, 179, 179)
        ]

        super().__init__(
            level = level,
            number = number,
            type = tp,
            manufacture = manufacture,
            manufactureEditable = manufactureEditable,
            icon = icon,
            color = colors[level - 2],
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features.
        The parent and children are not copied.
        This replaces the superclass method changing the type of object copied.

        Custom functions:
            self.getFeature()

        Returns:
            AssemblyNode: the copied node.
        """

        newNode = AssemblyNode(self.getFeature('number'), self.getFeature('level'))

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode


class LeafNode(BaseNode):
    """
    Subclass the BaseNode class.
    This class adds some default values valid only for this specific type of component.

    The Leaf node represents the smallest component there can be in a project, not including
    hardware components and consumables.

    Default values:
        level = 5
        type = Part
    """

    def __init__(self, number, **features):
        """
        Calls the superclass constructor passing every kwargs passed to this constructor
        and the default kwargs of this particular node.

        Args:
            number (str): the number of this node.
            **features (kwargs): the arguments of this node.
        """

        super().__init__(
            level = 5,
            number = number,
            type = 'Part',
            manufactureEditable = True,
            color = qtg.QColor(179, 179, 179),
            icon = qtg.QIcon('code/resources/icons/part.png'),
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features.
        The parent and children are not copied.
        This replaces the superclass method changing the type of object copied.

        Custom functions:
            self.getFeature()

        Returns:
            LeafNode: the copied node.
        """

        newNode = LeafNode(self.getFeature('number'))

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode


class HardwareNode(BaseNode):
    """
    Subclass the BaseNode class.
    This class adds some default values valid only for this specific type of component.

    The Hardware node represents a hardware component, that can be either a screw, a nut,
    a motor, a PCB etc...

    Default values:
        level = 5
        number prefix is one in [MEH, EMH, ELH]
        type = Hardware
        manufacture = Off the Shelf
    """

    def __init__(self, number, **features):
        """
        Calls the superclass constructor passing every kwargs passed to this constructor
        and the default kwargs of this particular node.

        Checks if the prefix of the given number is right, otherwise it will be reported.
        The node icon is calculated from the prefix.

        Args:
            number (str): the number of this node.
            **features (kwargs): the arguments of this node.
        """

        prefix = number[1:4]
        if prefix not in ['MEH', 'ELH', 'EMH']:
            prefix = 'NOTIN'

        icons = {
            'MEH': qtg.QIcon('code/resources/icons/hardware.png'),
            'ELH': qtg.QIcon('code/resources/icons/electronic.png'),
            'EMH': qtg.QIcon('code/resources/icons/electromechanical.png'),
            'NOTIN': None
        }

        super().__init__(
            level = 5,
            number = number,
            type = 'Hardware',
            manufacture = 'Off the Shelf',
            manufactureEditable = False,
            color = qtg.QColor(246, 246, 246),
            icon = icons[prefix],
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features.
        The parent and children are not copied.
        This replaces the superclass method changing the type of object copied.

        Custom functions:
            self.getFeature()

        Returns:
            HardwareNode: the copied node.
        """

        newNode = HardwareNode(self.getFeature('number'))

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode


class MeasuredNode(BaseNode):
    """
    Subclass the BaseNode class.
    This class adds some default values valid only for this specific type of component.

    The Measured node representsa particular type of Hardware node.
    It is a material bought to a certain measure (length, surface...) that is then cut to size.
    An example can be a pipe, a wood board etc...

    Default values:
        level = 5
        number prefix = MMH
        type = Hardware
        manufacture = Cut to Length
    """

    def __init__(self, number, **features):
        """
        Calls the superclass constructor passing every kwargs passed to this constructor
        and the default kwargs of this particular node.

        Args:
            number (str): the number of this node.
            **features (kwargs): the arguments of this node.
        """

        super().__init__(
            level = 5,
            number = number,
            type = 'Hardware',
            manufacture = 'Cut to Length',
            manufactureEditable = False,
            color = qtg.QColor(246, 246, 246),
            icon = qtg.QIcon('code/resources/icons/measured.png'),
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features.
        The parent and children are not copied.
        This replaces the superclass method changing the type of object copied.

        Custom functions:
            self.getFeature()

        Returns:
            MeasuredNode: the copied node.
        """

        newNode = MeasuredNode(self.getFeature('number'))

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode


class PlaceholderNode(BaseNode):
    """
    Subclass the BaseNode class.
    This class adds some default values valid only for this specific type of component.

    The Placeholder node is used to remember to the user something that occupy that place
    that is yet to be designed and/or is expected to be in that place.

    Default values:
        number prefix = PLC
        type = Placeholder
        status = Not Designed
    """

    def __init__(self, number, level, **features):
        """
        Calls the superclass constructor passing every kwargs passed to this constructor
        and the default kwargs of this particular node.

        Args:
            number (str): the number of this node.
            level (int): the level of this node.
            **features (kwargs): the arguments of this node.
        """

        super().__init__(
            level = level,
            number = number,
            type = 'Placeholder',
            status = 'Not Designed',
            color = qtg.QColor(148, 223, 255),
            icon = qtg.QIcon('code/resources/icons/placeholder.png'),
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features.
        The parent and children are not copied.
        This replaces the superclass method changing the type of object copied.

        Custom functions:
            self.getFeature()

        Returns:
            PlaceholderNode: the copied node.
        """

        newNode = PlaceholderNode(self.getFeature('number'), self.getFeature('level'))

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode


class JigNode(BaseNode):
    """
    Subclass the BaseNode class.
    This class adds some default values valid only for this specific type of component.

    The Jig node represents a custom made tool to make the assembly easier. It can be
    a single piece or a simple assembly with other components, therefore the level can vary.

    Default values:
        number prefix = JIG
        type = Jig
    """

    def __init__(self, number, level, **features):
        """
        Calls the superclass constructor passing every kwargs passed to this constructor
        and the default kwargs of this particular node.

        Args:
            number (str): the number of this node.
            level (int): the level of this node.
            **features (kwargs): the arguments of this node.
        """

        super().__init__(
            level = level,
            number = number,
            type = 'Jig',
            manufactureEditable = True,
            color = qtg.QColor(108, 201, 255),
            icon = qtg.QIcon('code/resources/icons/jig.png'),
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features.
        The parent and children are not copied.
        This replaces the superclass method changing the type of object copied.

        Custom functions:
            self.getFeature()

        Returns:
            JigNode: the copied node.
        """

        newNode = JigNode(self.getFeature('number'), self.getFeature('level'))

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode


class ConsumableNode(BaseNode):
    """
    Subclass the BaseNode class.
    This class adds some default values valid only for this specific type of component.

    The Consumable node represents a product used for a specific job, for examples glues,
    3D printer filament, etc...

    Default values:
        level = 5
        number prefix = CON
        type = Consumable
        manufacture = Product
        status = Can't be Designed
    """

    def __init__(self, number, **features):
        """
        Calls the superclass constructor passing every kwargs passed to this constructor
        and the default kwargs of this particular node.

        Args:
            number (str): the number of this node.
            **features (kwargs): the arguments of this node.
        """

        super().__init__(
            level = 5,
            number = number,
            type = 'Consumable',
            manufacture = 'Product',
            status = 'Can\'t be Designed',
            manufactureEditable = False,
            color = qtg.QColor(246, 246, 246),
            icon = qtg.QIcon('code/resources/icons/consumable.png'),
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features.
        The parent and children are not copied.
        This replaces the superclass method changing the type of object copied.

        Custom functions:
            self.getFeature()

        Returns:
            ConsumableNode: the copied node.
        """

        newNode = ConsumableNode(self.getFeature('number'))

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode
