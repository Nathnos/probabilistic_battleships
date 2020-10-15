"""
Some functions to estimate probabilities
"""

from game.board_setup import generate_random_grid, eq


def nb_random_grid(grid, boat_list):
    """
    This function estimates the number of valid combinations.
    To be more precise, it can executed multiple times, to get an average number.
    @grid must be a possible grid with every boat from boat_list.
    @return how many random grids have been generated to match the given grid.
    """
    count = 0
    random_grid = None
    while not eq(random_grid, grid):
        random_grid = generate_random_grid(boat_list)
        count += 1
    return count
