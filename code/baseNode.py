from math import ceil
import re
import random

class BaseNode():

# INITIALISATION

    def __init__(self, **features):
        self.up = None

        self.selfHash = 0
        self.number = ''
        self.level = 0
        self.package = 0
        self.price = 0
        self.quantity = 1
        self.title = 'Name'
        self.description = 'Description'
        self.status = 'Not Designed'
        self.commet = '-'

        self.children = []
        self.features = [
            'parentHash',   # identity hash of the parent
            'selfHash',     # identity hash of this node
            'level',        # level of the node in the tree
            'number',       # number of the node
            'title',        # name of the node
            'description',  # description of the node
            # 'type',         # type of the node
            # 'manufacture',  # fabrication specifications
            'status',       # advancement of the node
            'comment',      # optional comment
            # 'price',        # the price of this node
            'quantity',     # the quantity of this node
            # 'package',      # the quantity per package of this node
            # 'seller',       # the seller of this component node
            # 'kit',          # group of component sold together
            # 'link'          # the link to the shopping website
        ]

        self.updateHashes()
        self.initValues(**features)

    def initValues(self, **features):
        """
        Initializes the node to a default value.

        Custom functions:
            addFeature()
        """

        self.addFeatures(**features)

# INSERTION

    def addChild(self, node):
        """
        Adds a node to self.children of this node. See insertChild for more info.

        Custom functions:
            insertChild()

        Args:
            node [BaseNode]: the node to be added

        Returns:
            bool: the success of the operation
        """

        return self.insertChild(node, len(self.children))

    def insertChild(self, node, position):
        """
        Insert a node to self.children of this node in a specified position.
        Then node.up, node.selfHash, node.parentHash are updated.

        Custom functions:
            addFeatures()
            updateHashes()

        Args:
            node [BaseNode]: the node to be added
            position [int]: the position where to insert the node

        Returns:
            bool: the success of the operation
        """

        if 0 <= position <= len(self.children):
            self.children.insert(position, node)
            setattr(node, 'up', self)
            node.addFeatures(parentHash=self.selfHash)
            return True
        return False

    def addChildren(self, nodesList):
        """
        Adds multiple nodes to self.children.

        Custom functions:
            addChild()

        Args:
            nodesList [list[BaseNode]]: the list of nodes to add
        """

        for node in nodesList:
            self.addChild(node)

# REMOVAl

    def removeChild(self, node):
        """
        Locate and removes a node from self.children if present.

        Args:
            node [BaseNode]: the node to remove

        Returns:
            bool: the success of the operation
        """

        if node in self.children:
            self.children.remove(node)
            return True
        return False

    def popChild(self, position):
        """
        Removes and returns the node at the specified position of self.children if present.

        Args:
            position [int]: the position of the item to remove

        Returns:
            bool: the success of the operation
        """

        if 0 <= position < len(self.children):
            popped = self.children.pop(position)
            popped.up = None
            return popped
        return False

    def removeChildren(self, nodesList):
        """
        Removes multiple nodes from self.children if present.

        Custom functions:
            removeChild()

        Args:
            nodesList [list[BaseNode]]: the nodes to remove"""

        for node in nodesList:
            self.removeChild(node)

    def detach(self):
        """
        Detaches itself from the parent. Functions like a popChild() but on itself.

        Custom functions:
            popChild()
            getIndex()

        Returns:
            [BaseNode]: the detached node
        """

        if not self.up:
            return self

        parent = self.up
        index = self.getIndex()

        self.up = None

        return parent.popChild(index)

# COPY

    def copy(self):
        """
        Copies and returns this node with only it's features. The parent and children are not copied.

        Returns:
            [BaseNode]: the copied node
        """

        newNode = BaseNode()

        for key in self.features:
            value = convertToNumber(getattr(self, key, None))
            setattr(newNode, key, value)

        return newNode

    def deepCopy(self):
        """
        Copies and returns this node with parent and children.

        CUSTOM FUNCTION USED:
            addChild()

        Returns:
            [BaseNode]: the copied node
        """

        newNode = self.copy()

        for child in self.children:
            newNode.addChild(child.deepCopy())

        return newNode

# TRAVERSAL

    def iterDescendants(self):
        """
        Iters through the descendants of this node recursively from top to bottom level.

        Custom functions:
            iterDescendants()
        """

        yield self
        for child in self.children:
            yield from child.iterDescendants()

    def iterAncestor(self):
        """Iters through the ancestors of this node."""

        p = self.up

        if not p:
            raise StopIteration

        while p:
            yield p
            p = p.up

