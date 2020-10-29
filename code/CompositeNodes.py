from PyQt5 import QtGui as qtg
from BaseNode import BaseNode


class ProjectNode(BaseNode):
    def __init__(self, **features):
        super().__init__(
            level=1,
            number='#000-000',
            type='Project',
            manufacture='Assembled',
            color=qtg.QColor(255, 121, 65),
            icon=qtg.QIcon('code/resources/icons/project.png'),
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features. The parent and children are not copied.

        RETURN TYPE:
            BaseNode: the copied node
        """

        newNode = ProjectNode()

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode


class AssemblyNode(BaseNode):
    def __init__(self, number, level, **features):

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
            level=level,
            number=number,
            type=tp,
            manufacture=manufacture,
            manufactureEditable=manufactureEditable,
            icon=icon,
            color=colors[level - 2],
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features. The parent and children are not copied.

        RETURN TYPE:
            BaseNode: the copied node
        """

        newNode = AssemblyNode(self.getFeature('number'), self.getFeature('level'))

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode


class LeafNode(BaseNode):
    def __init__(self, number, **features):
        super().__init__(
            level=5,
            number=number,
            type='Part',
            manufactureEditable=True,
            color=qtg.QColor(179, 179, 179),
            icon=qtg.QIcon('code/resources/icons/part.png'),
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features. The parent and children are not copied.

        RETURN TYPE:
            BaseNode: the copied node
        """

        newNode = LeafNode(self.getFeature('number'))

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode


class HardwareNode(BaseNode):
    def __init__(self, number, **features):

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
            level=5,
            number=number,
            type='Hardware',
            manufacture='Off the Shelf',
            manufactureEditable=False,
            color=qtg.QColor(246, 246, 246),
            icon=icons[prefix],
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features. The parent and children are not copied.

        RETURN TYPE:
            BaseNode: the copied node
        """

        newNode = HardwareNode(self.getFeature('number'))

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode


class MeasuredNode(BaseNode):
    def __init__(self, number, **features):
        super().__init__(
            level=5,
            number=number,
            type='Hardware',
            manufacture='Cut to Length',
            manufactureEditable=False,
            color=qtg.QColor(246, 246, 246),
            icon=qtg.QIcon('code/resources/icons/measured.png'),
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features. The parent and children are not copied.

        RETURN TYPE:
            BaseNode: the copied node
        """

        newNode = MeasuredNode(self.getFeature('number'))

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode


class PlaceholderNode(BaseNode):
    def __init__(self, number, level, **features):
        super().__init__(
            level=level,
            number=number,
            type='Placeholder',
            status='Not Designed',
            color=qtg.QColor(148, 223, 255),
            icon=qtg.QIcon('code/resources/icons/placeholder.png'),
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features. The parent and children are not copied.

        RETURN TYPE:
            BaseNode: the copied node
        """

        newNode = PlaceholderNode(self.getFeature('number'), self.getFeature('level'))

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode


class JigNode(BaseNode):
    def __init__(self, number, level, **features):
        super().__init__(
            level=level,
            number=number,
            type='Jig',
            manufactureEditable=True,
            color=qtg.QColor(108, 201, 255),
            icon=qtg.QIcon('code/resources/icons/jig.png'),
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features. The parent and children are not copied.

        RETURN TYPE:
            BaseNode: the copied node
        """

        newNode = JigNode(self.getFeature('number'), self.getFeature('level'))

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode


class ConsumableNode(BaseNode):
    def __init__(self, number, **features):
        super().__init__(
            level=5,
            number=number,
            type='Consumable',
            manufacture='Product',
            manufactureEditable=False,
            color=qtg.QColor(246, 246, 246),
            icon=qtg.QIcon('code/resources/icons/consumable.png'),
            **features
        )

    def copy(self):
        """
        Copies and returns this node with only it's features. The parent and children are not copied.

        RETURN TYPE:
            BaseNode: the copied node
        """

        newNode = ConsumableNode(self.getFeature('number'))

        for key in self.features:
            value = self.getFeature(key)
            setattr(newNode, key, value)

        return newNode
