import csv
import numpy as np
from .cell import Cell
from .house import House

class Grid():
    def __init__(self, quantity, source_file):
        self.width = 180
        self.depth = 160
        self.cells = self.load_grid(self.width, self.depth)
        self.all_houses = self.load_houses(quantity)
        self.all_water = self.load_water(source_file)
        #self.create_water()
        self.map = source_file

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
        """
        Reads a csv file into a dictionary. Returns a dictionary of water 
        coordinates.
        """

        with open(source_file, 'r') as in_file:

            # Create dict to save water coordinates
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

                # Save water coordinates in dict
                water[row[0]] = {'bottom_left_x': row[1].strip("\""), 'bottom_left_y': row[2].strip("\""),'top_right_x': row[3].strip("\""), 'top_right_y': row[4].strip("\"")}

        return water

    def create_water(self):
        """
        Transforms Cell objects into the 'water' type.
        """

        # Iterate over all water objects in dict
        for water in self.all_water:
            # Define coordinates of water objects
            for x in range(int(self.all_water[water]['bottom_left_x']), int(self.all_water[water]['top_right_x']) + 1):
                for y in range(int(self.all_water[water]['bottom_left_y']), int([water]['top_right_y']) + 1):

                    # Transform cells into 'Water' type
                    self.cells[y][x].type = "Water"
    
    # def calculate_worth(self):
    #     """
    #     Calculates worth of all House objects on grid. Returns the total net 
    #     worth.
    #     """

    #     total_net_worth = 0

    #     for house in #ALL_HOUSES_ON_GRID
    #         net_worth_house = house.price
            
    #         if house.extra_free_cells != 0:
    #             net_worth_house += house.extra_free_cells * house.percentage * house.price
            
    #         total_net_worth += net_worth_house
        
    #     return total_net_worth



    def create_output(self):
        # how to create csv file from https://www.programiz.com/python-programming/writing-csv-files
        with open('data/output.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            # create header
            fieldnames =["structure", "corner_1", "corner_2", "corner_3", "corner_4", "type"]
            writer.writerow(fieldnames)

            # load coordinates for water from correct map
            water = self.load_water(self.map)

            # add location of water to csv file
            water_list = []
            for ident, coordinates in water.items():
                water_list = [ident, water[ident].get('bottom_left_x'), water[ident].get('bottom_left_y'), water[ident].get('top_right_x'), water[ident].get('top_right_y'), "WATER"]
                writer.writerow(water_list)
            
            # todo: add location of houses to csv file
            
            # add optimalization function to csv file
            optimalization = "[insert optimalization function]"
            writer.writerow(["networth", optimalization])
