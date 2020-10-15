"""
Represent a battleship player, using a specific strategy.
"""

from game.game_tools import get_random_position


class Player:
    def __init__(self, strat):
        self.strat_name = strat
        if strat == "random":
            self.strat = self.random_strat
            self.played = set()

    def random_strat(self):
        position = get_random_position()
        while position in self.played:
            position = get_random_position()
        self.played.add(position)
        return position

    def reset(self):
        self.played = set()
