from ..bundles.AbstractFeatureBundle import AbstractFeatureBundle

class AbstractNode(AbstractFeatureBundle):
    """
    Class to represent a node in a generic tree structure.

    self.up
    self.children

    self.bundle
    """

    def __init__(self, **features):
        self.up = None
        self.children = []
        self.bundle = AbstractFeatureBundle(**features)

# INSERTION

    def addChild(self, newNode):
        """
        Appends a node to the children of this node.

        Args:
            newNode (AbstractNode): the node to be added

        Returns:
            bool: the success of the operation
        """

        return self.insertChild(newNode, len(self))

    def insertChild(self, newNode, position):
        """
        Adds a node to the children of this node in a specific position.

        Args:
            newNode (AbstractNode): the node to be added
            position (int): the position where to add the node

        Returns:
            bool: the success of the operation
        """

        if not 0 <= position <= len(self): return False

        self.children.insert(position, newNode)
        newNode.updateParent(self)
        return True

    def addChildren(self, newNodes):
        """
        Adds multiple nodes to the children of this node.

        Args:
            nodesList (list[AbstractNode]): the list of nodes to add
        """

        for newNode in newNodes:
            self.addChild(newNode)

    def updateParent(self, parentNode = None):
        """
        Sets this node's parent as the passed node.

        Args:
            parentNode (AbstractNode): the parent node of this node. Default to None.
        """

        self.up = parentNode

# REMOVAL

    def removeChild(self, node):
        """
        Locates and removes a node from the children if present.

        Args:
            node (AbstractNode): the node to remove

        Returns:
            bool: the success of the operation
        """

        if node in self.children:
            self.children.remove(node)
            return True
        return False

    def popChild(self, position):
        """
        Removes and returns the node at the specified position of the children list if present.

        Args:
            position (int): the position of the item to remove

        Returns:
            Abstract: the removed node if any or False
        """

        if 0 <= position < len(self):
            poppedNode = self.children.pop(position)
            poppedNode.updateParent()
            return poppedNode
        return False

    def removeChildren(self, nodesList):
        """
        Removes multiple nodes from the children list if present

        Args:
            nodesList (list[AbstractNode]): the nodes to remove
        """

        for node in nodesList:
            self.removeChild(node)

    def detach(self):
        """
        Detaches itself from the parent. This corresponds to removing this node from the
        tree and returning itself. This node becomes a new rooted tree.

        Returns:
            AbstractNode: the detached node
        """

        if not self.up: return self

        parent = self.getParent()
        index = self.getIndex()

        return parent.popChild(index)

# COPY

    def superficialCopy(self):
        """
        Copies and returns this node with only it's features. The parent and children
        are not copied.

        Returns:
            AbstractNode: a superficial copy of the node
        """

        copiedNode = self.__class__()
        copiedNode.replaceBundle(self.bundle.copy())
        return copiedNode

    def deepCopy(self):
        """
        Copies and returns this node with no parent but copied descendants.

        Returns:
            AbstractNode: the copied node
        """

        copiedNode = self.superficialCopy()
        copiedNode.updateParent()

        for child in self.children:
            copiedNode.addChild(child.deepCopy())

        return copiedNode

# FEATURES HANDLING

    def addFeature(self, featureKey, featureValue):
        """
        Adds a feature to this node's bundle or updates the ones already existing.

        Args:
            featureKey (str): the name of the feature
            featureValue (PyObject): the value of the feature to store
        """

        self.bundle.addFeature(featureKey, featureValue)

    def addFeatures(self, **features):
        """
        Adds an arbitrary number of features to this node's bundle or updates the ones
        already existing.
        """

        self.bundle.addFeatures(**features)

    def updateFeature(self, featureKey, featureValue):
        """
        Updates the value of a feature of this node's bundle.

        Args:
            featureKey (str): the feature to update
            featureValue (PyObject): the new value to substitute
        """

        self.bundle.updateFeature(featureKey, featureValue)

    def deleteFeature(self, featureKey):
        """
        Deletes a feature from this node's bundle.

        Args:
            featureKey (str): the feature to delete
        """

        self.bundle.deleteFeature(featureKey)

    def deleteFeatures(self, *featureKeys):
        """
        Deletes an arbitrary number of features from this node's bundle.
        """

        self.bundle.deleteFeatures(*featureKeys)

    def getFeature(self, featureKey):
        """
        Returns the value of the feature  in this node's bundle, specified by the passed key.
        None is returned if the key doesn't exist.

        Args:
            featureKey (str): the feature to return the value of

        Returns:
            PyObject: the value of the attribute under the given key
        """

        return self.bundle.getFeature(featureKey)

    def getFeatureKeys(self):
        """
        Returns the list of feature keys of this node.

        Returns:
            list[str]: the list of features of this node
        """

        return self.bundle.getBundleKeys()

    def replaceBundle(self, newBundle):
        """
        Replaces this node's bundle with a new passed in one.

        Args:
            newBundle (AbstractFeatureBundle): the new bundle
        """

        self.bundle = newBundle

    def getBundle(self):
        """
        Returns this node's bundle.

        Returns:
            AbstractFeatureBundle: the feature bundle of this node
        """

        return self.bundle

