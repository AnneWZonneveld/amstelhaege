import csv
import itertools
import numpy as np
from .cell import Cell
from .house import House
from .water import Water
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
        self.all_empty_coordinates = self.load_empty_coordinates()
        self.all_water_coordinates = self.define_water_coordinates()
        self.all_house_coordinates = []
        self.all_man_free_coordinates = []
        self.value = 0   

    def load_empty_coordinates(self):
        """
        Returns a list with all coordinates that make up the map
        of Amstelhaege.
        """
        
        empty_coordinates = []

        for x in range(self.width + 1 ):
            for y in range(self.depth + 1):
                coordinate = (x,y)
                empty_coordinates.append(coordinate)

        return empty_coordinates 

    def load_houses(self):
        """
        Returns a list of house objects based on the specified quantity with a
        fixed share of single houses (60%), bungalows (25%) and maisons (15%). 
        """
        
        # Determine quantity for each house type based on total quantity
        q_single = int(0.6 * self.quantity)
        q_bungalow = int(0.25 * self.quantity)
        q_maison = int(0.15 * self.quantity)

        all_houses = []
        id_counter = 1

        # Create correct quantiy of houses
        for q_type in [q_single, q_bungalow, q_maison]:
            for house in range(int(q_type)):
                # Assign each House instance according type
                if q_type == q_single:
                    new_house = House("single", id_counter) 
                elif q_type == q_bungalow:
                    new_house = House("bungalow", id_counter)
                else:
                    new_house = House("maison", id_counter)

                # Add House to dictionary and adjust id_counter
                all_houses.append(new_house)
                id_counter = id_counter + 1

        return all_houses

    def load_water(self):
        """
        Creates a Water object for each water surface and sets its
        coordinates based on source file. Returns a list of all
        Water objects.
        """

        all_water = []

        # Load coordinates of water surface(s) from source file
        with open(self.water, 'r') as in_file:
            # Skip header
            next(in_file)
        
            while True:
                # For each row, create list of all items
                row = in_file.readline().rstrip("\n")
                if row == "":
                    break
                items = row.split(",")
                strip_items = [item.strip("\"") for item in items]

                # Create a new water object
                water = Water()
            
                # Save water coordinates in dict
                water.coordinates = {'bottom_left': (int(strip_items[1]), int(strip_items[4])),
                                    'bottom_right': (int(strip_items[3]), int(strip_items[4])),
                                    'top_left': (int(strip_items[1]), int(strip_items[2])),
                                    'top_right': (int(strip_items[3]), int(strip_items[2]))}
        
                # Add water object to list
                all_water.append(water)   
        
        return all_water

    def define_object_coordinates(self, coordinates):
        """
        Returns a list of coordinates for a specific object.
        """

        object_coordinates = []

        for column in range(coordinates['top_left'][1], coordinates['bottom_right'][1]):
            for row in range(coordinates['top_left'][0], coordinates['bottom_right'][0]):

                current_coordinate = (row, column)
                object_coordinates.append(current_coordinate)

        return object_coordinates 

    def define_water_coordinates(self):
        """
        Returns a list of all water coordinates.
        """

        water_coordinates = []

        for water in self.all_water:
            coordinates = self.define_object_coordinates(water.coordinates)

            for coordinate in coordinates:
                water_coordinates.append(coordinate)

                # Remove from list of empty coordinates
                self.all_empty_coordinates.remove(coordinate)

        return water_coordinates


    # def assignment_house(self, house, cell, rotation="horizontal"):
        """ 
        Places house on map and returns new map.
        """

    #     print("Performing random assignment of house")
        
    #     # Retrieve coordinates random starting cell (top-left)
    #     cell_x = cell.x_coordinate
    #     cell_y = cell.y_coordinate

    #     # Set house coordinates (excluding and including mandatory free space)
    #     house_coordinates = house.calc_house_coordinates(cell_x, cell_y, rotation)
    #     house_coordinates_mandatory_free_space = house.calc_mandatory_free_space_coordinates(house_coordinates)

    #     # embed()

    #     # Define all cells of possible house location (excluding and including mandatory free space)
    #     house_cells = self.define_object_cells(house_coordinates)
    #     house_cells_mandatory_free_space = self.define_object_cells(house_coordinates_mandatory_free_space)

    #     spot_available = True

    #     # For each cell, check if placing a house would be valid
    #     for cell in house_cells_mandatory_free_space:
                
    #         # House cells must be empty, mandatory free space may not overlap with a house
    #         if ((cell in house_cells) and cell.type != None) or cell.occupied_by_house():
    #             spot_available = False
   
    #     # If all cells of possible location are still availabe 
    #     if spot_available:   

    #         for current_cell in house_cells_mandatory_free_space:

    #             # Set cells occupied by house to according house type
    #             if current_cell in house_cells:
    #                 current_cell.type = house.type

    #             # Mark cells occupied by mandatory free space 
    #             elif current_cell.type != house.type:  #Of gewoon else?
    #                 current_cell.type = MandatoryFreeSpace(house)

    #         # Save coordinates
    #         house.coordinates = house_coordinates
    #         house.min_free_coordinates = house_coordinates_mandatory_free_space

    #         # Save cells
    #         house.min_free_cells = house_cells_mandatory_free_space

    #     else:
    #         raise ValueError("Location of house unavailable.")

    def undo_assignment_house(self, house):
        """
        Reverts the placement of a house at a certain position.
        """
    
        for coordinate in house.coordinates:
            self.empty_coordinates.append(coordinate)
            self.house_coordinates.remove(coordinate)
        
        house.coordinates.clear()

    def assignment_house(self, house):
        """ 
        Assigns house to grid, based on coordinates of cell. Returns the new 
        grid.
        """

        # embed()
        print("Performing assignment of house")

        # Add coordinates to grid 
        self.all_house_coordinates.append(house.house_coordinates)
        self.all_man_free_coordinates.append(house.man_free_coordinates)

        # Remove from empty coordinates
        self.all_empty_coordinates = list(set(self.all_empty_coordinates) - set(house.house_coordinates) - set(house.man_free_coordinates))
    
    
    def calculate_extra_free_meters(self, house):
        """
        Returns how many extra free meters can be assigned to a given house.
        """

        print(f"Calculating extra free meters for: {house}")

        distance_found = False

        # i is number of extra free meters, starting from 1
        for i in itertools.count(start=1):

            all_coordinates = []
            extra_free_coordinates = []

            # Loop through all house coordinates including mandatory free space and i extra free space
            for row in range((house.outer_man_free_coordinates['top_left'][0] - i), (house.outer_man_free_coordinates['bottom_right'][0] + i)):
                for column in range((house.outer_man_free_coordinates['top_left'][1] - i), (house.outer_man_free_coordinates['bottom_right'][1] + i)):
                    
                    # Check if coordinates are within borders of grid
                    if row >= 0 and row <= 180 and column >= 0 and column <= 160:
                        current_coordinate = (row, column)
                        all_coordinates.append(current_coordinate)

            # Save coordinates that are extra free meters in list
            for coordinate in all_coordinates:
                if coordinate not in house.house_coordinates and coordinate not in house.man_free_coordinates:
                    extra_free_coordinates.append(coordinate)

            # Check for all extra free coordinates if it is a house
            for coordinate in extra_free_coordinates:
                if coordinate in self.all_house_coordinates:

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
        for house in self.all_houses:
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

        # # Assign value to grid (MISSCHIEN NIET HANDIG VOOR GREEDY?)
        # self.value = total_networth

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