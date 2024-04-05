from __future__ import annotations
from Neurode import Neurode


class BPNeurode(Neurode):
    def __init__(self):
        """Initializes the BPNeurode with a default delta of 0."""
        super().__init__()
        self._delta = 0

    @staticmethod
    def _sigmoid_derivative(value: float):
        """Calculates the derivative of the sigmoid function."""
        return value * (1 - value)

    def _calculate_delta(self, expected_value: float = None):
        """Calculates the delta for output and hidden layer neurodes."""
        if expected_value is not None:
            self._delta = (
                    (expected_value - self.value) *
                    self._sigmoid_derivative(self.value)
            )
        else:
            weighted_deltas_sum = sum(
                node.delta * node.get_weight(self)
                for node in self._neighbors[self.Side.DOWNSTREAM]
            )
            self._delta = (weighted_deltas_sum *
                           self._sigmoid_derivative(self.value)
                           )

    def data_ready_downstream(self, node: Neurode):
        """Notifies the neurode that data from a downstream node is ready"""
        if self._check_in(node, Neurode.Side.DOWNSTREAM):
            self._calculate_delta()
            self._fire_upstream()
            self._update_weights()

    def set_expected(self, expected_value: float):
        """Sets the expected value for this neurode."""
        self._calculate_delta(expected_value)
        self._fire_upstream()

    def adjust_weights(self, node: Neurode, adjustment: float):
        """Adjusts the weight of the connection."""
        self._weights[node] += adjustment

    def _update_weights(self):
        """Updates the weights of connections to downstream nodes."""
        for node in self._neighbors[Neurode.Side.DOWNSTREAM]:
            adjustment = Neurode._learning_rate * node.delta * self.value
            node.adjust_weights(self, adjustment)

    def _fire_upstream(self):
        """Notifies upstream neurodes that the neurode has data ready."""
        for node in self._neighbors[Neurode.Side.UPSTREAM]:
            node.data_ready_downstream(self)

    @property
    def delta(self):
        """Returns the current delta value of the neurode."""
        return self._delta
