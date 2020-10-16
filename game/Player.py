"""
Represent a battleship player, using a specific strategy.
"""

from game.game_tools import get_random_position, get_random_direction
from game.board_setup import get_empty_grid, can_place, place
from numpy import unravel_index


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
        self.searching_boats = set()
        self.remaining_enemy_boats = list(range(1, 6))
        if strat == "random":
            self.strat = self.random_strat
            self.strat_feedback = lambda move, hit, boat: None
        elif strat == "heuristic":
            self.strat = self.heuristic_strat
            self.strat_feedback = self.heuristic_feedback
        elif strat == "simple_probabilistic":
            self.strat = self.simple_probabilistic_strat
            self.strat_feedback = self.simple_probabilistic_feedback

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
        position = exploring_position(self.last_played_successful)
        count = 0
        radius = 1
        while not self.check_move(position):
            position = exploring_position(self.last_played_successful, radius)
            count += 1
            if count == 100:  # We must have finished this way
                self.last_played_successful = self.first_played_successful
            if count == 200:  # No possible moves here !
                count = 0
                radius += 1
        self.played.add(position)
        return position

    def simple_probabilistic_strat(self):
        if self.searching:
            return self.heuristic_strat()
        prob_grid = get_empty_grid()
        for boat in self.remaining_enemy_boats:
            played_grid = get_empty_grid()
            for position in self.played:
                played_grid[position] = 1
            for i in range(10):
                for j in range(10):
                    if not self.grid[i, j]:
                        if can_place(played_grid, boat, (i, j), "horizontal"):
                            place(
                                prob_grid,
                                boat,
                                (i, j),
                                "horizontal",
                                append=True,
                            )
                        if can_place(played_grid, boat, (i, j), "vertical"):
                            place(
                                prob_grid, boat, (i, j), "vertical", append=True
                            )
        position = unravel_index(prob_grid.argmax(), prob_grid.shape)
        self.played.add(position)
        return position

    def feedback(self, move, hit, boat):
        self.strat_feedback(move, hit, boat)

    def heuristic_feedback(self, move, hit, boat):
        if hit == 2:
            self.searching_boats.remove(boat)
            if len(self.searching_boats) == 0:
                self.searching = False
        elif hit == 1:
            if not self.searching:
                self.searching = True
                self.first_played_successful = move
            self.last_played_successful = move
            self.searching_boats.add(boat)

    def simple_probabilistic_feedback(self, move, hit, boat):
        self.heuristic_feedback(move, hit, boat)
        if hit == 2:
            self.remaining_enemy_boats.remove(boat)

    def reset(self):
        self.played = set()
        self.searching = False
        self.initial_grid = self.grid.copy()
        self.remaining_enemy_boats = list(range(1, 6))
        self.searching_boats = set()


def exploring_position(position, radius=1):
    direction = (0, 0)
    for _ in range(radius):
        rand_dir = get_random_direction(to_int=True, positive_only=False)
        direction = tuple(
            (d + rand_dir for d, rand_dir in zip(direction, rand_dir))
        )
    return tuple(sum(x) for x in zip(position, direction))
