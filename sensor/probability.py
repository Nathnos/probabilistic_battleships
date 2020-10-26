from math import sqrt
import random
import numpy as np, numpy.random


class ProbabilityGrid:
    def __init__(self, N, set_submarine=False, **kwargs):
        self.N = int(sqrt(N))
        self.grid = [[0 for _ in range(self.N)] for _ in range(self.N)]
        self.visited = [[False for _ in range(self.N)] for _ in range(self.N)]
        if not set_submarine:
            self.x = random.randrange(self.N)
            self.y = random.randrange(self.N)
        else:
            self.x = kwargs["x"]
            self.y = kwargs["y"]
        self.visited_cells = 0

    def __iter__(self):
        for row in range(self.N):
            for col in range(self.N):
                yield (row, col), self.grid[row][col]

    def get_best_probability(self):
        best_value = max([value for (cell1, value) in self])
        return random.choice(
            [cell for cell, value in self if value == best_value]
        )

    def distributeProbability(self, probabilityFunction, initial=False):
        if initial:
            self.probability_function = probabilityFunction
        probabilities = probabilityFunction()
        cnt = 0
        for i in range(self.N):
            for j in range(self.N):
                if not self.visited[i][j]:
                    self.grid[i][j] = probabilities[cnt]
                    cnt += 1

    def check_if_submarine(self, x, y):
        def is_submarine(x, y):
            return self.x == x and self.y == y

        self.grid[x][y] = 0
        self.visited[x][y] = True
        self.visited_cells += 1
        return is_submarine(x, y)

    def update_probability_uniform(self):
        return [1 / (self.N ** 2 - self.visited_cells)] * (
            self.N ** 2 - self.visited_cells
        )

    def update_probability_random(self):
        probabilities = np.random.random(self.N ** 2 - self.visited_cells)
        probabilities /= probabilities.sum()
        return probabilities

    def update_probability_favoring_margins(self):
        probabilities = np.random.random(self.N ** 2 - self.visited_cells)
        probabilities /= probabilities.sum()
        probabilities = sorted(probabilities, reverse=True)
        mat = np.arange(self.N ** 2).reshape(self.N, self.N)
        mat = spiral_ccw(mat)
        spiral_probabilities = []
        i = 0
        for it in mat:
            x = it // self.N
            y = it % self.N
            if self.visited[x][y] == False:
                spiral_probabilities.append((it, probabilities[i]))
                i += 1
        spiral_probabilities.sort(key=lambda x: x[0])
        return [x[1] for x in spiral_probabilities]

    def update_probability_favoring_center(self):
        probabilities = np.random.random(self.N ** 2 - self.visited_cells)
        probabilities /= probabilities.sum()
        probabilities = sorted(probabilities)
        mat = np.arange(self.N ** 2).reshape(self.N, self.N)
        mat = spiral_ccw(mat)
        spiral_probabilities = []
        i = 0
        for it in mat:
            x = it // self.N
            y = it % self.N
            if self.visited[x][y] == False:
                spiral_probabilities.append((it, probabilities[i]))
                i += 1
        spiral_probabilities.sort(key=lambda x: x[0])
        return [x[1] for x in spiral_probabilities]

    def find_submarine(self):
        i = 0
        (x, y) = self.get_best_probability()
        while self.check_if_submarine(x, y) == False:
            self.distributeProbability(self.probability_function)
            (x, y) = self.get_best_probability()
            i += 1
        print(f"found after {i} iterations")
        print((x, y))


def spiral_ccw(A):
    A = np.array(A)
    out = []
    while A.size:
        out.append(A[0][::-1])
        A = A[1:][::-1].T
    return np.concatenate(out)


def create_random_point(N):
    x = random.randrange(N)
    y = random.randrange(N)
    return (x, y)


def test_random_probability_grid(N, set_point=False, **kwargs):
    pg = ProbabilityGrid(N, set_submarine=set_point, **kwargs)
    pg.distributeProbability(pg.update_probability_random, initial=True)
    pg.find_submarine()


def test_uniform_probability_grid(N, set_point=False, **kwargs):
    pg = ProbabilityGrid(N, set_submarine=set_point, **kwargs)
    pg.distributeProbability(pg.update_probability_uniform, initial=True)
    pg.find_submarine()


def test_margins_probability_grid(N, set_point=False, **kwargs):
    pg = ProbabilityGrid(N, set_submarine=set_point, **kwargs)
    pg.distributeProbability(
        pg.update_probability_favoring_margins, initial=True
    )
    pg.find_submarine()


def test_center_probability_grid(N, set_point=False, **kwargs):
    pg = ProbabilityGrid(N, set_submarine=set_point, **kwargs)
    pg.distributeProbability(
        pg.update_probability_favoring_center, initial=True
    )
    pg.find_submarine()


if __name__ == "__main__":
    N = 10000
    (x, y) = create_random_point(int(sqrt(N)))
    point = {"x": x, "y": y}
    test_uniform_probability_grid(N, True, **point)
    test_random_probability_grid(N, True, **point)
    test_margins_probability_grid(N, True, **point)
    test_center_probability_grid(N, True, **point)
