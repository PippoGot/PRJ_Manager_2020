import sys

from ..nodes.CompositeNodes import (
    ProjectNode, AssemblyNode, LeafNode,
    MechanicalNode, ElectricalNode, ElectromechanicalNode, MeasuredNode, ProductNode,
    JigNode, PlaceholderNode)

def strToClass(classname):
    """
    Returns a class from the classname given, if it is declared in this namespace.

    Args:
        classname (str): the class name

    Returns:
        Class: the class extracted from the string
    """

    return getattr(sys.modules[__name__], classname)

def classToStr(instance):
    """
    Returns the classname of a given instance.

    Args:
        instance (PyObject): the class instance from where to extract the classname

    Returns:
        str: the classname of the instance
    """

    return instance.__class__.__name__

def extractNode(data):
    """
    Traverse the json object and extracts the nodes from it in a tree data structure.
    The root of the tree is extracted.

    Args:
        data (dict[str, PyObject]): the json data

    Returns:
        AbstractNode: the root of the tree
    """

    if not data['children']:
        del data['children']
        classname = data['class']
        return strToClass(classname)(**data)

    classname = data['class']
    del data['class']
    if classname == 'AssemblyNode':
        parent = strToClass(classname)(level = data['level'])
    else:
        parent = strToClass(classname)()

    for childData in data['children']:
        child = extractNode(childData)
        parent.addChild(child)

    del data['children']
    parent.addFeatures(**data)

    return parent
