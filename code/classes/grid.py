import csv
import numpy as np
from .cell import Cell
from .house import House

class Grid():
    def __init__(self, quantity):
        self.width = 180
        self.depth = 160
        self.cells = self.load_grid(self.width, self.depth)
        self.all_houses = self.load_houses(quantity)

    def load_grid(self, width, depth):
        """
        Creates a 2D array filled with Cells with according coordinates
        """

        grid = np.array([])
        for y in range(width + 1 ):
            for x in range(depth + 1):
                cell = Cell(x, y)
                grid = np.append(grid, cell)
        
        grid = np.resize(grid,(width + 1, depth + 1))
        return grid 

    def print_grid(self):
        print(f"{self.cells}")

    def load_houses(self, quantity):
        """
        Creates according quantity of House instances with specific type 
        and id and returns dictionary with all houses.
        """

        # Determine according quantities for different types
        q_single = int(0.6 * quantity)
        q_bungalow = int(0.25 * quantity)
        q_maison = int(0.15 * quantity)

        # Save houses in dict
        all_houses = {}

        # Create specific quantiy of House instances with according type
        id_counter = 1
        for quantity in [q_single, q_bungalow, q_maison]:
            for i in range(int(quantity)):

                # Check for type
                if quantity == q_single:
                    house = House("single", id_counter) 
                elif quantity == q_bungalow:
                    house = House("bungalow", id_counter)
                else:
                    house = House("maison", id_counter)

                # Add House to dictionary and adjust id_counter
                all_houses[id_counter] = house
                id_counter = id_counter + 1

        return all_houses

    def load_water(self, source_file):
        with open(source_file, 'r') as in_file:

            # Create dict to save water
            water = {}
            
            # Skip the header row
            next(in_file)

            while True:
                # Read through file row by row (till blank row)
                row = in_file.readline().rstrip("\n")
                if row == "":
                    break
                # Create a list of all items on row
                row = row.split(",")

                # Create a dictionary to store all waters
                water[row[0]] = {'bottom_left_x': row[1].strip("\""), 'bottom_left_y': row[2].strip("\""),'top_right_x': row[3].strip("\""), 'top_right_y': row[4].strip("\"")}
                # water[row[0]] = {row[1], row[2], row[3], row[4]}

        return water

    # for x in range(x_left_bottom, x_right_bottom):
    #     for y in range(y_left_bottom, y_right_bottom):
    #         cell(x, j).type =  water