# FEATURES HANDLING

    def addFeatures(self, **features):
        """
        Adds an arbitrary number of features to this instance or updates the ones already existing.

        Args:
            **features [**kwargs]: an arbitrary number of keyword arguments to add as features
        """

        for key, value in features.items():
            if key not in self.features and value:
                self.features.append(key)

            if value:
                setattr(self, key, value)

    def updateFeature(self, key, value):
        """
        Updates the value of a feature of this node.

        Args:
            key [str]: the feature to update
            value [PyObject]: the new value to substitue
        """

        value = convertToNumber(value)
        setattr(self, key, value)

    def delFeatures(self, *features):
        """
        Deletes an arbitrary number of features from this instance.

        Args:
            *features [*args]: an arbitrary number of feature names to remove from the instance
        """

        for key in features:
            if key in self.features:
                self.features.remove(key)
                delattr(self, key)

# HASHING

    def updateHashes(self, root=None):
        """
        Updates the hashes numbers of the descendants of this node checking that the number doesn't repeat.
        Also updates the children self.parentHashes.

        Custom functions:
            getRoot()
            searchNode()
            addFeatures()
            updateHashes()

        Args:
            root [BaseNode]: the root of the tree where the operation should be started. Default is None
        """

        if not root:
            root = self.getRoot()

        newHash = random.randint(0, 99999999)

        while root.searchNode(selfHash=newHash):
            newHash = random.randint(0, 99999999)

        self.addFeatures(selfHash=newHash)

        for child in self.children:
            child.addFeatures(parentHash=self.selfHash)
            child.updateHashes(root)

# SEARCHING

    def searchNode(self, **features):
        """
        Search for nodes with the specified features.
        If more than one is present in the tree, the first occurrence is returnded.

        Custom functions:
            getNodesList()

        Args:
            **features [**kwargs]: an arbitrary number of features to use for the research of the node

        Returns:
            [BaseNode]: the first occurrence of the node that respects the passed attributes
        """

        searchList = self.getNodesList(**features)

        if searchList:
            return searchList[0]
        return None

# DEFINITION GETTERS

    def getRoot(self):
        """
        Returns this node's root by the definition

        root = the node that has no parent (None)

        Returns:
            [BaseNode]: the root of this tree
        """

        p = self.up
        while p:
            if not p.up:
                return p
            p = p.up
        return self

    def getParent(self):
        """
        Returns this node's parent.

        Returns:
            [BaseNode]: the self.up reference
        """

        return self.up

    def getChildAt(self, position):
        """
        Returns the child at the specified position if valid.

        Args:
            position [int]: the position of the wanted children
        """

        if 0 <= position < len(self.children):
            return self.children[position]

    def getChildren(self):
        """
        Returns self.children list.

        Returns:
            [list[BaseNode]]: self.children
        """

        return self.children

    def getDescendants(self):
        """
        Returns a list of the descendants nodes of this node.

        Custom functions:
            getNodesList()

        Returns:
            [list[BaseNode]]: the list of descendants nodes
        """

        return self.getNodesList()

    def getAncestors(self):
        """
        Returns a list of the ancestor nodes.

        Returns:
            [list[BaseNode]]: the list of ancestor nodes
        """

        ancestors = []

        for ancestor in self.iterAncestor():
            ancestors.append(ancestor)

        return ancestors

    def getHeigth(self):
        """
        Returns this node's heigth based on the definition:

        - if the node is a leaf, heigth = 0;
        - else heigth = 1 + max(node's children heigths);

        Returns:
            int:the heigth ot this node
        """

        if len(self.children) == 0:
            return 0

        heigths = []
        for child in self.children:
            heigths.append(child.getHeigth())

        return max(heigths) + 1

    def getDepth(self):
        """
        Returns this node's depth based on the definition:

        - if the node is the root, depth = 0;
        - else depth = 1 + node's parent depth;

        Custom functions:
            getDepth()

        Returns:
            [int]: this node's depth
        """

        if not self.up:
            return 0

        return self.up.getDepth() + 1

# TREE UTILITY GETTERS

    def getIndex(self):
        """
        Returns this node's index in it's parent list.

        Returns:
            [int]: the index of this item in the self.up.children list
        """

        if self.up:
            return self.up.children.index(self)
        return 0

    def getFeature(self, feature):
        """
        Returns the value of the passed key.

        Args:
            feature [str]: the feature to return the value of

        Returns:
            [PyObject]: the value of the key
        """

        value = convertToNumber(getattr(self, feature, None))

        return value

    def getNodesList(self, **features):
        """
        Returns a list of nodes with the specified features value. If nothing is specified,
        all of the nodes in the subtree will be returned.

        Custom functions:
            iterDescendants()

        Args:
            **features [**kwargs]: an arbitrary number of attributes to use for the research

        Returns:
            [list[BaseNode]]: the list of the corresponding nodes found
        """

        searchList = []

        for node in self.iterDescendants():
            check = True

            for key, value in features.items():
                checkingValue = getattr(node, key, None)
                if not checkingValue == value:
                    check = False
                    break

            if check:
                searchList.append(node)

        return searchList

    def getLeavesList(self):
        """
        Returns a list of leaf nodes in this node. A leaf is a node with no children.

        Custom functions:
            getNodesList()

        Returns:
            [list[BaseNode]]: the list of leaf nodes
        """

        leavesList = self.getNodesList(children=[])

        return leavesList

