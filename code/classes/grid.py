import csv
import numpy as np
from .cell import Cell

class Grid():
    def __init__(self):
        self.width = 18
        self.depth = 16
        self.cells = self.load_grid(self.width, self.depth)

    def load_grid(self, width, depth):
        grid = np.array([])
        for i in range(width + 1):
            x = width - i 
            for y in range(depth + 1):
                cell = Cell(x, y)
                grid = np.append(grid, cell)
        
        grid = np.resize(grid,(width, depth))
        return grid 

    # def load_water(self, source_file):
    #     with open(source_file, 'r') as in_file:
    #         reader = csv.DictReader(in_file)

    #         water = {}
    #         # skip the header
    #         next(reader, None)
    #         for row in reader:
    #             water[row[0]] = {'bottom_left_xy': row[1], 'top_right_xy': row[2]}

    #     return water
    
    def draw(self):
        for i in range(self.width + 1):
            x = self.width - i 
            for y in range(self.depth + 1):
                print("hi", end="")
            print("")
        

