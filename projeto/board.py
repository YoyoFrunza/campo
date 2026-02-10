import random
from constants import DIFFICULTY

class Tile:
    def __init__(self):
        self.mine = False
        self.revealed = False
        self.flagged = False
        self.exploded = False
        self.adjacent = 0

class Board:
    def __init__(self, level="Normal"):
        self.level = level
        self.rows, self.cols, self.mines_count = DIFFICULTY[level]
        self.grid = [[Tile() for _ in range(self.cols)] for _ in range(self.rows)]
        self.place_mines()
        self.calculate_numbers()

    def place_mines(self):
        cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        for r, c in random.sample(cells, self.mines_count):
            self.grid[r][c].mine = True

    def calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].mine: continue
                count = 0
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.grid[nr][nc].mine:
                                count += 1
                self.grid[r][c].adjacent = count

    def reveal(self, r, c):
        tile = self.grid[r][c]
        if tile.revealed or tile.flagged: return
        tile.revealed = True
        if tile.mine:
            tile.exploded = True
            return
        if tile.adjacent == 0:
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.reveal(nr,nc)
