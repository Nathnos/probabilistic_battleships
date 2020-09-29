"""
Main game functions
"""

import numpy as np

from game.game_tools import (
    get_direction,
    get_boat_size,
    get_random_direction,
    get_random_position,
)


def can_place(grid, boat, position, direction):
    """
    grid : numpy array
    boats : represented by an integer
    position : tuple (x, y)
    direction : left, right, top or bottom
    """
    x_dir, y_dir = get_direction(direction)
    boat_size = get_boat_size(boat)
    x, y = position
    for i in range(boat_size):
        x_i = x + i * x_dir
        y_i = y + i * y_dir
        if x_i >= 10 or x_i < 0 or y_i >= 10 or y_i < 0 or grid[y_i, x_i]:
            return False
    return True


def place(grid, boat, position, direction):
    if can_place(grid, boat, position, direction):
        x_dir, y_dir = get_direction(direction)
        boat_size = get_boat_size(boat)
        x, y = position
        for i in range(boat_size):
            grid[y + i * y_dir, x + i * x_dir] = boat
        return True
    else:  # Can't place
        return False


def generate_grid():
    grid = np.zeros((10, 10), dtype=np.uint8)
    for boat in range(1, 6):  # For each boat
        random_placement(grid, boat)
    return grid


def random_placement(grid, boat):
    placed = False
    while not placed:
        direction = get_random_direction()
        position = get_random_position()
        placed = place(grid, boat, position, direction)


def show(grid):
    print(grid)


def eq(grid1, grid2):
    return (grid1 == grid2).all()