# MODEL UTILITY GETTERS

    def getPrefix(self):
        """
        Returns the first 3 digits of the number of this node.

        Returns:
            [str]: the number in base 36
        """

        return self.number[1:4]

    def getSize(self):
        """
        Returns this node's size. The size is defined by the item number. Each digit has the following weigth:

        #      X      X      X      -      X      X      X
            36^3 + 36^4 + 36^5      +   36^2 + 36^1 + 36^0

        Custom functions:
            unpackNumber()
            toBase10()

        Returns:
            [int]: the size of the node
        """

        stringNumber = unpackNumber(self.number)

        prefix = stringNumber[:4]
        suffix = stringNumber[4:]

        prefix = prefix[::-1]

        stringNumber = prefix + suffix

        return toBase10(stringNumber)

    def getLevel(self):
        """
        Returns this node's level.

        Returns:
            [int]: the level of this node
        """

        return self.getFeature('level')

    def getTotalCost(self):
        """
        Calculates and returns the cost of this component based on the total quantity of this component
        in the tree (assembly).

        Custom functions:
            getTotalQuantity()
            getFeature()

        Returns:
            float: the total price of this item
        """

        quantity = self.getTotalQuantity()
        package = self.getFeature('package')
        if not package or package == 0: package = 1

        return ceil(quantity / package) * self.getFeature('price')

    def getTotalQuantity(self):
        """
        Calculates and returns the quantity of this node inside the tree (root node).

        Custom functions:
            getRoot()
            getNodesList()
            iterAncecstor()

        Returns:
            [int]: the total quantity of this item inside the tree
        """

        root = self.getRoot()
        componentsList = root.getNodesList(number=self.getFeature('number'))
        quantity = 0

        for node in componentsList:
            currentQuantity = node.getFeature('quantity')
            for ancestor in node.iterAncestor():
                currentQuantity *= ancestor.getFeature('quantity')

            quantity += currentQuantity

        return quantity

    def getNewNumber(self, prefix, level):
        """
        Calculates and returns the next available number for the specified prefix and level.
        The parents prefix number is passed if the new node is not a special type ( so if the new
        node is either a Project, Assembly or Part).

        Custom functions:
            getRoot()
            incNumber()
            searchNode()

        Args:
            prefix [str]: the prefix of the new item or of his parent
            level [int]: the level of the new item

        Returns:
            [str]: the next available number
        """

        root = self.getRoot()

        suffix = '000'
        ct = 1
        number = incNumber(prefix, suffix, level, ct)

        while root.searchNode(number=number):
            ct += 1
            number = incNumber(prefix, suffix, level, ct)

        return number

# REPRESENTATION GETTERS

    def getNodeString(self):
        """
        Returns a string of the current node features, except for the hashes and the level.
        Used for model filtering.

        Returns:
            [str]: the node string
        """

        output = ''
        for key in self.features:
            value = self.getFeature(key)
            if value and key not in ['selfHash', 'parentHash', 'level', 'color', 'icon']:
                output += f'{value} '

        return output

    def getTreeList(self):
        """
        Returns a list of nodes in dictionary format.

        Custom functions:
            iterDescendants()
            getNodeDictionary()

        Returns:
            [list[BaseNode]]: the list of all the nodes of the tree as dictionary
        """

        treeList = []

        for node in self.iterDescendants():
            treeList.append(node.getNodeDictionary())

        return treeList

    def getNodeDictionary(self, *features):
        """
        Returns a dictionary with every feature as key and it's value.

        Custom functions:
            getAttribute()

        Args:
            *features [*args]: the feature to include in the dictionary

        Returns:
            [dict]: the dictionary {features: values}
        """

        nodeDict = {}

        for feature in features:
            nodeDict[feature] = self.getFeature(feature)

        return nodeDict

# STRING CONVERSION

    def toString(self, tab=0, *features):
        """
        Returns a string version of the tree with optional features.

        Custom functions:
            getIndex()
            toString()
            getDepth()

        Args:
            tab [int]: the number of spaces of indentation. Default as 0
            *features [*args]: optional features to display

        Returns:
            [str]: the tree structure in string format
        """

        string = ''
        number = self.getFeature('number')
        string += tab * '   ' + f'|-- {self.getIndex()}° - {number}'

        for key in features:
            value = getattr(self, key, None)
            string += f' - {value}'

        for child in self.children:
            string += '\n' + child.toString(child.getDepth(), *features)

        return string

