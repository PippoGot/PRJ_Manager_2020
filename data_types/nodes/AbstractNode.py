class AbstractNode():
    """
    Class that describes the basic behaviour of a tree node.
    Provides insertion, deletion, copying, ancestor traversal, features
    and properties managers, representation and basic getters.
    """

# INIT

    def __init__(self, *keys, **features):
        """
        Initializes the class variables and adds all the passed features.
        """

        self.features = []
        self.up = None
        self.children = []

        self.addFeatures('ID', *keys, **features)

# INSERTION

    def insertChild(self, child, position):
        """
        Adds a node to the children of this node in a specific position.

        Args:
            child (AbstractNode): the node to add
            position (int): the position where to add the node

        Returns:
            True: successfully inserted the node
            False: position error
        """

        if not 0 <= position <= len(self): return False

        self.children.insert(position, child)
        child.up = self
        return True

    def addChild(self, child):
        """
        Appends a node to the children of this node.

        Args:
            child (AbstractNode): the node to add

        Returns:
            True: successfully added the node
            False: add error
        """

        return self.insertChild(child, len(self))

    def addChildren(self, children):
        """
        Adds multiple nodes to the children of this node.

        Args:
            children (list[AbstractNode]): the list of nodes to add
        """

        for child in children:
            self.addChild(child)

# DELETION

    def removeChild(self, child):
        """
        Locates and removes a node from the children if present.

        Args:
            child (AbstractNode): the node to remove

        Returns:
            True: successfully removed the node
            False: position error
        """

        if child not in self.children: return False

        self.children.remove(child)
        return True

    def removeChildren(self, children):
        """
        Removes multiple nodes from the children list if present

        Args:
            children (list[AbstractNode]): the nodes to remove
        """

        for child in children:
            self.removeChild(child)

    def popChild(self, position):
        """
        Removes and returns the node at the specified position of the children list if present.

        Args:
            position (int): the position of the item to remove

        Returns:
            AbstractNode: the popped node
            False: position error
        """

        if not 0 <= position < len(self): return False

        poppedNode = self.children.pop(position)
        poppedNode.up = None
        return poppedNode

    def detach(self):
        """
        Detaches this node from the parent. This corresponds to removing this node from the
        tree and returning itself. This node becomes a new rooted tree.

        Returns:
            AbstractNode: this detached node
        """

        if not self.up: return self

        return self.up.popChild(self.getIndex())

# TRAVERSAL

    def iterAncestors(self):
        """
        Iters through the ancestors of this node, this node included.

        Yields:
            AbstractNode: the next ancestor node to visit
        """

        yield self
        parent = self.up
        while parent:
            yield parent
            parent = parent.up

# COPY

    def superficialCopy(self):
        """
        Returns a copy of this node with only it's features. The parent and children
        are not copied.

        Returns:
            AbstractNode: a superficial copy of this node
        """

        data = self.items().copy()
        copiedNode = self.__class__(**data)

        return copiedNode

    def deepCopy(self):
        """
        Returns a copy of this node with descendants.

        Returns:
            AbstractNode: the copied node
        """

        copiedNode = self.superficialCopy()

        for child in self.children:
            copiedNode.addChild(child.deepCopy())

        return copiedNode

# FEATURES

    def addFeature(self, key, value):
        """
        Adds a feature to this node or updates the ones already existing.

        Args:
            key (str): the name of the feature
            value (PyObject): the value of the feature to store
        """

        setattr(self, key, value)
        if not key in self.features:
            self.features.append(key)

    def addFeatures(self, *keys, **features):
        """
        Adds an arbitrary number of features to this nodd or updates the ones
        already existing.
        """

        for key in keys:
            self.addFeature(key, None)

        for key, value in features.items():
            self.addFeature(key, value)

    def delFeature(self, key):
        """
        Deletes a feature from this node.

        Args:
            key (str): the feature to delete
        """

        delattr(self, key)
        if key in self.features:
            self.features.remove(key)

    def delFeatures(self, *keys):
        """
        Deletes an arbitrary number of features from this node.
        """

        for key in keys:
            self.delFeature(key)

    def getFeature(self, key):
        """
        Returns the value of the feature in this node, specified by the passed key.
        None is returned if the key doesn't exist.

        Args:
            key (str): the feature to return the value of

        Returns:
            PyObject: the value of the attribute under the given key
            None: key doesn't exist
        """

        return getattr(self, key, None)

    def getFeatures(self, *keys):
        """
        Returns this node feature dictionary with only selected keys.

        Returns:
            dict[str, PyObject]: the dictionary with the passed feature keys and values
        """

        data = {}
        for key in keys:
            data[key] = self.getFeature(key)

        return data

    def keys(self):
        """
        Returns the list of feature keys of this node.

        Returns:
            list[str]: the list of features keys of this node
        """

        return self.features

    def values(self):
        """
        Returns the list of feature values of this node.

        Returns:
            list[PyObject]: the list of features values of this node
        """

        values = []
        for key in self.features:
            value = self.getFeature(key)
            if value:
                values.append(value)

        return values

    def items(self):
        """
        Returns this node feature dictionary.

        Returns:
            dict[str, PyObject]: the dictionary of this node's features
        """

        return self.getFeatures(*self.features)

# GETTERS

    def getParent(self):
        """
        Returns this node's parent.

        Returns:
            AbstractNode: the parent of this node
        """

        return self.up

    def getChildren(self):
        """
        Returns the children list of this node.

        Returns:
            list[AbstractNode]: children of this node
        """

        return self.children

    def getChildAt(self, position):
        """
        Returns the child at the specified position if valid.

        Args:
            position (int): the position of the wanted child

        Returns:
            AbstractNode: the node at the specified position if present
            None: position error
        """

        if not 0 <= position < len(self): return

        return self.children[position]

    def getIndex(self):
        """
        Returns this node's index in it's parent list.

        Returns:
            int: the index of this node
        """

        if not self.up: return 0
        return self.up.children.index(self)

    def getHeight(self):
        """
        Returns this node's heigth.

        - if the node is a leaf, heigth = 0;
        - else heigth = 1 + max(node's children heigths);

        Returns:
            int: the heigth ot this node
        """

        if len(self) == 0: return 0

        heights = []
        for child in self.getChildren():
            heights.append((child.getHeight()))

        return max(heights) + 1

    def getDepth(self):
        """
        Returns this node's depth.

        - if the node is the root, depth = 0;
        - else depth = 1 + node's parent depth;

        Returns:
            int: this node's depth
        """

        if not self.up: return 0

        return self.up.getDepth() + 1

# REPRESENTATION

    def toString(self):
        """
        Returns a string version of the node with every feature.

        Returns:
            str: the node structure in string format
        """

        string = ''
        for key in self.features:
            value = self.getFeature(key)
            string += f'{key}: {value},\n'
        return string

# DUNDERS

    def __len__(self):
        return len(self.children)

    def __repr__(self):
        return self.toString()

    def __str__(self):
        return self.toString()

    def __bool__(self):
        return True

    def __eq__(self, other):
        return self.getFeature('ID') == other.getFeature('ID')