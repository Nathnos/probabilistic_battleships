"""
Represent a battleship player, using a specific strategy.
"""

from game.board_setup import generate_random_grid
from game.game_tools import get_random_position


class Player:
    def __init__(self, strat, number):
        """
        @own_grid Tells the player where its boats are.
        Kinda useful.
        """
        self.strat_name = strat
        self.number = number
        self.played = set()
        self.last_played = None
        self.last_played_successful = False
        self.grid = generate_random_grid()
        if strat == "random":
            self.strat = self.random_strat

    def random_strat(self):
        """
        Random move but avoids hitting its own boat and playing two times the same move.
        """
        position = get_random_position()
        while position in self.played and not self.grid[position]:
            position = get_random_position()
        self.played.add(position)
        return position

    def heuristic(self):
        pass

    def feedback(self, hit):
        self.last_played_successful = hit

    def reset(self):
        self.played = set()
        self.grid = generate_random_grid()
