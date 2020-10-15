"""
Represent a battleship player, using a specific strategy.
"""

from game.game_tools import get_random_position, get_random_direction


class Player:
    def __init__(self, strat, number, grid):
        """
        @own_grid Tells the player where its boats are.
        Kinda useful.
        """
        self.strat_name = strat
        self.number = number
        self.played = set()
        self.searching = False
        self.last_played_successful = None
        self.first_played_successful = None
        self.grid = grid
        self.initial_grid = grid.copy()
        if strat == "random":
            self.strat = self.random_strat
            self.strat_feedback = lambda move, hit: None
        if strat == "heuristic":
            self.strat = self.heuristic_strat
            self.strat_feedback = self.heuristic_feedback

    def check_move(self, position):
        i, j = position
        if i >= 10 or i < 0 or j >= 10 or j < 0:
            return False
        return position not in self.played and not self.initial_grid[position]

    def random_strat(self):
        """
        Random move but avoids hitting its own boat and playing two times the same move.
        """
        position = get_random_position()
        while not self.check_move(position):
            position = get_random_position()
        self.played.add(position)
        return position

    def heuristic_strat(self):
        """
        Random move, until we hit something ; then we try near the last successful shot.
        """
        if not self.searching:
            return self.random_strat()
        position = tuple_sum(
            self.last_played_successful, get_random_direction(to_int=True)
        )
        count = 0
        while not self.check_move(position):
            position = tuple_sum(
                self.last_played_successful, get_random_direction(to_int=True)
            )
            count += 1
            if count == 100:  # We must have finished this way
                self.last_played_successful = self.first_played_successful
            if count == 200:  # No possible moves here !
                self.searching = False
                return self.random_strat()
        self.played.add(position)
        return position

    def feedback(self, move, hit):
        self.strat_feedback(move, hit)

    def heuristic_feedback(self, move, hit):
        if self.searching and hit == 2:
            self.searching = False
        elif hit == 1:
            if not self.searching:
                self.searching = True
                self.first_played_successful = move
            self.last_played_successful = move

    def reset(self):
        self.played = set()
        self.searching = False
        self.initial_grid = self.grid.copy()


def tuple_sum(tuple1, tuple2):
    return tuple(sum(x) for x in zip(tuple1, tuple2))
