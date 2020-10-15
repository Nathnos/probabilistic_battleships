import unittest

import combinatorial.boats_positions
import combinatorial.single_boat_positions


class BoatPositionsTest(unittest.TestCase):
    def test_fun_eq(self):
        for boat in range(1, 6):
            self.assertEqual(
                combinatorial.boats_positions.number_of_positions([boat]),
                combinatorial.single_boat_positions.number_of_positions(boat),
            )


if __name__ == "__main__":
    unittest.main()
