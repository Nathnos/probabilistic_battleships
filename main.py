"""
Main function
"""

from game.board_setup import generate_grid, show
from combinatorial.single_boat_positions import number_of_positions
import combinatorial.boats_positions
import time


def main():
    show_positions()
    show_positions_2_boats()


def show_random_grid():
    grid = generate_grid()
    show(grid)


def show_positions():
    print("Porte-avion : ", number_of_positions(1), "positions")
    print("Croiseur : ", number_of_positions(2), "positions")
    print("Contre-torpilleur : ", number_of_positions(3), "positions")
    print("Sous-marin : ", number_of_positions(4), "positions")
    print("Torpilleur : ", number_of_positions(5), "positions\n")


def show_positions_2_boats():
    start_time = time.time()
    print(
        "Façons de placer le porte-avion et croisseur : ",
        combinatorial.boats_positions.number_of_positions([1, 2]),
    )  # 28 800 combinaisons trouvées, en moins d'une seconde
    print("Took", time.time() - start_time, "seconds to execute.")


def show_positions_3_boats():
    start_time = time.time()
    print(
        "Façons de placer le porte-avion, croisseur et torpilleur : ",
        combinatorial.boats_positions.number_of_positions([1, 2, 3]),
    )  # 11 104 416 combinaisons trouvées, en presque 6 minutes
    print("Took", time.time() - start_time, "seconds to execute.")


if __name__ == "__main__":
    main()
