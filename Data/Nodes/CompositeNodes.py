from PyQt5 import QtGui as qtg

from .ComponentNode import ComponentNode

from UIs import resources

# ASSEMBLY

class ProjectNode(ComponentNode):
    """
    self.level = 1
    self.numberID = #000-000
    self.type = Project
    self.manufacture = Assembled
    self.editable = False
    """

    def __init__(self, **features):
        super().__init__(**features)

        self.editable = False
        self.level = 1
        self.color = qtg.QColor(255, 121, 65)
        self.icon = qtg.QIcon(":/project.png")

        self.addFeatures(
            numberID = '#000-000',
            type = 'Project',
            manufacture = 'Assembled',
        )

class AssemblyNode(ComponentNode):
    def __init__(self, level, **features):
        super().__init__(**features)

        self.level = level
        colors = [
            qtg.QColor(255, 159, 81),
            qtg.QColor(255, 198, 77),
            qtg.QColor(255, 225, 93),
            qtg.QColor(179, 179, 179)
        ]

        if self.level == 5:
            self.editable = True
            self.icon = qtg.QIcon(":/part.png")

            self.addFeatures(type = 'Part')

        else:
            self.editable = False
            self.icon = qtg.QIcon(":/assembly.png")

            self.addFeatures(type = 'Assembly', manufacture = 'Assembled')

        self.color = colors[self.level - 2]

    # REIMPLEMENTATIONS

    def superficialCopy(self):
        """
        Copies and returns this node with only it's features. The parent and children
        are not copied.

        Returns:
            ComponentNode: a superficial copy of the node
        """

        copiedNode = self.__class__(self.getLevel())
        copiedNode.replaceBundle(self.bundle.copy())
        return copiedNode

class LeafNode(ComponentNode):
    """
    self.level = 5
    self.type = Part
    self.editable = True
    """

    def __init__(self, **features):

        super().__init__(**features)

        self.editable = True
        self.level = 5
        self.color = qtg.QColor(179, 179, 179)
        self.icon = qtg.QIcon(":/part.png")

        self.addFeatures(type = 'Part')

# HARDWARE AND PRODUCTS

class HardwareNode(ComponentNode):
    """
    self.level = 5
    self.ID prefix is one in [MEH, EMH, ELH]
    self.type = Hardware
    self.manufacture = Off the Shelf
    self.editable = False
    """

    def __init__(self, **features):
        super().__init__(**features)

        self.editable = False
        self.level = 5
        self.color = qtg.QColor(246, 246, 246)

        icons = {
            'MEH': qtg.QIcon(":/hardware.png"),
            'ELH': qtg.QIcon(":/electronic.png"),
            'EMH': qtg.QIcon(":/electromechanical.png")
        }
        self.icon = icons[self.getPrefix()]

        self.addFeatures(type = 'Hardware', manufacture = 'Off the Shelf')

class MeasuredNode(ComponentNode):
    """
    self.level = 5
    self.ID prefix = MMH
    self.type = Hardware
    self.manufacture = Cut to Length
    self.editable = False
    """

    def __init__(self, **features):
        super().__init__(**features)

        self.editable = False
        self.level = 5
        self.color = qtg.QColor(246, 246, 246)
        self.icon = qtg.QIcon(":/measured.png")

        self.addFeatures(type = 'Hardware', manufacture = 'Cut to Length')

class ProductNode(ComponentNode):
    """
    self.level = 5
    self.ID prefix = PRO
    self.type = Product
    self.manufacture = Off the Shelf
    self.editable = False
    """

    def __init__(self, **features):
        super().__init__(**features)

        self.editable = False
        self.level = 5
        self.color = qtg.QColor(246, 246, 246)
        self.icon = qtg.QIcon(":/consumable.png")

        self.addFeatures(type = 'Consumable', manufacture = 'Product')

# JIGS AND PLACEHOLDERS

class JigNode(ComponentNode):
    """
    self.ID prefix = JIG
    self.type = Jig
    self.editable = True
    """

    def __init__(self, level, **features):
        super().__init__(**features)

        self.editable = True
        self.level = level
        self.color = qtg.QColor(108, 201, 255)
        self.icon = qtg.QIcon(":/jig.png")

        self.addFeatures(type = 'Jig')

    # REIMPLEMENTATIONS

    def superficialCopy(self):
        """
        Copies and returns this node with only it's features. The parent and children
        are not copied.

        Returns:
            ComponentNode: a superficial copy of the node
        """

        copiedNode = self.__class__(self.getLevel())
        copiedNode.replaceBundle(self.bundle.copy())
        return copiedNode

class PlaceholderNode(ComponentNode):
    """
    self.ID prefix = PLC
    self.type = Placeholder
    self.manufacture = Not Designed
    self.editable = True
    """

    def __init__(self, level, **features):
        super().__init__(**features)

        self.editable = True
        self.level = level
        self.color = qtg.QColor(148, 223, 255)
        self.icon = qtg.QIcon(":/placeholder.png")

        self.addFeatures(type = 'Placeholder', status = 'Not Designed')

    # REIMPLEMENTATIONS

    def superficialCopy(self):
        """
        Copies and returns this node with only it's features. The parent and children
        are not copied.

        Returns:
            ComponentNode: a superficial copy of the node
        """

        copiedNode = self.__class__(self.getLevel())
        copiedNode.replaceBundle(self.bundle.copy())
        return copiedNode
