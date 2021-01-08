import numpy as np
from .cell import Cell

class Grid():
    def __init__(self):
        self.width = 18
        self.depth = 16
        self.cells = self.load_grid(self.width, self.depth)

    def load_grid(self, width, depth):
        grid = np.array([])
        for x in range(width):
            for y in range(depth):
                cell = Cell(x, y)
                grid = np.append(grid, cell)
        
        grid = np.resize(grid,(width, depth))
        return grid 