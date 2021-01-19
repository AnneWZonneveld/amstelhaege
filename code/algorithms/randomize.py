import random
import copy
from code.classes.mandatory import MandatoryFreeSpace

def define_empty_cells(grid, house):
	"""
	Returns a list of all cells on grid where house could be placed. Cells
	must be empty and keep a distance from the map's border that is equal
	to or bigger than the house's mandatory free space.
	"""

	empty_cells = []

	for row in grid.cells:
		for cell in row:
			if cell.x_coordinate >= house.min_free and cell.y_coordinate >= house.min_free and cell.type == None:
				empty_cells.append(cell)
	
	return empty_cells

def random_empty_cell(grid, house):
	"""
	Returns a random empty cell from grid.
	"""

	print("Performing picking empty cell")

	random_cell = random.choice(define_empty_cells(grid, house))
	return random_cell

def random_assignment_house(grid, house, random_cell):
	""" 
	Assigns house to grid, based on coordinates of random cell. Returns the new 
	grid.
	"""

	print("Performing random assignment of house")
	
	# Retrieve coordinates of random starting cell (top-left)
	random_cell_x = random_cell.x_coordinate
	random_cell_y = random_cell.y_coordinate

	# Set house coordinates (excluding and including mandatory free space)
	house_coordinates = set_house_coordinates(house, random_cell_x, random_cell_y)
	house_coordinates_mandatory_free_space = set_house_coordinates_mandatory_free_space(house, house_coordinates)

	# Define all cells of possible house location (excluding and including mandatory free space)
	house_cells = define_object_cells(grid, house_coordinates)
	house_cells_mandatory_free_space = define_object_cells(grid, house_coordinates_mandatory_free_space)

	# ONLY ONE FOR-LOOP
	# ADDED "occupied_by_house()" METHOD TO CELL.PY

	spot_available = True

	# For each cell, check if placing a house would be valid
	for cell in house_cells_mandatory_free_space:
		# House cells must be empty, mandatory free space may not overlap with a house
		if ((cell in house_cells) and cell.type != None) or cell.occupied_by_house():
			spot_available = False
	
	# Place house if all cells are still availabe 
	if spot_available:
		for current_cell in house_cells_mandatory_free_space:
			# Set cells occupied by house to according house type
			if current_cell in house_cells:
				current_cell.type = house.type
			# Mark cells occupied by mandatory free space 
			elif current_cell.type != house.type:
				current_cell.type = MandatoryFreeSpace(house)

		# Save house coordinates
		house.coordinates = house_coordinates
		house.min_free_coordinates = house_coordinates_mandatory_free_space
	else:
		raise ValueError("Location of house unavailable.")

	return grid

def random_rotation_choice():
	"""
	Returns a random rotation.
	"""

	rotation = ['horizontal', 'vertical']
	random_rotation = random.choice(rotation)

	return random_rotation

def set_house_coordinates(house, random_cell_x, random_cell_y):
	"""
	Returns a dictionary of house coordinates (excluding mandatory free space).
	"""

	random_rotation = random_rotation_choice()

	if random_rotation == 'horizontal':
		width = house.width
		depth = house.depth
	else:
		width = house.depth
		depth = house.width

	house_coordinates = {
		'bottom_left': (random_cell_x, random_cell_y + depth), 
		'bottom_right': (random_cell_x + width, random_cell_y + depth), 
		'top_left': (random_cell_x, random_cell_y),
		'top_right': (random_cell_x + width, random_cell_y)
		}
	
	return house_coordinates

def set_house_coordinates_mandatory_free_space(house, house_coordinates):
	"""
	Returns a dictionary of house coordinates (including mandatory free space).
	"""

	house_coordinates_mandatory_free_space = {
		'bottom_left': (house_coordinates['bottom_left'][0] - house.min_free, house_coordinates['bottom_left'][1] + house.min_free), 
		'bottom_right': (house_coordinates['bottom_right'][0] + house.min_free, house_coordinates['bottom_right'][1] + house.min_free), 
		'top_left': (house_coordinates['top_left'][0] - house.min_free, house_coordinates['top_left'][1] - house.min_free),
		'top_right': (house_coordinates['top_right'][0] + house.min_free, house_coordinates['top_right'][1] - house.min_free)
		}

	return house_coordinates_mandatory_free_space


def define_object_cells(grid, coordinates):
	"""
	Returns a list of cells for a specific object.
	"""

	object_cells = []

	for row in range(coordinates['top_left'][1], coordinates['bottom_right'][1]):
		for column in range(coordinates['top_left'][0], coordinates['bottom_right'][0]):

			current_cell = grid.cells[row, column]
			object_cells.append(current_cell)

	return object_cells


def list_all_houses(houses):
	"""
	Returns a list of all houses.
	"""

	all_houses = []
	
	for house in houses.values():
		all_houses.append(house)

	return all_houses


def random_assignment(grid):
	"""
	Places all houses randomly on grid. Returns the new grid.
	"""

	# Copy empty grid 
	copy_grid = copy.deepcopy(grid)
	houses = copy_grid.all_houses
	
	# Try to place all houses on grid at valid location, from large to small (heuristic)
	all_houses = list_all_houses(houses)
	for house in reversed(all_houses):

		print(f"Trying to place: {house}")

		while house.placed == False:
			try:
				random_cell = random_empty_cell(copy_grid, house)
				new_grid = random_assignment_house(copy_grid, house, random_cell)
				house.placed = True

			except:
				print("Error")
				pass

	print("All houses placed succesfully")

	return new_grid