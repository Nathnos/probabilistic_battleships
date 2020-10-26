"""
Represent a battleship player, using a specific strategy.
"""
import random
from game.game_tools import get_random_position, get_random_direction
from game.board_setup import get_empty_grid, can_place, place
from numpy import unravel_index
from game.board_setup import get_direction, get_boat_size

HITT = -1000
SHIPS = [1, 2, 3, 4, 5]


class FrequencyGrid:

    GUESSED = -1
    HIT = -4

    def __init__(self):
        self.grid = [[0 for _ in range(10)] for _ in range(10)]

    def __iter__(self):
        for row in range(10):
            for col in range(10):
                yield (row, col), self.grid[row][col]

    def set_cell(self, row, col, value):
        self.grid[row][col] = value

    def set_played_cells(self, played):
        for (x, y) in played:
            self.set_cell(x, y, self.GUESSED)

    def get_cell(self, row, col):
        return self.grid[row][col]

    def inc(self, row, col):
        self.grid[row][col] += 1

    def get_best_cell(self, played):
        best_value = -8000
        for (cell1, value) in self:
            if cell1 not in played:
                best_value = max(value, best_value)
        return random.choice(
            [cell for cell, value in self if value == best_value]
        )


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
        self.start_grid = get_empty_grid()
        self.hit = []
        if strat == "random":
            self.strat = self.random_strat
            self.strat_feedback = lambda move, hit, boat: None
        elif strat == "heuristic":
            self.strat = self.heuristic_strat
            self.strat_feedback = self.heuristic_feedback
        elif strat == "simple_probabilistic":
            self.strat = self.simple_probabilistic_strat
            self.strat_feedback = self.simple_probabilistic_feedback
        elif strat == "Monte Carlo":
            self.strat = self.monte_carlo_strat
            self.strat_feedback = self.monte_carlo_feedback

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
        self.hit = []
        self.played = set()
        self.searching = False
        self.initial_grid = self.grid.copy()
        self.remaining_enemy_boats = list(range(1, 6))
        self.searching_boats = set()

    def monte_carlo_feedback(self, move, hit, boat):
        if hit >= 1:
            self.hit.append(move)
        if hit == 2:
            self.remaining_enemy_boats.remove(boat)

    def generate_grid(self, grid, boats):
        for boat in boats:
            grid = random_placement_compatible_ret_grid(grid, boat)
        return grid

    def is_valid_cell(self, grid, row, col):
        return grid[row][col] in range(1, 6)

    def monte_carlo_strat(self):
        N = 50
        probabilities = FrequencyGrid()
        probabilities.set_played_cells(self.played)
        r = self.get_remaining_ships()
        for _ in range(N):
            grid = get_empty_grid()
            for (x, y) in self.played:
                grid[x][y] = HITT

            current_grid = self.generate_grid(grid, r)
            for row in range(10):
                for col in range(10):
                    if self.is_valid_cell(current_grid, row, col):
                        probabilities.inc(row, col)
                        for (x, y) in self.hit:
                            if x - 1 >= 0 and (x - 1, y) not in self.hit:
                                for _ in range(1):
                                    probabilities.inc(x - 1, y)
                            if x + 1 < 10 and (x + 1, y) not in self.hit:
                                for _ in range(1):
                                    probabilities.inc(x + 1, y)
                            if y - 1 >= 0 and (x, y - 1) not in self.hit:
                                for _ in range(1):
                                    probabilities.inc(x, y - 1)
                            if y + 1 < 10 and (x, y + 1) not in self.hit:
                                for _ in range(1):
                                    probabilities.inc(x, y + 1)
        best_prob = probabilities.get_best_cell(self.played)
        self.played.add(best_prob)
        return best_prob

    def get_remaining_ships(self):
        hits = len(self.hit)
        if hits:
            for _attempt in range(999):
                remaining_ships = SHIPS
                hit_ships = []
                for _count in range(len(SHIPS) - 1):
                    hit_ships.append(
                        remaining_ships.pop(
                            random.randrange(len(remaining_ships))
                        )
                    )
                    if sum([get_boat_size(hit) for hit in hit_ships]) == hits:
                        return remaining_ships
        return SHIPS


def random_placement_compatible_ret_grid(grid, boat):
    max_num = 20
    placed = False
    direction = (0, 0)
    position = (-1, -1)
    i = 1
    while i < max_num and not placed:
        i += 1
        direction = get_random_direction()
        position = get_random_position()
        placed = place_new(grid, boat, position, direction)
    return grid


def can_place_new(grid, boat, position, direction):
    x_dir, y_dir = get_direction(direction)
    boat_size = get_boat_size(boat)
    x, y = position
    for i in range(boat_size):
        x_i = x + i * x_dir
        y_i = y + i * y_dir
        if x_i >= 10 or x_i < 0 or y_i >= 10 or y_i < 0 or grid[x_i][y_i] != 0:
            return False
    return True


def place_new(grid, boat, position, direction):
    if not can_place_new(grid, boat, position, direction):
        return False
    x_dir, y_dir = get_direction(direction)
    boat_size = get_boat_size(boat)
    x, y = position
    for i in range(boat_size):
        grid[x + i * x_dir][y + i * y_dir] = boat
    return True


def exploring_position(position, radius=1):
    direction = (0, 0)
    for _ in range(radius):
        rand_dir = get_random_direction(to_int=True, positive_only=False)
        direction = tuple(
            (d + rand_dir for d, rand_dir in zip(direction, rand_dir))
        )
    return tuple(sum(x) for x in zip(position, direction))
