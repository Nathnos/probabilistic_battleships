"""
Gives the number of positions of a given ship 2.2
"""

from game.board_setup import can_place, get_empty_grid


def number_of_positions(boat):
    return number_of_positions_for_grid(get_empty_grid(), boat)


def number_of_positions_for_grid(gird, boat):
    positions = 0
    for i in range(10):
        for j in range(10):
            if can_place(gird, boat, (i, j), "horizontal"):
                positions += 1
            if can_place(gird, boat, (i, j), "vertical"):
                positions += 1
    return positions
