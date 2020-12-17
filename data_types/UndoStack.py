class UndoStack():
    """
    Class to store the various phases of a file editing. Stores changes
    in a stack and provides traversal methods to undo and redo modifications
    of files.
    """

# INIT

    def __init__(self, overflow = 100):
        """
        Initializes a new UndoStack with the passed (or default) overflow value.

        Args:
            overflow (int): the maximum number of changes stored in this stack. Defaults to 100.
        """

        self.overflow = overflow
        self.memory = []
        self.head = 0

# CHANGES MANAGEMENT

    def addSnapshot(self, snapshot, name = 'unnamed change'):
        """
        Adds a new change snapshot to the stack. Before doing so it clears the
        redo segment (items ahead of the head). After adding the snapshot clears
        the overflow.

        Args:
            snapshot (PyObject): the save item
            name (str): the name of the change performed. Default at unnamed change.
        """

        self._clearRedoSegment()

        snapshot = (snapshot, name)
        self.memory.insert(0, snapshot)

        self._clearOverflow()

    def undo(self):
        """
        If possible, move the head back one position (increments it) and returns
        the saved item at that position, otherwise the current item is returned.

        Returns:
            PyObject: the stored item
        """

        if self._isEmpty(): return

        if self.head + 1 < len(self.memory) and not self._isEmpty():
            self.head += 1

        snapshot, _ = self.memory[self.head]
        return snapshot

    def redo(self):
        """
        If possible, move the head one position ahead (decrements it) and returns the
        saved item at that position, otherwise the current item is returned.

        Returns:
            PyObject: the stored item
        """

        if self._isEmpty(): return

        if self.head - 1 >= 0:
            self.head -= 1

        snapshot, _ = self.memory[self.head]
        return snapshot

# UTILITY

    def _clearRedoSegment(self):
        """
        Removes the items in the list segment between index 0 and the head value.
        """

        if self._isEmpty(): return

        for x in range(self.head):
            self.memory.pop(x)

        self.head = 0

    def _clearOverflow(self):
        """
        Removes the items with index greater than the overflow value.
        """

        if self._isEmpty(): return

        if len(self.memory) >= self.overflow:
            for _ in range(len(self.memory) - self.overflow):
                self.memory.pop(-1)

    def _isEmpty(self):
        """
        Returns the emptiness of the stack.

        Returns:
            True: the stack is empty
            False: the stack is not empty
        """

        return not self.memory

# REPRESENTATION

    def toString(self):
        """
        Returns a string version of this item. Both the latest change and the
        current change are marked.

        Returns:
            str: this item in string format
        """

        string = ''
        for snapshot, name in self.memory:
            string += f'{name}'
            if self.memory.index((snapshot, name)) == self.head:
                string += f' <-- current change'
            if self.memory.index((snapshot, name)) == 0:
                string += ' <-- latest change'
            string += '\n'

        return string

# DUNDERS

    def __repr__(self):
        return self.toString()

    def __str__(self):
        return self.toString()
