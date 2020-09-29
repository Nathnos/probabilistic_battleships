import unittest

import numpy as np

from game import place, eq


class PlacingTest(unittest.TestCase):
    def test_eq(self):
        grid1 = np.zeros((10, 10), dtype=np.uint8)
        place(grid1, 1, (0, 0), "right")
        place(grid1, 2, (0, 1), "bottom")
        place(grid1, 3, (5, 6), "right")
        place(grid1, 4, (7, 4), "right")
        place(grid1, 5, (0, 2), "bottom")
        grid2 = np.zeros((10, 10), dtype=np.uint8)
        place(grid2, 1, (4, 0), "left")
        place(grid2, 2, (0, 4), "top")
        place(grid2, 3, (7, 6), "left")
        place(grid2, 4, (9, 4), "left")
        place(grid2, 5, (0, 3), "top")
        self.assertTrue(eq(grid1, grid2), True)


if __name__ == "__main__":
    unittest.main()
