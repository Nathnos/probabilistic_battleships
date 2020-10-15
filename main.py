"""
Main function
"""

from game.board_setup import generate_grid, show
from combinatorial.positions import number_of_positions


def main():
    show_positions()


def show_random_grid():
    grid = generate_grid()
    show(grid)


def show_positions():
    print("Porte-avion : ", number_of_positions(1), "positions")
    print("Croiseur : ", number_of_positions(2), "positions")
    print("Contre-torpilleur : ", number_of_positions(3), "positions")
    print("Sous-marin : ", number_of_positions(4), "positions")
    print("Torpilleur : ", number_of_positions(5), "positions")


if __name__ == "__main__":
    main()
