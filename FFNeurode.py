"""Implementing FFNeurode Class"""
from __future__ import annotations
from Neurode import Neurode
import math


class FFNeurode(Neurode):

    def __init__(self):
        super().__init__()

    @staticmethod
    def _sigmoid(value: float):
        """Return the result of the sigmoid function."""
        return 1 / (1 + math.exp(-value))

    def _calculate_value(self):
        """Calculate the weighted sum of upstream nodes' values and apply the sigmoid function."""
        weighted_sum = sum(node.value * self._weights[node] for node in self._neighbors[Neurode.Side.UPSTREAM])
        self._value = FFNeurode._sigmoid(weighted_sum)

    def _fire_downstream(self):
        """Notify downstream neighbors that data is ready from this node."""
        for node in self._neighbors[Neurode.Side.DOWNSTREAM]:
            node.data_ready_upstream(self)

    def data_ready_upstream(self, node: Neurode):
        """Upstream neurodes call this method when they have data ready."""
        if self._check_in(node, Neurode.Side.UPSTREAM):
            self._calculate_value()
            self._fire_downstream()

    def set_input(self, input_value: float):
        """This method is used by the client to directly set the value of an input layer neurode."""
        self._value = input_value
        self._fire_downstream()
