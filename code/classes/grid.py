import csv
import os
from .house import House
from .water import Water
from code.constants import *
from shapely.geometry import Point


# Constants
MAX_EXTRA_FREE = 250
GRID_WIDTH = 180
GRID_DEPTH = 160
PERC_SINGLE = 0.6
PERC_BUNGALOW = 0.25
PERC_MAISON = 0.15

class Grid():
    def __init__(self, quantity, source_file):
        self.width = GRID_WIDTH
        self.depth = GRID_DEPTH
        self.quantity = quantity
        self.water = source_file
        self.all_houses = self.load_houses()
        self.all_water = self.load_water()
        self.all_empty_coordinates = self.load_empty_coordinates()
        self.all_water_coordinates = self.define_water_coordinates()
        self.all_house_coordinates = []
        self.all_man_free_coordinates = []
        self.value = 0   


    def load_houses(self):
        """
        Returns a list of house objects based on the specified quantity with a
        fixed share of single houses (60%), bungalows (25%) and maisons (15%). 
        """
        
        # Determine quantity for each house type based on total quantity
        q_single = int(PERC_SINGLE * self.quantity)
        q_bungalow = int(PERC_BUNGALOW * self.quantity)
        q_maison = int(PERC_MAISON * self.quantity)

        all_houses = []
        id_counter = 1

        # Create correct quantiy of houses
        for q_type in [q_maison, q_bungalow, q_single]:

            for house in range(int(q_type)):

                # Assign each House instance according type
                if q_type == q_maison:
                    new_house = House("maison", id_counter) 
                elif q_type == q_bungalow:
                    new_house = House("bungalow", id_counter)
                else:
                    new_house = House("single", id_counter)
                    
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
                water.coordinates = {"bottom_left": (int(strip_items[1]), int(strip_items[4])),
                                    "bottom_right": (int(strip_items[3]), int(strip_items[4])),
                                    "top_left": (int(strip_items[1]), int(strip_items[2])),
                                    "top_right": (int(strip_items[3]), int(strip_items[2]))}
        
                # Add water object to list
                all_water.append(water)   

                id_counter += 1
        
        return all_water


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


    def define_object_coordinates(self, coordinates):
        """
        Returns a list of coordinates for a specific object.
        """

        object_coordinates = []

        for x in range(coordinates['top_left'][0], coordinates['bottom_right'][0]):
            
            for y in range(coordinates['top_left'][1], coordinates['bottom_right'][1]):
        
                current_coordinate = (x, y)
                object_coordinates.append(current_coordinate)

        return object_coordinates 


    def assignment_house(self, house):
        """ 
        Assigns house to grid, based on its coordinates.
        """

        print("Performing assignment of house")

        # Add coordinates to grid 
        for coordinate in house.house_coordinates:
            self.all_house_coordinates.append(coordinate)
        
        for coordinate in house.man_free_coordinates:
            self.all_man_free_coordinates.append(coordinate)

        # Remove from empty coordinates
        self.all_empty_coordinates = list(set(self.all_empty_coordinates) - set(house.house_coordinates) - set(house.man_free_coordinates))

        house.placed = True


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

    
    def calculate_extra_free_meters(self, house):
        """
        Returns how many extra free meters can be assigned to a given house.
        """

        #print(f"Calculating extra free meters for: {house}")

        # Set extra free meters to the possible maximum
        house.extra_free = Point(0,0).distance(Point(GRID_WIDTH,GRID_DEPTH))

        # For all placed houses other than the selected one
        for other_house in self.all_houses:
            if other_house != house and other_house.placed:
                
                # If other_house is at the top left of the house
                if other_house.outer_house_coordinates["bottom_right"][0] <= house.outer_house_coordinates["top_left"][0] and other_house.outer_house_coordinates["bottom_right"][1] <= house.outer_house_coordinates["top_left"][1]:
                    house_xy = house.outer_house_coordinates["top_left"]
                    other_house_xy = other_house.outer_house_coordinates["bottom_right"]
                    distance = Point(house_xy[0],house_xy[1]).distance(Point(other_house_xy[0],other_house_xy[1]))

                # If other_house is at the top right of the house
                elif other_house.outer_house_coordinates["bottom_left"][0] >= house.outer_house_coordinates["top_right"][0] and other_house.outer_house_coordinates["bottom_left"][1] <= house.outer_house_coordinates["top_right"][1]:
                    house_xy = house.outer_house_coordinates["top_right"]
                    other_house_xy = other_house.outer_house_coordinates["bottom_left"]
                    distance = Point(house_xy[0],house_xy[1]).distance(Point(other_house_xy[0],other_house_xy[1]))
                
                # If other_house is at the bottom right of the house
                elif other_house.outer_house_coordinates["top_left"][0] >= house.outer_house_coordinates["bottom_right"][0] and other_house.outer_house_coordinates["top_left"][1] >= house.outer_house_coordinates["bottom_right"][1]:
                    house_xy = house.outer_house_coordinates["bottom_right"]
                    other_house_xy = other_house.outer_house_coordinates["top_left"]
                    distance = Point(house_xy[0],house_xy[1]).distance(Point(other_house_xy[0],other_house_xy[1]))

                # If other_house is at the bottom left of the house
                elif other_house.outer_house_coordinates["top_right"][0] <= house.outer_house_coordinates["bottom_left"][0] and other_house.outer_house_coordinates["top_right"][1] >= house.outer_house_coordinates["bottom_left"][1]:
                    house_xy = house.outer_house_coordinates["bottom_left"]
                    other_house_xy = other_house.outer_house_coordinates["top_right"]
                    distance = Point(house_xy[0],house_xy[1]).distance(Point(other_house_xy[0],other_house_xy[1]))

                # If other_house is above the house
                elif other_house.outer_house_coordinates["bottom_left"][1] < house.outer_house_coordinates["top_left"][1]:
                    distance = house.outer_house_coordinates["top_left"][1] - other_house.outer_house_coordinates["bottom_left"][1]

                # If other_house is to the right of the house
                elif other_house.outer_house_coordinates["bottom_left"][0] > house.outer_house_coordinates["bottom_right"][0]:
                    distance = other_house.outer_house_coordinates["bottom_left"][0] - house.outer_house_coordinates["bottom_right"][0]

                # If other_house is below the house
                elif other_house.outer_house_coordinates["top_left"][1] > house.outer_house_coordinates["bottom_left"][1]:
                    distance = other_house.outer_house_coordinates["top_left"][1] - house.outer_house_coordinates["bottom_left"][1]

                # If other_house is to the left of the house
                elif other_house.outer_house_coordinates["bottom_right"][0] < house.outer_house_coordinates["bottom_left"][0]:
                    distance = house.outer_house_coordinates["bottom_left"][0] - other_house.outer_house_coordinates["bottom_right"][0]
                
                # Calculate extra free space
                extra_free_space = distance - house.min_free

                # If extra free space is less than the current amount, replace
                if extra_free_space < house.extra_free:
                    house.extra_free = extra_free_space
                    
        # print(f"Extra free space for {house}: {house.extra_free}")

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

        # Round to nearest integer
        total_networth = int(round(total_networth))

        # Assign value to grid
        self.value = total_networth
        
        return total_networth


    def create_output(self, map_name, quantity, name):
        """
        Creates a csv-file with results from running an algorithm to place 
        houses.
        """

        # embed()

        path = f"data/output/{map_name}/{quantity}/csv/{name}"

        if not os.path.exists(path):
            os.makedirs(path)

        with open(f"{path}/output.csv", "w", newline='') as file:
            writer = csv.writer(file)

            # Create header
            fieldnames =["structure", "corner_1", "corner_2", "corner_3", "corner_4", "type"]
            writer.writerow(fieldnames)

            # Add location of water to csv file
            for water_object in self.load_water():
                bottom_left = f"{water_object.coordinates['bottom_left'][0]},{water_object.coordinates['bottom_left'][1]}"
                bottom_right = f"{water_object.coordinates['bottom_right'][0]},{water_object.coordinates['bottom_right'][1]}"
                top_left = f"{water_object.coordinates['top_left'][0]},{water_object.coordinates['top_left'][1]}"
                top_right = f"{water_object.coordinates['top_right'][0]},{water_object.coordinates['top_right'][1]}"
                water_list = [water_object, bottom_left, top_left, top_right, bottom_right, "WATER"]
                writer.writerow(water_list)
            
            for house in self.all_houses:

                # Determine label
                if house.type == "single":
                    label = "eengezinswoning"
                else:
                    label = house.type

                bottom_left = f"{house.outer_house_coordinates['bottom_left'][0]},{house.outer_house_coordinates['bottom_left'][1]}"
                bottom_right = f"{house.outer_house_coordinates['bottom_right'][0]},{house.outer_house_coordinates['bottom_right'][1]}"
                top_left = f"{house.outer_house_coordinates['top_left'][0]},{house.outer_house_coordinates['top_left'][1]}"
                top_right = f"{house.outer_house_coordinates['top_right'][0]},{house.outer_house_coordinates['top_right'][1]}"
                house_list = [f"{label}_{house.id}", bottom_left, top_left, top_right, bottom_right, label.upper()]
                writer.writerow(house_list)

            # Add total networth of map to csv file
            networth = self.value
            writer.writerow(["networth", networth])