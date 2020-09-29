"""
Main function
"""

from game.board_setup import generate_grid, show


def main():
    grid = generate_grid()
    show(grid)


if __name__ == "__main__":
    main()