# DUNDER METHODS

    def __eq__(self, other):
        """
        Enables the == operator

        Custom functions:
            getSize()

        Args:
            other [PyObject]: the item to compare this item with

        Returns:
            bool: the result of the comparison
        """

        if isinstance(other, BaseNode):
            return other.getSize() == self.getSize()
        return False

    def __repr__(self):
        """
        Enables the print() function. See toString() for more details.

        Custom functions:
            toString()

        Returns:
            [str]: the tree in string format
        """

        return self.toString()

# GLOBAL

VALUES = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def toBase36(number):
    """
    Converts a number from base 10 to base 36.

    Args:
        number [int]: the base 10 number to be converted to base 36

    Returns:
        [str]: the converted number
    """

    outputCharacters = []

    while number > 0:
        number, rest = divmod(number, 36)
        outputCharacters.append(VALUES[rest])

    outputCharacters.reverse()
    outputCharacters = ''.join(outputCharacters)

    return outputCharacters

def toBase10(string):
    """
    Converts a string to a number from base 36 to base 10.

    Args:
        string [str]: the string to convert from base 36 to base 10

    Returns:
        [int]: the converted number
    """

    output = 0
    x = len(string) - 1

    for char in string:
        output += VALUES.index(char.upper()) * (36 ** x)
        x -= 1

    return output

def incPrefix(prefix, level, qty):
    """
    Increments a string prefix of the specified amount in a certain way.

    YXX if level = 2
    XYX if level = 3
    XXY if level = 4
    unchanged if level not in {2, 3, 4}

    Custom functions:
        toBase36()
        toBase10()

    Args:
        prefix [str]: the prefix of the number to increment
        level [int]: where the increment should be done
        qty [int]: the amount of increment

    Returns:
        [str]: the incremented number converted to base 36
    """

    if not 1 < level < 5:
        return prefix

    if level == 2:
        return toBase36(toBase10(prefix[0]) + qty) + prefix[1:]

    if level == 3:
        return prefix[0] + toBase36(toBase10(prefix[1]) + qty) + prefix[2]

    if level == 4:
        return prefix[:2] + toBase36(toBase10(prefix[2]) + qty)

def incSuffix(suffix, level, qty):
    """
    Increments a string suffix of the specified amount.

    Custom functions:
        toBase36()
        toBase10()

    Args:
        suffix [str]: the number to increment
        level [int]: where the increment should be done
        qty [int]: the amount to increment the number

    Returns:
        [str]: the incremented number converted to base 36
    """

    if level > 4:
        suffix = toBase36(toBase10(suffix) + qty)

    return suffix.zfill(3)

def incNumber(prefix, suffix, level, quantity):
    """
    Increments a complete number and returns it already packed.

    "#XXX-XXX"

    Custom functions:
        incPrefix()
        incSuffix()
        packNumber()

    Args:
        prefix [str]: the prefix of the number to increment
        suffix [str]: the suffix of the number to increment
        level [int]: where the increment should be done
        qty [int]: the amount to increment the number

    Returns:
        [str]: the incremented number
    """

    prefix = incPrefix(prefix, level, quantity)
    suffix = incSuffix(suffix, level, quantity)

    return packNumber(prefix, suffix)

def unpackNumber(stringNumber):
    """
    Removes the non alphanumerical characters from the string and returns the obtained string.

    Args:
        stringNumber [str]: the string to clean

    Returns:
        [str]: the cleaned string
    """

    stringNumber = stringNumber.upper()
    stringNumber = re.sub(r'[\W_]+', '', stringNumber)
    return stringNumber

def packNumber(prefix, suffix):
    """
    Composes and returns a number in the wanted format.

    #{prefix}-{suffix}

    Args:
        prefix [str]: the first half of the number
        suffix [str]: the second half of the number

    Returns:
        [str]: the formatted number
    """

    return f'#{prefix}-{suffix}'

def convertToNumber(value):
    """
    Converts a string value to an int or a float if possible.

    Args:
        value (str): the value to convert

    Returns:
        object: the converted value if possible or the input if not possible
    """

    if type(value) not in [type(5), type('str'), type(14.5)]:
        return value

    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value

# HELPER CODE

if __name__ == '__main__':

    root = BaseNode(number='root')

    child1 = BaseNode(number='1', level=0)
    child2 = BaseNode(number='2', level=0)
    child3 = BaseNode(number='3')

    root.addChild(child1)
    child1.addChild(child3)
    child1.insertChild(child2, 1)

    print(convertToNumber('5'), type(convertToNumber('5')))
