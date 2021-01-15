import random
import copy
from code.classes.mandatory import MandatoryFreeSpace


def define_empty_cells(grid):
	"""
	Returns a list of all empty cells on grid.
	"""

	empty_cells = []

	for row in grid.cells:
		for cell in row:
			if cell.type == None:
				empty_cells.append(cell)
	
	return empty_cells


def random_empty_cell(grid):
	"""
	Returns a random empty cell from grid.
	"""

	print("Performing picking empty cell")

	random_cell = random.choice(define_empty_cells(grid))
	return random_cell


def random_assignment_house(grid, house, random_cell):
	""" 
	Assigns house to grid, based on coordinates of random cell. Returns the new 
	grid.
	"""

	print("Performing random assignment of house")
	
	# Retrieve coordinates random starting cell (top-left)
	random_cell_x = random_cell.x_coordinate
	random_cell_y = random_cell.y_coordinate

	# Set house coordinates (excluding and including mandatory free space)
	house_coordinates = set_house_coordinates(house, random_cell_x, random_cell_y)
	house_coordinates_mandatory_free_space = set_house_coordinates_mandatory_free_space(house, house_coordinates)

	# Define all cells of possible house location (excluding and including mandatory free space)
	house_cells = define_object_cells(grid, house_coordinates)
	house_cells_mandatory_free_space = define_object_cells(grid, house_coordinates_mandatory_free_space)

	occupied = False

	# Check for all cells of possible house location if occupied 
	for current_cell in house_cells:
		if current_cell.type != None:
			occupied = True

	# Check for all cells of possible mandatory free space location if occupied
	for current_cell in house_cells_mandatory_free_space:
		if current_cell.type in ['single', 'bungalow', 'maison']: #AANPASSEN?
			occupied = True
	
	# If all cells of possible location are still availabe 
	if occupied == False:

		# Set cells to according house type
		for current_cell in house_cells:
			current_cell.type = house.type

		# Set cells to according mandatory free space type
		for current_cell in house_cells_mandatory_free_space:
			if current_cell.type != house.type:
				current_cell.type = MandatoryFreeSpace(house)

		# Save coordinates
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


def random_assignment(grid):
	"""
	Places all houses randomly on grid. Returns the new grid.
	"""

	# Copy empty grid 
	copy_grid = copy.deepcopy(grid)
	houses = copy_grid.all_houses
	
	# Try to place all houses on grid at valid location 
	for house in houses.values():

		print(f"HOUSE: {house}")

		while house.placed == False:
			try:
				random_cell = random_empty_cell(copy_grid)
				new_grid = random_assignment_house(copy_grid, house, random_cell)
				house.placed = True

			except:
				print("Error")
				pass

	print("All houses placed succesfully")

	return new_grid