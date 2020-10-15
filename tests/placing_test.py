import unittest

import numpy as np

from game.board_setup import place, eq, get_empty_grid


class PlacingTest(unittest.TestCase):
    def test_eq(self):
        grid1 = get_empty_grid()
        self.assertTrue(place(grid1, 1, (0, 0), "right"))
        self.assertTrue(place(grid1, 2, (0, 1), "bottom"))
        self.assertTrue(place(grid1, 3, (5, 6), "right"))
        self.assertTrue(place(grid1, 4, (7, 4), "right"))
        self.assertTrue(place(grid1, 5, (5, 2), "bottom"))
        grid2 = get_empty_grid()
        self.assertTrue(place(grid2, 1, (4, 0), "left"))
        self.assertTrue(place(grid2, 2, (0, 4), "top"))
        self.assertTrue(place(grid2, 3, (7, 6), "left"))
        self.assertTrue(place(grid2, 4, (9, 4), "left"))
        self.assertTrue(place(grid2, 5, (5, 3), "top"))
        self.assertTrue(eq(grid1, grid2))

    def test_neq(self):
        grid1 = get_empty_grid()
        self.assertTrue(place(grid1, 1, (0, 0), "right"))
        grid2 = get_empty_grid()
        self.assertTrue(place(grid2, 1, (4, 1), "left"))
        self.assertFalse(eq(grid1, grid2))


if __name__ == "__main__":
    unittest.main()
