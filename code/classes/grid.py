import csv
import itertools
import numpy as np
from .cell import Cell
from .house import House
from code.classes.mandatory import MandatoryFreeSpace
import code.algorithms.randomize as rz
from IPython import embed;

class Grid():
    def __init__(self, quantity, source_file):
        self.width = 180
        self.depth = 160
        self.quantity = quantity
        self.water = source_file
        self.all_houses = self.load_houses()
        self.all_water = self.load_water()
        self.empty_coordinates = self.load_empty_coordinates()
        self.water_coordinates = self.load_water_coordinates()
        self.house_coordinates = []
        self.man_free_coordinates = []
        self.value = 0   


    def load_grid(self):
        """
        Creates and returns a 2D array filled with cells. Each cell represents
        one square meter on the map and is associated with coordinates that
        point to its unique position in the grid.
        """
        
        all_coordinates = []
        for y in range(self.depth + 1 ):
            for x in range(self.width + 1):
                coordinates = (x, y)
                all_coordinates = np.append(grid, cell)
        
        return all_coordinates

    def load_houses(self):
        """
        Creates the specified quantity of houses with a fixed share of single
        houses (60%), bungalows (25%) and maisons (15%). Returns a dictionary
        that maps each house and its type to an ID.
        """
        
        # Determine quantity for each house type based on total quantity
        q_single = int(0.6 * self.quantity)
        q_bungalow = int(0.25 * self.quantity)
        q_maison = int(0.15 * self.quantity)

        all_houses =[]

        id_counter = 1

        # Create correct quantiy of houses
        for q_type in [q_single, q_bungalow, q_maison]:
            for h in range(int(q_type)):
                # Assign each House instance according type
                if q_type == q_single:
                    house = House("single", id_counter) 
                elif q_type == q_bungalow:
                    house = House("bungalow", id_counter)
                else:
                    house = House("maison", id_counter)

                # Add House to dictionary and adjust id_counter
                all_houses.append(house)
                id_counter = id_counter + 1

        return all_houses


    def load_water(self):
        """
        Returns a dictionary that maps the water surface(s) on a given map to
        coordinates.
        """

        # Load coordinates of water surface(s) from source file
        with open(self.map, 'r') as in_file:
            # Skip header
            next(in_file)

            water = {}

            while True:
                # For each row, create list of all items
                row = in_file.readline().rstrip("\n")
                if row == "":
                    break
                items = row.split(",")
                strip_items = [item.strip("\"") for item in items]

                # Save water coordinates in dict
                water[strip_items[0]] = {'bottom_left': (int(strip_items[1]), int(strip_items[4])),
                                    'bottom_right': (int(strip_items[3]), int(strip_items[4])),
                                    'top_left': (int(strip_items[1]), int(strip_items[2])),
                                    'top_right': (int(strip_items[3]), int(strip_items[2]))}

        return water

    def create_water(self):
        """
        Assigns cells that overlap with the water surface(s) into type 'Water'.
        """

        all_water = self.load_water()

        # For each cell that ovelaps with water, update cell type to "Water"       
        for water in all_water:
            for y in range(int(all_water[water]['top_left'][1]), int(all_water[water]['bottom_right'][1]) + 1):
                for x in range(int(all_water[water]['bottom_left'][0]), int(all_water[water]['top_right'][0]) + 1):    
                    self.cells[y][x].type = "Water"

    def define_empty_cells(self, house):
        """
        Returns a list of all empty cells on grid, where certain house would fit between 
        borders of grid.
        """

        empty_cells = []

        for row in self.cells:
            for cell in row:
                if cell.x_coordinate >= house.min_free and cell.y_coordinate >= house.min_free and cell.type == None:
                    empty_cells.append(cell)
        
        return empty_cells

    def define_object_cells(self, coordinates):
        """
        Returns a list of cells for a specific object.
        """

        object_cells = []

        for row in range(coordinates['top_left'][1], coordinates['bottom_right'][1]):
            for column in range(coordinates['top_left'][0], coordinates['bottom_right'][0]):

                current_cell = self.cells[row, column]
                object_cells.append(current_cell)

        return object_cells


    def assignment_house(self, house, cell, rotation="horizontal"):
        """ 
        Assigns house to grid, based on coordinates of cell. Returns the new 
        grid.
        """

        print("Performing random assignment of house")
        
        # Retrieve coordinates random starting cell (top-left)
        cell_x = cell.x_coordinate
        cell_y = cell.y_coordinate

        # Set house coordinates (excluding and including mandatory free space)
        house_coordinates = house.calc_house_coordinates(cell_x, cell_y, rotation)
        house_coordinates_mandatory_free_space = house.calc_mandatory_free_space_coordinates(house_coordinates)

        # embed()

        # Define all cells of possible house location (excluding and including mandatory free space)
        house_cells = self.define_object_cells(house_coordinates)
        house_cells_mandatory_free_space = self.define_object_cells(house_coordinates_mandatory_free_space)

        spot_available = True

        # For each cell, check if placing a house would be valid
        for cell in house_cells_mandatory_free_space:
                
            # House cells must be empty, mandatory free space may not overlap with a house
            if ((cell in house_cells) and cell.type != None) or cell.occupied_by_house():
                spot_available = False
   
        # If all cells of possible location are still availabe 
        if spot_available:   

            for current_cell in house_cells_mandatory_free_space:

                # Set cells occupied by house to according house type
                if current_cell in house_cells:
                    current_cell.type = house.type

                # Mark cells occupied by mandatory free space 
                elif current_cell.type != house.type:  #Of gewoon else?
                    current_cell.type = MandatoryFreeSpace(house)

            # Save coordinates
            house.coordinates = house_coordinates
            house.min_free_coordinates = house_coordinates_mandatory_free_space

            # Save cells
            house.min_free_cells = house_cells_mandatory_free_space

        else:
            raise ValueError("Location of house unavailable.")

    def calculate_extra_free_meters(self, house):
        """
        Returns how many extra free meters can be assigned to a given house.
        """

        print(f"Calculating extra free meters for: {house}")

        distance_found = False

        # i is number of extra free meters, starting from 1
        for i in itertools.count(start=1):

            list_of_cells = []

            # Save all cells, including i extra free meters in list
            for row in range((house.min_free_coordinates['top_left'][1] - i), (house.min_free_coordinates['bottom_right'][1] + i)):
                for column in range((house.min_free_coordinates['top_left'][0] - i), (house.min_free_coordinates['bottom_right'][0] + i)):
                    
                    # Check if cell is within borders of grid
                    if row >= 0 and row <= 160 and column >= 0 and column <= 180:
                        current_cell = self.cells[row, column]
                        list_of_cells.append(current_cell)
        
            # Save cells that are extra free meters in list
            for cell_1 in list_of_cells:
                if cell_1 not in house.min_free_cells:
                    house.extra_free_cells.append(cell_1)

            # Check for all cells if it is a house
            for cell_2 in house.extra_free_cells:
                if cell_2.type in ["single", "bungalow", "maison"]:

                    # Calculate distance
                    shortest_distance = i - 1
                    # Set to True, as shortest distance is found
                    distance_found = True
                    break
            
            if distance_found == True:
                break

        # Assign extra free meters to house
        house.extra_free = shortest_distance

    def calculate_worth(self):
        """
        Returns the total net worth of the map based on house type an extra free
        space.
        """

        total_networth = 0

        # Calculate worth of each house placed on the map
        for house in self.all_houses.values():
            if house.placed == True:

                # Net worth of house
                worth_house = house.price

                # Calculate extra free meters
                self.calculate_extra_free_meters(house)
                
                # Add worth of extra free space to worth of house, if any
                if house.extra_free != 0:
                    worth_house += house.extra_free * house.percentage * house.price

                # Add worth of house to total net worth of the map
                total_networth += worth_house
            # else:
            #     raise ValueError("Not all houses have been placed. Run algorithm to place houses.")

        self.value = total_networth

        return total_networth

    def create_output(self):
        """
        Creates csv-file with results from running an algorithm to place houses.
        """

        with open('data/output.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            # Create header
            fieldnames =["structure", "corner_1 (bottom_left)", "corner_2 (bottom_right)", "corner_3 (top_left)", "corner_4 (top_right)", "type"]
            writer.writerow(fieldnames)

            # Load water coordinates from correct map
            water = self.load_water()

            # Add location of water to csv file
            for ident, coordinates in water.items():
                water_list = [ident, water[ident].get('bottom_left'), water[ident].get('bottom_right'), water[ident].get('top_left'), water[ident].get('top_right'), "WATER"]
                writer.writerow(water_list)
            
            # Add location of houses to csv file
            for house in self.all_houses.values():
                house_list = f"{house.type}_{house.id}", house.coordinates['bottom_left'], house.coordinates['bottom_right'], house.coordinates['top_left'], house.coordinates['top_right'], house.type.upper()
                writer.writerow(house_list)
            
            # Add total networth of map to csv file
            networth = self.calculate_worth()
            writer.writerow(["networth", networth])