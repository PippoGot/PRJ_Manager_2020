from .ComponentNode import ComponentNode

# --- ASSEMBLY NODES ---

class ProjectNode(ComponentNode):
    def __init__(self, *keys, **features):
        super().__init__(*keys, **features)

        self.setEditable(False)
        self.color = (255, 121, 65)
        self.icon = "project.png"

        self.addFeatures(
            ID = '#000-000',
            type = 'Project',
            manufacture = 'Assembled',
        )

class AssemblyNode(ComponentNode):

    colors = [
        (255, 159, 81),
        (255, 198, 77),
        (255, 225, 93)
    ]

    def __init__(self, *keys, **features):
        super().__init__(*keys, **features)

        self.setEditable(False)
        self.icon = "assembly.png"

        self.addFeatures(
            type = 'Assembly',
            manufacture = 'Assembled'
        )

        level = self.getFeature('level')
        if level:
            self.setLevel(level)

    def setLevel(self, level):
        """
        Sets the level of the assembly node and it's color tuple.

        Args:
            level (int): the level of this assembly node
        """

        self.addFeatures(
            level = level,
            color = self.colors[level - 2]
        )

class LeafNode(ComponentNode):
    def __init__(self, *keys, **features):

        super().__init__(*keys, **features)

        self.setEditable(True)
        self.color = (179, 179, 179)
        self.icon = "part.png"

        self.addFeatures(type = 'Part')

# --- HARDWARE NODES ---

class HardwareNode(ComponentNode):
    def __init__(self, *keys, **features):
        super().__init__(*keys, **features)

        self.setEditable(False)
        self.color = (246, 246, 246)

        self.addFeatures(
            type = 'Hardware',
            manufacture = 'Off the Shelf'
        )

class MechanicalNode(HardwareNode):
    def __init__(self, *keys, **features):
        super().__init__(*keys, **features)

        self.icon = "hardware.png"

class ElectricalNode(HardwareNode):
    def __init__(self, *keys, **features):
        super().__init__(*keys, **features)

        self.icon = "electronic.png"

class ElectromechanicalNode(HardwareNode):
    def __init__(self, *keys, **features):
        super().__init__(*keys, **features)

        self.icon = "electromechanical.png"

class MeasuredNode(HardwareNode):
    def __init__(self, *keys, **features):
        super().__init__(*keys, **features)

        self.icon = "measured.png"

        self.addFeatures(
            type = 'Hardware',
            manufacture = 'Cut to Length'
        )

class ProductNode(HardwareNode):
    def __init__(self, *keys, **features):
        super().__init__(*keys, **features)

        self.icon = "consumable.png"

        self.addFeatures(
            type = 'Consumable',
            manufacture = 'Product'
        )

# --- MISC NODES ---

class JigNode(ComponentNode):
    def __init__(self, *keys, **features):
        super().__init__(*keys, **features)

        self.setEditable(True)
        self.color = (108, 201, 255)
        self.icon = "jig.png"

        self.addFeatures(type = 'Jig')

class PlaceholderNode(ComponentNode):
    def __init__(self, *keys, **features):
        super().__init__(*keys, **features)

        self.setEditable(True)
        self.color = (148, 223, 255)
        self.icon = "placeholder.png"

        self.addFeatures(
            type = 'Placeholder',
            status = 'Not Designed'
        )
