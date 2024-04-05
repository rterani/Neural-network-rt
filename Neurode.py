"""Implementing the Neurode class."""
from __future__ import annotations
from enum import Enum
import random
from abc import ABC, abstractmethod


class MultiLinkNode(ABC):
    """Abstract base class for nodes giving them the ability to connect."""

    class Side(Enum):
        """Enum to distinguish between upstream and downstream nodes."""
        UPSTREAM = 1
        DOWNSTREAM = 2

    def __init__(self):
        """Initialize tracking methods for reporting nodes and neighbors."""
        self._reporting_nodes = {self.Side.UPSTREAM: 0, self.Side.DOWNSTREAM: 0}
        self._reference_value = {self.Side.UPSTREAM: 0, self.Side.DOWNSTREAM: 0}
        self._neighbors = {self.Side.UPSTREAM: [], self.Side.DOWNSTREAM: []}

    def __str__(self):
        """Return a string representation showing node IDs and their neighbors."""
        upstream_ids = [id(node) for node in self._neighbors[self.Side.UPSTREAM]]
        downstream_ids = [id(node) for node in self._neighbors[self.Side.DOWNSTREAM]]
        return f"Node ID: {id(self)}\nUpstream Neighbors: {upstream_ids}\nDownstream Neighbors: {downstream_ids}"

    @abstractmethod
    def _process_new_neighbor(self, node: MultiLinkNode, side: Side):
        """Define how new neighbors are processed."""
        pass

    def reset_neighbors(self, nodes: list, side: Side):
        """Add neighbor nodes from a list, clearing any previous nodes."""
        self._neighbors[side] = nodes.copy()
        for node in nodes:
            self._process_new_neighbor(node, side)
        self._reference_value[side] = (1 << len(nodes)) - 1
        self._reporting_nodes[side] = 0


class Neurode(MultiLinkNode):
    """Represents the neurode class."""
    _learning_rate = 0.05

    @property
    def learning_rate(self):
        """Return the current learning rate."""
        return Neurode._learning_rate

    @learning_rate.setter
    def learning_rate(self, value):
        """Set a new learning rate."""
        Neurode._learning_rate = value

    def __init__(self):
        """Initialize the neurode with default values."""
        self._value = 0
        self._weights = {}
        super().__init__()

    def _process_new_neighbor(self, node, side):
        """Assign a random weight to a new upstream neighbor."""
        if side == MultiLinkNode.Side.UPSTREAM:
            self._weights[node] = random.random()

    def _check_in(self, node, side):
        """Check if all neighbor nodes have reported."""
        if node in self._neighbors[side]:
            node_index = self._neighbors[side].index(node)
            self._reporting_nodes[side] |= 1 << node_index
            if self._reporting_nodes[side] == self._reference_value[side]:
                self._reporting_nodes[side] = 0
                return True
        return False

    def get_weight(self, node):
        """Retrieve the weight associated with a node."""
        return self._weights.get(node)

    @property
    def value(self):
        """Return the neurode's current value."""
        return self._value
