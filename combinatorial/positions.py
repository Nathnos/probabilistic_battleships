"""
Gives the number of positions of a given ship
"""

from game.board_setup import can_place, get_empty_grid


def number_of_positions(boat):
    empty_grid = get_empty_grid()
    positions = 0
    for i in range(10):
        for j in range(10):
            if can_place(empty_grid, boat, (i, j), "horizontal"):
                positions += 1
            if can_place(empty_grid, boat, (i, j), "vertical"):
                positions += 1
    return positions