# VISITS ITERATORS

    def iterPreorder(self):
        """
        Iters through the descendants of this node recursively from root to leaf level.

        Yields:
            AbstractNode: the next descendant node to visit
        """

        yield self
        for child in self.children:
            yield from child.iterPreorder()

    def iterPostorder(self):
        """
        Iters through the descendants of this node recursively from leaf to root level.

        Yields:
            AbstractNode: the next descendant node to visit
        """

        for child in self.children:
            yield from child.iterPreorder()
        yield self

    def iterAncestors(self):
        """
        Iters through the ancestors of this node.

        Yields:
            AbstractNode: the next ancestor node to visit
        """

        yield self

        parent = self.getParent()
        if not parent: raise StopIteration

        while parent:
            yield parent
            parent = parent.getParent()

# GETTERS

    def getRoot(self):
        """
        Returns this node's root by the definition:

        root = the node that has no parent (None);

        Returns:
            AbstractNode: the root of this tree
        """

        for ancestorNode in self.iterAncestors():
            if not ancestorNode.getParent(): return ancestorNode
        return self

    def getParent(self):
        """
        Returns this node's parent.

        Returns:
            AbstractNode: the parent of this node
        """

        return self.up

    def getChildAt(self, position):
        """
        Returns the child at the specified position if valid.
        If the index is non-existent an error is printed and no exception
        is raised.

        Args:
            position (int): the position of the wanted child

        Returns:
            AbstractNode: the node at the specified position if present
        """

        if 0 <= position < len(self):
            return self.children[position]

    def getChildren(self):
        """
        Returns the children list.

        Returns:
            list[AbstractNode]: self.children of this node
        """

        return self.children

    def getDescendants(self):
        """
        Returns a list of the descendant nodes of this node.

        Returns:
            list[AbstractNode]: the list of descendant nodes
        """

        descendantsList = []
        for node in self.iterPreorder():
            descendantsList.append(node)
        return descendantsList

    def getAncestors(self):
        """
        Returns a list of the ancestor nodes.

        Returns:
            list[AbstractNode]: the list of ancestor nodes
        """

        ancestorsList = []
        for node in self.iterAncestors():
            ancestorsList.append(node)
        return ancestorsList

    def getLeaves(self):
        """
        Returns a list of leaf nodes in this node. A leaf is a node with no children.

        Returns:
            list[AbstractNode]: the list of leaf nodes
        """

        leavesList = []
        for node in self.iterPreorder():
            if len(node) == 0:
                leavesList.append(node)

        return leavesList

    def getHeight(self):
        """
        Returns this node's heigth based on the definition:

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
        Returns this node's depth based on the definition:

        - if the node is the root, depth = 0;
        - else depth = 1 + node's parent depth;

        Returns:
            int: this node's depth
        """

        if not self.getParent(): return 0

        return self.getParent().getDepth() + 1

    def getIndex(self):
        """
        Returns this node's index in it's parent list.

        Returns:
            int: the index of this node
        """

        parent = self.getParent()

        if not parent: return 0
        return parent.getChildren().index(self)

# REPRESENTATION

    def toString(self):
        """
        Returns a string version of the node with empty names.

        Returns:
            str: the node structure in string format
        """

        string = f'|-- {self.getIndex()}°'

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
