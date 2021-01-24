import csv
import itertools
import numpy as np
from .house import House
from .water import Water
from shapely.geometry import Point
from code.classes.mandatory import MandatoryFreeSpace
from shapely.geometry import Point
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
        
        house.placed = False

    def assignment_house(self, house):
        """ 
        Assigns house to grid, based on coordinates of cell. Returns the new 
        grid.
        """

        # Add coordinates to grid 
        for coordinate in house.house_coordinates:
            self.all_house_coordinates.append(coordinate)
        
        for coordinate in house.man_free_coordinates:
            self.all_man_free_coordinates.append(coordinate)

        # Remove from empty coordinates
        self.all_empty_coordinates = list(set(self.all_empty_coordinates) - set(house.house_coordinates) - set(house.man_free_coordinates))

        house.placed = True
    
    def calculate_extra_free_meters(self, house):
        """
        Returns how many extra free meters can be assigned to a given house.
        """

        print(f"Calculating extra free meters for: {house}")

        # MISSCHIEN NOG AANPASSEN?
        house.extra_free = 10000

        # For all houses other than the selected one
        for other_house in self.all_houses:
            if other_house != house and other_house.placed:
                
                # other_house linksboven van house
                if other_house.outer_house_coordinates['bottom_right'][0] <= house.outer_house_coordinates['top_left'][0] and other_house.outer_house_coordinates['bottom_right'][1] <= house.outer_house_coordinates['top_left'][1]:
                    house_x = house.outer_house_coordinates['top_left'][0]
                    house_y = house.outer_house_coordinates['top_left'][1]
                    other_house_x = other_house.outer_house_coordinates['bottom_right'][0]
                    other_house_y = other_house.outer_house_coordinates['bottom_right'][1]
                    distance = Point(house_x,house_y).distance(Point(other_house_x,other_house_y))
                    extra_free_space = distance - house.min_free

                # other_house rechtsboven van house
                elif other_house.outer_house_coordinates['bottom_left'][0] >= house.outer_house_coordinates['top_right'][0] and other_house.outer_house_coordinates['bottom_left'][1] <= house.outer_house_coordinates['top_right'][1]:
                    house_x = house.outer_house_coordinates['top_right'][0]
                    house_y = house.outer_house_coordinates['top_right'][1]
                    other_house_x = other_house.outer_house_coordinates['bottom_left'][0]
                    other_house_y = other_house.outer_house_coordinates['bottom_left'][1]
                    distance = Point(house_x,house_y).distance(Point(other_house_x,other_house_y))
                    extra_free_space = distance - house.min_free
                
                # other_house rechtsonder van house
                elif other_house.outer_house_coordinates['top_left'][0] >= house.outer_house_coordinates['bottom_right'][0] and other_house.outer_house_coordinates['top_left'][1] >= house.outer_house_coordinates['bottom_right'][1]:
                    house_x = house.outer_house_coordinates['bottom_right'][0]
                    house_y = house.outer_house_coordinates['bottom_right'][1]
                    other_house_x = other_house.outer_house_coordinates['top_left'][0]
                    other_house_y = other_house.outer_house_coordinates['top_left'][1]
                    distance = Point(house_x,house_y).distance(Point(other_house_x,other_house_y))
                    extra_free_space = distance - house.min_free

                # other_house linksonder van house
                elif other_house.outer_house_coordinates['top_right'][0] <= house.outer_house_coordinates['bottom_left'][0] and other_house.outer_house_coordinates['top_right'][1] >= house.outer_house_coordinates['bottom_left'][1]:
                    house_x = house.outer_house_coordinates['bottom_left'][0]
                    house_y = house.outer_house_coordinates['bottom_left'][1]
                    other_house_x = other_house.outer_house_coordinates['top_right'][0]
                    other_house_y = other_house.outer_house_coordinates['top_right'][1]
                    distance = Point(house_x,house_y).distance(Point(other_house_x,other_house_y))
                    extra_free_space = distance - house.min_free

                # other_house boven house
                elif other_house.outer_house_coordinates['bottom_left'][1] < house.outer_house_coordinates['top_left'][1]:
                    distance = house.outer_house_coordinates['top_left'][1] - other_house.outer_house_coordinates['bottom_left'][1]
                    extra_free_space = distance - house.min_free

                # other_house rechts van house
                elif other_house.outer_house_coordinates['bottom_left'][0] > house.outer_house_coordinates['bottom_right'][0]:
                    distance = other_house.outer_house_coordinates['bottom_left'][0] - house.outer_house_coordinates['bottom_right'][0]
                    extra_free_space = distance - house.min_free

                # other_house onder house
                elif other_house.outer_house_coordinates['top_left'][1] > house.outer_house_coordinates['bottom_left'][1]:
                    distance = other_house.outer_house_coordinates['top_left'][1] - house.outer_house_coordinates['bottom_left'][1]
                    extra_free_space = distance - house.min_free

                # other_house links van house
                elif other_house.outer_house_coordinates['bottom_right'][0] < house.outer_house_coordinates['bottom_left'][0]:
                    distance = house.outer_house_coordinates['bottom_left'][0] - other_house.outer_house_coordinates['bottom_right'][0]
                    extra_free_space = distance - house.min_free

                print(f"Extra free space: {extra_free_space}")

                # If extra free space is shorter than the current one, replace
                if extra_free_space < house.extra_free:
                    house.extra_free = extra_free_space
                    
                    print(f"NEW SHORTEST EXTRA FREE SPACE: {house.extra_free}")

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

        # Assign value to grid (MISSCHIEN NIET HANDIG VOOR GREEDY?)
        self.value = total_networth

        return total_networth

    def create_output(self, name):
        """
        Creates csv-file with results from running an algorithm to place houses.
        """

        with open(f'data/output/csv/output_{name}.csv', 'w', newline='') as file:
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
            networth = self.value
            writer.writerow(["networth", networth])