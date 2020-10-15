"""
Main function
"""

import time

from game.board_setup import generate_random_grid, show
from combinatorial.single_boat_positions import number_of_positions
import combinatorial.boats_positions
from combinatorial.estimate_probabilities import nb_random_grid
from game.Battle import Battle


def main():
    show_positions()
    show_positions_2_boats()
    show_grids_needed_for_2(5)
    play_game(100)


def play_game(nb_of_games):
    battle = Battle("random", "random")
    total_moves = 0
    for _ in range(nb_of_games):
        _, moves = battle.launch_game()
        total_moves += moves
    print(
        "Random strat : average of {} moves (from both players).".format(
            int(total_moves / nb_of_games)
        )
    )


def show_random_grid():
    grid = generate_random_grid()
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
        "Ways to place the 'porte-avion' and 'croisseur' : ",
        combinatorial.boats_positions.number_of_positions([1, 2]),
    )  # 28 800 combinations founds, in less than a second.
    print("Took", time.time() - start_time, "seconds to execute.\n")


def show_positions_3_boats():
    start_time = time.time()
    print(
        "Ways to place the 'porte-avion', 'croisseur' and 'contre-torpilleur' : ",
        combinatorial.boats_positions.number_of_positions([1, 2, 3]),
    )  # 11 104 416 combinations founds, in almost 6 minutes.
    print("Took", time.time() - start_time, "seconds to execute.\n")


def show_grids_needed_for_2(number_of_tries):
    grids_sum = 0
    boat_list = [1, 2]
    for i in range(number_of_tries):
        grids_sum += nb_random_grid(generate_random_grid(boat_list), boat_list)
    print(
        "Average number of random grids needed to get a grid with 2 ships : ",
        grids_sum / number_of_tries,
        "\n",
    )


if __name__ == "__main__":
    main()
