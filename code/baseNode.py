from math import ceil
from re import sub
from random import randint

class baseNode():

    def __init__(self, number, **features):
        self.up = None

        self.children = []
        self.number = number
        self.features = [
            'parentHash',
            'selfHash',
            'level',
            'number',
            'title',
            'description'
        ]

        self.updateHashes()
        self.addFeatures(**features)

# --- TREE FUNCTIONS ---

# DATA

    def addChild(self, node):
        """
        Adds a node to self.children of this node. See insertChild for more info.

        CUSTOM FUNCTIONS USED:
            insertChild()

        INPUT:
            baseNode - node: the node to be added

        RETURN TYPE: 
            bool: the success of the operation
        """

        return self.insertChild(node, len(self.children))

    def insertChild(self, node, position):
        """
        Insert a node to self.children of this node in a specified position.
        Then node.up, node.selfHash, node.parentHash are updated.

        CUSTOM FUNCTIONS USED:
            addFeatures()
            updateHashes()

        INPUT:
            baseNode - node: the node to be added

        RETURN TYPE: 
            bool: the success of the operation
        """

        if 0 <= position <= len(self.children):
            self.children.insert(position, node)
            setattr(node, 'up', self)
            node.addFeatures(parentHash = self.selfHash)
            node.updateHashes()
            return True
        return False

    def addChildren(self, nodesList):
        """
        Adds multiple nodes to self.children.

        CUSTOM FUNCTIONS USED:
            addChild()

        INPUT:
            list - nodesList: the list of nodes to add
        """

        for node in nodesList:
            self.addChild(node)

    def removeChild(self, node):
        """
        Locate and removes a node from self.children if present.

        INPUT:
            baseNode - node: the node to remove
            
        RETURN TYPE:
            bool: the success of the operation
        """

        if node in self.children:
            self.children.remove(node)
            return True
        return False

    def popChild(self, position):
        """
        Removes and returns the node at the specified position of self.children if present.

        INPUT:
            int - position: the position of the item to remove
            
        RETURN TYPE:
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

        CUSTOM FUNCTIONS USED:
            removeChild()

        INPUT:
            list - nodesList: the nodes to remove"""

        for node in nodesList:
            self.removeChild(node)

    def copy(self):
        """
        Copies and returns this node with only it's features. The parent and children are not copied.

        RETURN TYPE:
            baseNode: the copied node
        """

        newNode = baseNode()

        for key in features:
            value = getattr(self, key, None)
            setattr(newNode, key, value)

        return newNode

    def iterDescendants(self):
        """
        Iters through the descendants of this node recursively from top to bottom level.

        CUSTOM FUNCTIONS USED:
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

# GETTERS

    def getChildAt(self, position):
        """
        Returns the child at the specified position if valid.

        INPUT:
            int - position: the position of the wanted children
        """

        if 0 <= position < len(self.children):
            return self.children[position]

    def getParent(self):
        """
        Returns this node's parent.

        RETURN TYPE:
            baseNode/None: the self.up reference
        """

        return self.up

    def getChildren(self):
        """
        Returns self.children list.

        RETURN TYPE:
            list: self.children
        """

        return self.children

    def getRoot(self):
        """
        Returns this node's root by the definition

        root = the node that has no parent (None)

        RETURN TYPE:
            baseNode: the root of this tree
        """

        p = self.up
        while p:
            if not p.up:
                return p
            p = p.up
        return self

    def getHeigth(self):
        """
        Returns this node's heigth based on the definition:

        - if the node is a leaf, heigth = 0;
        - else heigth = 1 + max(node's children heigths);

        RETURN TYPE:
            int:the heigth ot this node
        """

        if len(self.children) == 0: return 0

        heigths = []
        for child in self.children:
            heigths.append(child.getHeigth())

        return max(heigths) + 1

    def getDepth(self):
        """
        Returns this node's depth based on the definition:

        - if the node is the root, depth = 0;
        - else depth = 1 + node's parent depth;

        CUSTOM FUNCTIONS USED:
            getDepth()

        RETURN TYPE:
            int: this node's depth
        """

        if not self.up:
            return 0

        return self.up.getDepth() + 1

    def getIndex(self):
        """
        Returns this node's index in it's parent list.

        RETURN TYPE:
            int: the index of this item in the self.up.children list
        """

        if self.up:
            return self.up.children.index(self)
        return 0

    def getNodeDictionary(self):
        """
        Returns a dictionary with every feature as key and it's value.

        RETURN TYPE:
            dict: the dictionary {features: values}
        """

        nodeDict = {}

        for feature in self.features:
            nodeDict[feature] = getattr(self, feature, None)

        return nodeDict

    def getTreeList(self):
        """
        Returns a list of nodes in dictionary format.

        CUSTOM FUNCTIONS USED:
            iterDescendants()
            getNodeDictionary()

        RETURN TYPE:
            list: the list of all the nodes of the tree as dictionary
        """

        treeList = []

        for node in self.iterDescendants():
            treeList.append(node.getNodeDictionary())

        return treeList

# REPRESENTATION

    def toString(self, tab = 0, *features):
        """
        Returns a string version of the tree with optional features.

        CUSTOM FUNCTIONS USED:
            getIndex()
            toString()
            getDepth()

        INPUT:
            int - tab: the number of spaces of indentation. Default as 0
            args - *features: optional features to display

        RETURN TYPE:
            str: the tree structure in string format
        """

        string = ''
        string += tab * '   ' + f'|-- {self.getIndex()}° - {self.number}'

        for key in features:
            value = getattr(self, key, None)
            string += f' - {value}'

        for child in self.children:
            string += '\n' + child.toString(child.getDepth(), *features)

        return string

    def __repr__(self):
        """
        Enables the print() function. See toString() for more details.

        CUSTOM FUNCTIONS USED:
            toString()

        RETURN TYPE:
            str: the tree in string format
        """

        return self.toString()

# --- COMPONENT FUNCTIONS ---

# DATA

    def addFeatures(self, **features):
        """
        Adds an arbitrary number of features to this instance or updates the ones already existing.

        INPUT:
            kwargs - **features: an arbitrary number of keyword arguments to add as features
        """

        for key, value in features.items():
            self.features.append(key)
            setattr(self, key, value)

    def delFeatures(self, *features):
        """
        Deletes an arbitrary number of features from this instance.

        INPUT:
            args - *features: an arbitrary number of feature names to remove from the instance
        """

        for key in features.items():
            if key in self.features:
                self.features.remove(key)
                delattr(self, key)

    def updateHashes(self, root = None):
        """
        Updates the hashes numbers of the descendants of this node checking that the number doesn't repeat.
        Also updates the children self.parentHashes.

        CUSTOM FUNCTIONS USED:
            getRoot()
            searchNode()
            addFeatures()
            updateHashes()

        INPUT:
            baseNode/None - root: the root of the tree where the operation should be started. Default is None
        """

        if not root:
            root = self.getRoot()

        newHash = random.randint(0, 99999999)

        while root.searchNode(selfHash = newHash):
            newHash = random.randint(0, 99999999)

        self.addFeatures(selfHash = newHash)

        for child in self.children:
            child.addFeatures(parentHash = self.selfHash)
            child.updateHashes()

# GETTERS

    def getSize(self):
        """
        Returns this node's size. The size is defined by the item number. Each digit has the following weigth:

        #      X      X      X      -      X      X      X
            36^3 + 36^4 + 36^5      +   36^2 + 36^1 + 36^0

        CUSTOM FUNCTIONS USED:
            unpackNumber()
            toBase10()

        RETURN TYPE:
            int: the size of the node
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

        RETURN TYPE:
            int: the level of this node
        """

        return self.level

    def getTotalCost(self):
        """
        Calculates and returns the cost of this component based on the total quantity of this component
        in the tree (assembly).

        CUSTOM FUNCTIONS USED:
            getTotalQuantity()

        RETURN TYPE:
            float: the total price of this item
        """

        quantity = self.getTotalQuantity()

        return ceil(quantity / self.package) * float(self.price) 

    def getTotalQuantity(self):
        """
        Calculates and returns the quantity of this node inside the tree (root node).

        CUSTOM FUNCTIONS USED:
            getRoot()
            getNodesList()
            iterAncecstor()

        RETURN TYPE:
            int: the total quantity of this item inside the tree
        """

        root = self.getRoot()
        componentsList = root.getNodesList(number = self.number)
        quantity = int(self.quantity)

        for node in componentsList:
            for ancestor in node.iterAncestor():
                quantity *= int(ancestor.quantity)

        return quantity

    def getNewNumber(self, prefix, level):
        """
        Calculates and returns the next available number for the specified prefix and level.
        The parents prefix number is passed if the new node is not a special type ( so if the new
        node is either a Project, Assembly or Part).

        CUSTOM FUNCTIONS USED:
            getRoot()
            incNumber()
            searchNode()

        INPUT:
            str - prefix: the prefix of the new item or of his parent
            int - level: the level of the new item

        RETURN TYPE:
            str: the next available number
        """

        root = self.getRoot()

        suffix = '000'
        ct = 1
        number = incNumber(prefix, suffix, level, ct)

        while root.searchNode(number = number):
            ct += 1
            number = incNumber(prefix, suffix, level, ct)

        return number

    def getNodesList(self, **features):
        """
        Returns a list of nodes with the specified features value. If nothing is specified,
        all of the nodes in the subtree will be returned.

        CUSTOM FUNCTIONS USED:
            iterDescendants()

        INPUT:
            kwargs - **features: an arbitrary number of attributes to use for the research

        RETURN TYPE:
            list/None: the list of the corresponding nodes found
        """

        searchList = []

        for node in self.iterDescendants():
            check = True

            for key, value in features.items():
                checkingValue = getattr(node, key, None)
                if not checkingValue == value:
                    check = False
                    break

            if check: searchList.append(node)

        return searchList

    def getLeavesList(self):
        """
        Returns a list of leaf nodes in this node. A leaf is a node with no children.

        CUSTOM FUNCTIONS USED:
            getNodesList()

        RETURN TYPE:
            list: the list of leaf nodes
        """

        leavesList = self.getNodesList(children = [])

        return leavesList

    def searchNode(self, **features):
        """
        Search for nodes with the specified features.
        If more than one is present in the tree, the first occurrence is returnded.

        CUSTOM FUNCTIONS USED:
            getNodeList()

        INPUT:
            kwargs - **features: an arbitrary number of features to use for the research of the node

        RETURN TYPE:
            baseNode/None: the first occurrence of the node that respects the passed attributes
        """

        searchList = self.getNodesList(**features)

        if searchList:
            return searchList[0]
        return None

# GLOBAL

VALUES = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def toBase36(number):
    """
    Converts a number from base 10 to base 36.

    INPUT:
        int - number: the base 10 number to be converted to base 36

    RETURN TYPE:
        str: the converted number
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

    INPUT:
        str - string: the string to convert from base 36 to base 10

    RETURN TYPE:
        int: the converted number
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

    CUSTOM FUNCTIONS USED:
        toBase36()
        toBase10()

    INPUT:
        str - prefix: the prefix of the number to increment
        int - level: where the increment should be done
        int - qty: the amount of increment

    RETURN TYPE:
        str: the incremented number converted to base 36
    """

    if not 1 < level < 5: return prefix

    if level == 2: return toBase36(toBase10(prefix[0]) + qty) + prefix[1:]

    if level == 3: return prefix[0] + toBase36(toBase10(prefix[1]) + qty) + prefix[2]

    if level == 4: return prefix[:2] + toBase36(toBase10(prefix[2]) + qty)

def incSuffix(suffix, level, qty):
    """
    Increments a string suffix of the specified amount.

    CUSTOM FUNCTIONS USED:
        toBase36()
        toBase10()

    INPUT:
        str - suffix: the number to increment
        int - level: where the increment should be done
        int - qty: the amount to increment the number

    RETURN TYPE:
        str: the incremented number converted to base 36
    """

    if level > 4:
        suffix = toBase36(toBase10(suffix) + qty)

    return suffix.zfill(3)

def incNumber(prefix, suffix, level, quantity):
    """
    Increments a complete number and returns it already packed.

    "#XXX-XXX"

    CUSTOM FUNCTIONS USED:
        incPrefix()
        incSuffix()
        packNumber()

    INPUT:
        str - prefix: the prefix of the number to increment
        str - suffix: the suffix of the number to increment
        int - level: where the increment should be done
        int - qty: the amount to increment the number

    RETURN TYPE:
        str: the incremented number
    """

    prefix = incPrefix(prefix, level, quantity)
    suffix = incSuffix(suffix, level, quantity)

    return packNumber(prefix, suffix)

def unpackNumber(stringNumber):
    """
    Removes the non alphanumerical characters from the string and returns the obtained string.

    INPUT:
        str - stringNumber: the string to clean

    RETURN TYPE:
        str: the cleaned string
    """

    stringNumber = stringNumber.upper()
    stringNumber = re.sub('[\W_]+', '', stringNumber)
    return stringNumber

def packNumber(prefix, suffix):
    """
    Composes and returns a number in the wanted format.

    #{prefix}-{suffix}

    INPUT:
        str - prefix: the first half of the number
        str - suffix: the second half of the number

    RETURN TYPE:
        str: the formatted number
    """

    return f'#{prefix}-{suffix}'


# HELPER CODE

if __name__ == '__main__':

    root = baseNode(number = '#000-000')

    child1 = baseNode(number = '#100-000', level = 0)
    child2 = baseNode(number = '#110-000', level = 0)
    child3 = baseNode(number = '#120-000')

    root.addChild(child1)
    child1.addChild(child3)
    child1.insertChild(child2, 1)

    print(root.toString(0, 'selfHash', 'parentHash'))