"""Implementing the Doubly Linked List ADT."""


class DLLNode:
    """Linked List Node."""

    def __init__(self, data):
        """Initialize the DLLNode class."""
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """Implementing Doubly Linked List ADT."""

    def __init__(self):
        """Initialize DoublyLinkedList class."""
        self._head = None
        self._curr = None
        self._tail = None

    def reset_to_head(self):
        """Reset the current pointer to head."""
        self._curr = self._head

    def reset_to_tail(self):
        """Reset the current pointer to tail."""
        self._curr = self._tail

    def add_to_head(self, data):
        """Add a new node to the head of the list."""
        new_node = DLLNode(data)
        new_node.next = self._head
        if self._head:
            self._head.prev = new_node
        self._head = new_node
        self.reset_to_head()
        if not self._head.next:
            self._tail = self._head

    def remove_from_head(self):
        """Remove a node from the head of the list and return data."""
        if not self._head:
            raise IndexError
        return_value = self._head.data
        self._head = self._head.next
        self.reset_to_head()
        if self._head:
            self._head.prev = None
        if not self._head:
            self._tail = None
        return return_value

    def move_forward(self):
        """Move forward through the list."""
        if not self._curr or not self._curr.next:
            raise IndexError
        self._curr = self._curr.next

    def move_backward(self):
        """Move backward through the list."""
        if not self._curr or not self._curr.prev:
            raise IndexError
        self._curr = self._curr.prev

    def move_back(self):
        """Move backward through the list."""
        if not self._curr or not self._curr.prev:
            raise IndexError
        self._curr = self._curr.prev

    @property
    def curr_data(self):
        """Return the data at the current position."""
        if not self._curr:
            raise IndexError
        return self._curr.data

    def add_after_current(self, data):
        """Add a node after the current position."""
        if not self._curr:
            raise IndexError
        new_node = DLLNode(data)
        if self._curr.next:
            self._curr.next.prev = new_node
        new_node.next = self._curr.next
        self._curr.next = new_node
        new_node.prev = self._curr

    def remove_after_current(self):
        """Remove the node after the current node, returning data."""
        if not self._curr or not self._curr.next:
            raise IndexError
        return_value = self._curr.next.data
        self._curr.next = self._curr.next.next
        if not self._curr.next:
            self._tail = self._curr
        if self._curr.next:
            self._curr.next.prev = self._curr
        if not self._head:
            self._tail = None
        return return_value

    def find(self, data):
        """Find and return an item in the list."""
        temp_curr = self._head
        while temp_curr:
            if temp_curr.data == data:
                return temp_curr.data
            temp_curr = temp_curr.next
        raise IndexError

    def remove(self, data):
        """Find and remove a node."""
        if not self._head:
            raise IndexError
        if self._head.data == data:
            return self.remove_from_head()
        temp_head = self._head
        while temp_head.next:
            if temp_head.next.data == data:
                return_value = temp_head.next.data
                temp_head.next = temp_head.next.next
                self.reset_to_head()
                if temp_head.next:
                    temp_head.next.prev = temp_head
                if not temp_head.next:
                    self._tail = temp_head
                return return_value
            temp_head = temp_head.next
        if not self._head:
            self._tail = None
        self.reset_to_head()
        raise IndexError

    def __iter__(self):
        self._curr_iter = self._head
        return self

    def __next__(self):
        if self._curr_iter is None:
            raise StopIteration
        ret_val = self._curr_iter.data
        self._curr_iter = self._curr_iter.next
        return ret_val
