import unittest

from game.board_setup import place, eq, get_empty_grid


class PlacingTest(unittest.TestCase):
    def test_eq(self):
        grid1 = get_empty_grid()
        self.assertTrue(place(grid1, 1, (0, 0), "right", 1))
        self.assertTrue(place(grid1, 2, (0, 1), "bottom", 1))
        self.assertTrue(place(grid1, 3, (5, 6), "right", 1))
        self.assertTrue(place(grid1, 4, (7, 4), "right", 1))
        self.assertTrue(place(grid1, 5, (5, 2), "bottom", 1))
        grid2 = get_empty_grid()
        self.assertTrue(place(grid2, 1, (4, 0), "left", 1))
        self.assertTrue(place(grid2, 2, (0, 4), "top", 1))
        self.assertTrue(place(grid2, 3, (7, 6), "left", 1))
        self.assertTrue(place(grid2, 4, (9, 4), "left", 1))
        self.assertTrue(place(grid2, 5, (5, 3), "top", 1))
        self.assertTrue(eq(grid1, grid2))

    def test_neq(self):
        grid1 = get_empty_grid()
        self.assertTrue(place(grid1, 1, (0, 0), "right", 1))
        grid2 = get_empty_grid()
        self.assertTrue(place(grid2, 1, (4, 1), "left", 1))
        self.assertFalse(eq(grid1, grid2))


if __name__ == "__main__":
    unittest.main()
