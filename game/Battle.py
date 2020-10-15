"""
Class to play a game
"""

import random

import numpy as np

from game.game_tools import get_random_player
from game.Player import Player


class Battle:
    def __init__(self, strat_player_1, strat_player_2):
        self.player1 = Player(strat_player_1, 1)
        self.player2 = Player(strat_player_2, 2)
        self.current_player = random.choice([self.player1, self.player2])

    def launch_game(self, verbose=0):
        victory = 0
        number_of_moves = 0
        while not victory:
            self.play_turn()
            self.switch_player()
            number_of_moves += 1
            victory = self.victory()
        if verbose:
            print(
                "Player {} wins ! {} total moves played".format(
                    victory, number_of_moves
                )
            )
        self.reset()
        return victory, number_of_moves

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def play(self, position):
        """ @return 1 when 'touché', 2 when drowned, 0 otherwise """
        self.switch_player()
        grid = self.current_player.grid
        self.switch_player()
        if grid[position]:
            boat = grid[position]
            grid[position] = 0
            if not np.isin(grid, boat).any():
                return 2  # Drowned
            return 1  # Only hit
        return 2  # Missed !

    def victory(self):
        if not self.current_player.grid.any():
            self.switch_player()  # The other player won
            return self.current_player.number
        return 0

    def play_turn(self):
        hit = self.play(self.current_player.strat())
        self.current_player.feedback(hit)

    def reset(self):
        self.player1.reset()
        self.player2.reset()
        self.current_player = random.choice([self.player1, self.player2])
