"""
Gives the number of positions of a list of ships.
Done recursively.
"""

from combinatorial.single_boat_positions import number_of_positions_for_grid
from game.board_setup import get_empty_grid, can_place, place
import gc


def number_of_positions(boat_list):
    positions = 0
    for boat in boat_list:
        remaining_boat_list = boat_list.copy()
        remaining_boat_list.remove(boat)
        positions += rec_number_of_positions(
            get_empty_grid(), boat, remaining_boat_list
        )
    return positions


"""
We consider that placing boat 1 then boat 2 is not the same as placing boat 2 then boat 1, even thought it may 
result in the same board state.
Otherwise, force brute is impossible, as it demands to keep in memory all grids already created.
"""


def rec_number_of_positions(grid, boat, remaining_boat_list):
    if len(remaining_boat_list) == 0:
        return number_of_positions_for_grid(grid, boat)
    positions_count = 0
    for i in range(10):
        for j in range(10):
            if can_place(grid, boat, (i, j), "horizontal"):
                new_grid = grid.copy()
                place(new_grid, boat, (i, j), "horizontal")
                for remaining_boat in remaining_boat_list:
                    new_remaining_boat_list = remaining_boat_list.copy()
                    new_remaining_boat_list.remove(remaining_boat)
                    positions_count += rec_number_of_positions(
                        new_grid.copy(), remaining_boat, new_remaining_boat_list
                    )
                    gc.collect()
            if can_place(grid, boat, (i, j), "vertical"):
                new_grid = grid.copy()
                place(new_grid, boat, (i, j), "vertical")
                for remaining_boat in remaining_boat_list:
                    new_remaining_boat_list = remaining_boat_list.copy()
                    new_remaining_boat_list.remove(remaining_boat)
                    positions_count += rec_number_of_positions(
                        new_grid.copy(), remaining_boat, new_remaining_boat_list
                    )
                    gc.collect()
    return positions_count
