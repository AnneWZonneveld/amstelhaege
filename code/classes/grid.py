import csv
import itertools
import numpy as np
from .house import House
from .water import Water
from code.classes.mandatory import MandatoryFreeSpace
import code.algorithms.randomize as rz
# from IPython import embed;

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

            id_counter = 1

            while True:

                # For each row, create list of all items
                row = in_file.readline().rstrip("\n")
                if row == "":
                    break
                items = row.split(",")
                strip_items = [item.strip("\"") for item in items]

                # Create a new water object
                water = Water()

                water.id = id_counter

                # Save water coordinates in dict
                water.coordinates = {'bottom_left': (int(strip_items[1]), int(strip_items[4])),
                                    'bottom_right': (int(strip_items[3]), int(strip_items[4])),
                                    'top_left': (int(strip_items[1]), int(strip_items[2])),
                                    'top_right': (int(strip_items[3]), int(strip_items[2]))}
        
                # Add water object to list
                all_water.append(water)   

                id_counter += 1
        
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


    def undo_assignment_house(self, house):
        """
        Reverts the placement of a house at a certain position.
        """
        
        for coordinate in house.house_coordinates:
            self.all_empty_coordinates.append(coordinate)
            self.all_house_coordinates.remove(coordinate)
        
        for coordinate in house.man_free_coordinates:
            self.all_empty_coordinates.append(coordinate)
            self.all_man_free_coordinates.remove(coordinate)
        
        house.house_coordinates.clear()

    def assignment_house(self, house):
        """ 
        Assigns house to grid, based on coordinates of cell. Returns the new 
        grid.
        """

        # embed()
        print("Performing assignment of house")

        # Add coordinates to grid 
        for coordinate in house.house_coordinates:
            self.all_house_coordinates.append(coordinate)
        
        for coordinate in house.man_free_coordinates:
            self.all_man_free_coordinates.append(coordinate)

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
                    if row >= 0 and row <= self.width and column >= 0 and column <= self.depth:
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

            # Add location of water to csv file
            for water_object in self.load_water():
                bottom_left = water_object.coordinates['bottom_left']
                bottom_right = water_object.coordinates['bottom_right']
                top_left = water_object.coordinates['top_left']
                top_right = water_object.coordinates['top_left']
                water_list = [water_object, bottom_left, bottom_right, top_left, top_right, "WATER"]
                writer.writerow(water_list)
            
            for house in self.all_houses:
                bottom_left = house.outer_house_coordinates['bottom_left']
                bottom_right = house.outer_house_coordinates['bottom_right']
                top_left = house.outer_house_coordinates['top_left']
                top_right = house.outer_house_coordinates['top_left']
                house_list = [f"{house.type}_{house.id}", bottom_left, bottom_right, top_left, top_right, house.type.upper()]
                writer.writerow(house_list)

            # Add total networth of map to csv file
            networth = self.calculate_worth()
            writer.writerow(["networth", networth])