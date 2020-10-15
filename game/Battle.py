"""
Class to play a game
"""

import numpy as np

from game.board_setup import generate_random_grid_2_players
from game.game_tools import get_random_player
from game.Player import Player


class Battle:
    def __init__(self, strat_player_1, strat_player_2):
        self.grid = generate_random_grid_2_players()
        self.player1 = Player(strat_player_1)
        self.player2 = Player(strat_player_2)
        self.current_player = get_random_player()

    def launch_game(self, verbose=0):
        victory = 0
        number_of_moves = 0
        while not victory:
            self.play_turn(player=self.current_player)
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
        return self.victory(), number_of_moves

    def switch_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    def play(self, position):
        self.grid[position] = 0

    def victory(self):
        if not np.isin(self.grid, 1).any():
            return 2
        if not np.isin(self.grid, 2).any():
            return 1
        return 0

    def play_turn(self, player):
        if player == 1:
            self.play(self.player1.strat())
        elif player == 2:
            self.play(self.player2.strat())

    def reset(self):
        self.grid = generate_random_grid_2_players()
        self.player1.reset()
        self.player2.reset()
        self.current_player = get_random_player()
