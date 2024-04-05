from abc import ABC, abstractmethod
import math


class RMSE(ABC):
    """Initializes the RMSE class with an empty list."""
    def __init__(self):
        self.pairs = []

    def __add__(self, other):
        """Returns a new RMSE object with combined pairs."""
        new_obj = type(self)()
        if isinstance(other, tuple):
            new_obj.pairs = self.pairs + [other]
        else:
            new_obj.pairs = self.pairs + other.pairs
        return new_obj

    def __iadd__(self, other):
        """Adds pairs from the other RMSE object."""
        if isinstance(other, tuple):
            self.pairs.append(other)
        else:
            self.pairs.extend(other.pairs)
        return self

    def reset(self):
        """Resets the list of pairs to an empty list."""
        self.pairs = []

    @property
    def error(self):
        """Returns the Root Mean Squared Error from the current pairs."""
        n = len(self.pairs)
        if n == 0:
            return 0
        if type(self) == Euclidean:
            sum_of_squares = sum(self.distance(
                predicted, expected) for predicted, expected in self.pairs)
        elif type(self) == Taxicab:
            sum_of_squares = sum(
                self.distance(predicted, expected) ** 2
                for predicted, expected in self.pairs
            )
        mean_squared_error = sum_of_squares / n
        return math.sqrt(mean_squared_error)

    @staticmethod
    @abstractmethod
    def distance(predicted, expected):
        pass


class Euclidean(RMSE):
    @staticmethod
    def distance(predicted, expected):
        """Return Euclidean distance between predicted and expected values."""
        return sum((p - e) ** 2 for p, e in zip(predicted, expected))


class Taxicab(RMSE):
    @staticmethod
    def distance(predicted, expected):
        """Return Taxicab distance between predicted and expected values."""
        return sum(abs(p - e) for p, e in zip(predicted, expected))
