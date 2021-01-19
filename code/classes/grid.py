import csv
import numpy as np
from .cell import Cell
from .house import House
import code.algorithms.randomize as rz
# from IPython import embed;

class Grid():
    def __init__(self, quantity, source_file):
        self.width = 180
        self.depth = 160
        self.map = source_file
        self.quantity = quantity
        self.cells = self.load_grid()
        self.all_houses = self.load_houses() # misschien alleen list nodig?
        self.all_houses_list = rz.list_all_houses(self.all_houses)
        self.value = 0   
        self.create_water()      

    def load_grid(self):
        """
        Creates and returns a 2D array filled with cells. Each cell represents
        one square meter on the map and is associated with coordinates that
        point to its unique position in the grid.
        """
        
        grid = np.array([])
        for y in range(self.depth + 1 ):
            for x in range(self.width + 1):
                cell = Cell(x, y)
                grid = np.append(grid, cell)
        grid = np.resize(grid,(self.depth + 1, self.width + 1))

        return grid 

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

        all_houses = {}

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
                all_houses[id_counter] = house
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

    def calculate_extra_free_meters(self, house):
        """
        Returns how many extra free meters can be assigned to a given house.
        """

        shortest_distance = None

        # Calculate shortest distance for all sides of house
        for key in house.coordinates:

            # Check for key 
            if key == "top_right":

                # Loop through depth right side of house per meter
                for row in range(house.coordinates['top_right'][1], house.coordinates['bottom_right'][1] + 1):

                    # For every meter, loop from side house to side grid until you find other house
                    for column in range(house.coordinates['top_right'][0], self.width + 1):

                        # Check if cell is a house or if reached end of grid
                        if self.cells[row, column].type in ['bungalow', 'single', 'maison'] or column == self.width:

                            # Calculate distance and check if shortest
                            distance = column - house.coordinates['top_right'][0]
                            if shortest_distance == None:
                                shortest_distance = distance
                            elif distance < shortest_distance:
                                shortest_distance = distance
                            break

            elif key == "bottom_right":

                # Loop through width bottom side of house per meter
                for column in range(house.coordinates['bottom_left'][0], house.coordinates['bottom_right'][0] + 1):
                    
                    # For every meter, loop from bottom house to bottom grid
                    for row in range(house.coordinates['bottom_right'][1], self.depth + 1):

                        # Check if cell is a house or if reached end of grid
                        if self.cells[row, column].type in ['bungalow', 'single', 'maison'] or row == self.depth:

                            # Calculate distance and check if shortest
                            distance = row - house.coordinates['bottom_right'][1]
                            if shortest_distance == None:
                                shortest_distance = distance
                            elif distance < shortest_distance:
                                shortest_distance = distance
                            break 

            elif key == "bottom_left":

                # Loop through depth left side of house per meter
                for row in range(house.coordinates['top_left'][1], house.coordinates['bottom_left'][1] + 1 ):
                    
                    # For every meter, loop from side of house to side grid
                    for column in reversed(range(0, house.coordinates['top_left'][0])):

                        # Check if cell is a house or if reached end of grid
                        if self.cells[row, column].type in ['bungalow', 'single', 'maison'] or column == 0:

                            # Calculate distance and check if shortest
                            distance = house.coordinates['top_left'][0] - column 
                            if shortest_distance == None:
                                shortest_distance = distance
                            elif distance < shortest_distance:
                                shortest_distance = distance
                            break

            # Key = top_left
            else:

                # Loop through width top side of house per meter
                for column in range(house.coordinates['top_left'][0], house.coordinates['top_right'][0] + 1):
                    
                    # For every meter, loop from side of house to side grid
                    for row in reversed(range(0, house.coordinates['top_left'][1])):

                        # Check if cell is a house or if reached end of grid
                        if self.cells[row, column].type in ['bungalow', 'single', 'maison'] or row == 0:

                            # Calculate distance and check if shortest
                            distance = house.coordinates['top_left'][1] - row
                            if shortest_distance == None:
                                shortest_distance = distance
                            elif distance < shortest_distance:
                                shortest_distance = distance
                            break 

        # Calculate smallest extra free space
        house.extra_free = shortest_distance - house.min_free

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