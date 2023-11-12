from pprint import pprint
from random import random
import matplotlib.pyplot as plt


class CityGrid:
    def __init__(self, n, m, coverage=0.3):
        self.n = n
        self.coverage = coverage
        self.m = m
        self.grid = [[0 if random() > self.coverage else 1
                      for j in range(self.m)] for _ in range(self.n)]

    def _set_to_grid(self, x, y, num):
        if self.grid[y][x] != 1:
            self.grid[y][x] = num

    def set_tower(self, x, y, tower_range):
        for i in range(max(0, y - tower_range),
                       min(self.n, y + tower_range + 1)):
            for j in range(max(0, x - tower_range),
                           min(self.m, x + tower_range + 1)):
                if self.grid[i][j] == 0:
                    self.grid[i][j] = 2
        self.grid[y][x] = 3

    def optimize_tower(self, tower_range):
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                if (i % (tower_range + 1) == 0 and j % (tower_range + 1) == 0 and
                        self.grid[i - 1][j - 1] == 0):
                    self.set_tower(j - 1, i - 1, tower_range)
        self.non_optimize_tower(tower_range)

    def non_optimize_tower(self, tower_range):
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                if self.grid[i - 1][j - 1] == 0:
                    self.set_tower(j - 1, i - 1, tower_range)

    def draw_city(self):
        fig, ax = plt.subplots()

        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == 1:
                    ax.add_patch(plt.Rectangle((j, self.n - i - 1), 1, 1, color="gray"))
                if self.grid[i][j] == 3:
                    ax.add_patch(plt.Rectangle((j, self.n - i - 1), 1, 1, color="red"))
                if self.grid[i][j] == 2:
                    ax.add_patch(plt.Rectangle((j, self.n - i - 1), 1, 1, color="blue"))


        ax.set_aspect("equal")
        ax.set_xlim(0, self.m)
        ax.set_ylim(0, self.n)
        plt.show()


class TowerGraph():
    def __init__(self, city_grid, tower_range):
        self.city_grid = city_grid
        self.tower_range = tower_range

    def get_min_path(self, x1,y1,x2,y2):
        Q = [[(x1, y1), 0]]
        seen = []
        ways = []
        while Q:
            v = Q.pop(0)
            dist = v[1]
            v = v[0]
            seen.append(v)
            for i in range(max(0, v[1] - self.tower_range),
                           min(self.city_grid.n, v[1] + self.tower_range + 1)):
                for j in range(max(0, v[0] - self.tower_range),
                               min(self.city_grid.m, v[0] + self.tower_range + 1)):
                    if self.city_grid.grid[i][j] == 3 and (j,i) not in seen:
                        Q.append([(j,i), dist+1])
                        if j == x2 and i == y2:
                            ways.append(dist+1)
        return min(ways)


c = CityGrid(12, 15, 0.3)

c.optimize_tower(2)
c.draw_city()
pprint(c.grid)


x1 = int(input())
y1 = int(input())
x2 = int(input())
y2 = int(input())

tg = TowerGraph(c, 3)
print(tg.get_min_path(x1,y1,x2,y2))
