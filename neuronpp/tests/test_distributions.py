import unittest
import numpy as np
from neuronpp.core.distributions import Dist


class TestSeed(unittest.TestCase):
    def test_seed(self):
        Dist.set_seed(13)
        self.assertEqual(13, np.random.get_state()[1][0])
