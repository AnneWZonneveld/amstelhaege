import csv
import numpy as np
from .cell import Cell
from .house import House
# from IPython import embed;

class Grid():
    def __init__(self, quantity, source_file):
        self.width = 180
        self.depth = 160
        self.map = source_file
        self.quantity = quantity
        self.cells = self.load_grid()
        self.all_houses = self.load_houses()    
        self.create_water()      

    def load_grid(self):
        """
        Creates and returns a 2D array filled with cells. Each cell 
        represents one square meter on the map and is associated with
        coordinates that point to its unique position in the grid.
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
        Creates the specified quantity of houses with a fixed share of
        single houses (60%), bungalows (25%) and maisons (15%). Returns
        a dictionary that maps each house and its type to an ID.
        """
        

        # Determine demand for each house type based on total quantity
        q_single = int(0.6 * self.quantity)
        q_bungalow = int(0.25 * self.quantity)
        q_maison = int(0.15 * self.quantity)

        # Save houses in dict
        all_houses = {}

        # Create specified quantiy of House instances with according type
        id_counter = 1
        for q_type in [q_single, q_bungalow, q_maison]:
            for h in range(int(q_type)):
                # Create house an assign correct type
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
        Returns a dictionary that maps the water surface(s) on a given
        map to coordinates.
        """

        # Load coordinates of water surface(s) from source file
        with open(self.map, 'r') as in_file:

            water = {}
            
            # Skip header
            next(in_file)

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
        Transforms Cell objects into the 'water' type.
        """

        print("Creating water")

        all_water = self.load_water()
        print(f"All water: {all_water}")

        # Iterate over all water objects in dict
        for water in all_water:

            # # Define coordinates of water objects
            # for x in range(int(all_water[water]['bottom_left'][0]), int(all_water[water]['top_right'][0]) + 1):
            #     for y in range(int(all_water[water]['bottom_left'][1]), int(all_water[water]['top_right'][1]) + 1):

            #         # Transform cells into 'Water' type
            #         self.cells[y][x].type = "Water"

            # Define coordinates of water objects
            for y in range(int(all_water[water]['top_left'][1]), int(all_water[water]['bottom_right'][1]) + 1):
                for x in range(int(all_water[water]['bottom_left'][0]), int(all_water[water]['top_right'][0]) + 1):    
                    
                    # Transform cells into 'Water' type
                    self.cells[y][x].type = "Water"

    def calculate_extra_free_meters(self, house):
        print("Calculating extra free meters")

        #embed()
        for coordinate in house.coordinates:
            print("coordinate: {coordinate}")

    def calculate_worth(self):
        """
        Calculates worth of all House objects on grid. Returns the total net 
        worth.
        """

        # Create variable to calculate total net worth
        total_net_worth = 0

        for house in self.all_houses.values():
            print(house)

            # Calculate extra free meters
            self.calculate_extra_free_meters(house)

            if house.placed == True:
                # Net worth of house
                net_worth_house = house.price
            
                if house.extra_free_meters != 0:
                    # Add worth of extra free space to net worth of house
                    net_worth_house += house.extra_free_meters * house.percentage * house.price

                # Add net worth of house to total net worth
                total_net_worth = total_net_worth + net_worth_house
    
        return total_net_worth

    def create_output(self):
        """
        Creates csv-file that represents results from running the algorithm.
        """

        # how to create csv file from https://www.programiz.com/python-programming/writing-csv-files
        with open('data/output.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            # Create header
            fieldnames =["structure", "corner_1 (bottom_left)", "corner_2 (bottom_right)", "corner_3 (top_left)", "corner_4 (top_right)", "type"]
            writer.writerow(fieldnames)

            # Load water coordinates from correct map
            water = self.load_water()

            # Add location of water to csv file
            water_list = []
            for ident, coordinates in water.items():
                water_list = [ident, water[ident].get('bottom_left'), water[ident].get('bottom_right'), water[ident].get('top_left'), water[ident].get('top_right'), "WATER"]
                writer.writerow(water_list)
            
            for house in self.all_houses.values():
                house_list = f"{house.type}_{house.id}", house.coordinates['bottom_left'], house.coordinates['bottom_right'], house.coordinates['top_left'], house.coordinates['top_right'], house.type.upper()
                writer.writerow(house_list)
            
            # Add optimalization function to csv file
            optimalization = self.calculate_worth()
            writer.writerow(["networth", optimalization])