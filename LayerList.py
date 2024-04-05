from DoublyLinkedList import DoublyLinkedList


class LayerList(DoublyLinkedList):

    def __init__(self, inputs: int, outputs: int, neurode_type):
        """Initializes LayerList with input and output layers of neurodes."""
        super().__init__()
        self._neurode_type = neurode_type
        if inputs < 0 or outputs < 0:
            raise IndexError
        input_layer = [self._neurode_type() for _ in range(inputs)]
        output_layer = [self._neurode_type() for _ in range(outputs)]
        self.add_to_head(output_layer)
        self.add_to_head(input_layer)
        self.link_layers()

    def link_layers(self):
        """Helper function to link layers."""
        for i in self._curr.data:
            i.reset_neighbors(
                self._curr.next.data, self._neurode_type.Side.DOWNSTREAM
            )
        for i in self._curr.next.data:
            i.reset_neighbors(
                self._curr.data, self._neurode_type.Side.UPSTREAM
            )

    def add_layer(self, num_nodes: int):
        """Adds a hidden layer of neurodes after the current layer."""
        if self._curr == self._tail:
            raise IndexError("Cannot add a layer after the output layer.")
        hidden_layer = [self._neurode_type() for _ in range(num_nodes)]
        self.add_after_current(hidden_layer)
        self.link_layers()
        self.move_forward()
        self.link_layers()
        self.reset_to_head()

    def remove_layer(self):
        """Removes the layer after the current layer."""
        if self._curr.next == self._tail or self._curr.next == self._tail:
            raise IndexError("Cannot remove the output layer or layer after.")
        self.remove_after_current()
        self.link_layers()

    @property
    def input_nodes(self):
        """Returns the input layer neurodes."""
        return self._head.data

    @property
    def output_nodes(self):
        """Returns the output layer neurodes."""
        return self._tail.data
