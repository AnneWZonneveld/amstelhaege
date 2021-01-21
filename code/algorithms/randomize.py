import random
import copy

# Tools
from IPython import embed
from code.visualization import visualize as vis

        print("Performing picking empty coordinate")

        random_coordinate = random.choice(grid.all_empty_coordinates)
        
        return random_coordinate

def random_rotation():
	"""
	Returns a random rotation.
	"""

	rotation = ['horizontal', 'vertical']
	random_rotation = random.choice(rotation)

	return random_rotation


def random_assignment(grid):
	"""
	Places all houses randomly on grid. Returns the new grid.
	"""

	# Copy empty grid 
	copy_grid = copy.deepcopy(grid)
	houses = copy_grid.all_houses
	
	# Try to place all houses on grid at valid location, from large to small (heuristic)
	for house in reversed(houses):
		
		#embed()

		print(f"Trying to place: {house}")

		while house.placed == False:

				random_coordinate = random_empty_coordinate(copy_grid)
				print(f"random cell: {random_coordinate}")

				rotation = random_rotation()

				# Samenvoegen tot 1 functie die ook rotatie parameter heeft? returnt dictionary 
				house.outer_house_coordinates = house.calc_house_coordinates(random_cell, rotation)
				house.outer_man_free_coordinates = house.calc_man_free_coordinates(house.outer_house_coordinates)

				if house.valid_location(copy_grid):
					print("Valid location")

					#Assign house to grid
					copy_grid.assignment_house(house)
					house.placed = True
				else:
					print("Invalid location, retry")

	print("All houses placed succesfully")

	return copy_grid
