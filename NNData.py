"""Implementing the NNData class."""
from collections import deque
from enum import Enum
import numpy as np
import random


class Set(Enum):
    """Define Set enum class with TRAIN and TEST."""

    TRAIN = 1
    TEST = 2


class Order(Enum):
    """Define Order enum class with SHUFFLE and STATIC."""

    SHUFFLE = 1
    STATIC = 2


class NNData:
    """Define NNData class."""

    @staticmethod
    def percentage_limiter(percentage):
        """Define percentage limiter."""
        if percentage < 0:
            return 0
        elif percentage > 1:
            return 1
        else:
            return percentage

    def __init__(self, features=None, labels=None, train_factor=0.9):
        """Initialize NNData class."""
        self._labels = None
        self._features = None
        self._train_factor = NNData.percentage_limiter(train_factor)
        self._test_indices = []
        self._train_indices = []
        self._test_pool = deque()
        self._train_pool = deque()
        self.load_data(features, labels)

    def load_data(self, features=None, labels=None):
        """Load data method."""
        if features is None or labels is None:
            """Check if features or labels are none."""
            self._features = None
            self._labels = None
            self.split_set()
            return

        if len(features) != len(labels):
            """Check if length of features and labels are not equal."""
            self._features = None
            self._labels = None
            self.split_set()
            raise ValueError("Features and labels must have the same length.")

        try:
            """Try converting features & labels into numpy arrays."""
            self._features = np.array(features, dtype=float)
            self._labels = np.array(labels, dtype=float)
        except ValueError:
            """If conversion fails..."""
            self._features = None
            self._labels = None
            self.split_set()
            raise ValueError("Failed to convert feat./labels to numpy arrays.")
        self.split_set()

    def split_set(self, new_train_factor=None):
        """Split data set for training and testing."""
        if new_train_factor is not None:
            """Updating train factor"""
            self._train_factor = NNData.percentage_limiter(new_train_factor)

        if self._features is None:
            """Check if features are loaded."""
            self._train_indices = []
            self._test_indices = []
            return

        """Calculate number of examples."""
        num_examples = len(self._features)
        num_train_examples = int(num_examples * self._train_factor)

        """Create indices."""
        all_indices = list(range(num_examples))
        random.shuffle(all_indices)

        """Assign first portion to testing and the rest to training."""
        self._train_indices = all_indices[:num_train_examples]
        self._test_indices = all_indices[num_train_examples:]

    def use_training_data_for_testing(self):
        self._test_indices = self._train_indices.copy()
        self._test_pool = self._train_pool.copy()

    def prime_data(self, target_set=None, order=None):
        """Prepare data."""
        if target_set is None:
            """Load both train and test pools if target_set is None."""
            self._train_pool = deque(self._train_indices)
            self._test_pool = deque(self._test_indices)

            if order == Order.SHUFFLE:
                """Shuffle the pools if order is SHUFFLE."""
                random.shuffle(self._train_pool)
                random.shuffle(self._test_pool)

        elif target_set == Set.TRAIN:
            """Load only the train pool if target_set is TRAIN."""
            self._train_pool = deque(self._train_indices)
            """Shuffle the train pool if order is SHUFFLE."""

            if order == Order.SHUFFLE:
                random.shuffle(self._train_pool)

        elif target_set == Set.TEST:
            """Load only the test pool if target_set = TEST."""
            self._test_pool = deque(self._test_indices)
            """Shuffle the test pool if order is SHUFFLE."""

            if order == Order.SHUFFLE:
                random.shuffle(self._test_pool)

    def get_one_item(self, target_set=None):
        """Retrieve 1 item and return as a tuple."""
        if target_set is None or target_set == Set.TRAIN:
            if self._train_pool:
                a = self._train_pool.popleft()
                return self._features[a], self._labels[a]
        elif target_set == Set.TEST:
            if self._test_pool:
                a = self._test_pool.popleft()
                return self._features[a], self._labels[a]
        return None

    def pool_is_empty(self, target_set=None):
        """Determine whether data pool is empty."""
        if target_set is None or target_set == Set.TRAIN:
            return not self._train_pool
        elif target_set == Set.TEST:
            return not self._test_pool

    def number_of_samples(self, target_set=None):
        """Return number of samples."""
        if target_set == Set.TRAIN:
            return len(self._train_indices)
        elif target_set == Set.TEST:
            return len(self._test_indices)
        else:
            return len(self._train_indices) + len(self._test_indices)
