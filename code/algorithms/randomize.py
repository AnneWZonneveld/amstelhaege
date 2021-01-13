import random
import copy
from code.classes.mandatory import MandatoryFreeSpace

def random_empty_cell(grid):
	""" 
	Picks a random empty cell from grid.
	"""

	print("Perfoming picking empty cell")

	empty_cells = []

	for row in grid.cells:
		for cell in row:
			if cell.type == None:
				empty_cells.append(cell)

	# print(f"empty_cells: {empty_cells}")
	random_cell = random.choice(empty_cells)
	print(f"random_start_cell: {random_cell}")

	return random_cell

def random_assignment_house(grid, house, random_cell):
	""" 
	Assigns house to grid, based on coordinates of random cell.
	"""

	print("Performing random_assignment_house")
	
	# Pick random empty cell
	random_cell_x = random_cell.x_coordinate
	random_cell_y = random_cell.y_coordinate

	# Set house coordinates
	house_coordinates = {
		'bottom_left': (random_cell_x, random_cell_y + house.width), 
		'bottom_right': (random_cell_x + house.depth, random_cell_y + house.width), 
		'top_left': (random_cell_x, random_cell_y),
		'top_right': (random_cell_x + house.depth, random_cell_y)
		}

	# Set all grid cells of house to according house type
	for row in range(random_cell_y, random_cell_y + house.width):
		for column in range(random_cell_x, random_cell_x + house.depth):
			# print(f"current cell: {grid.cells[row,column]}")
			# grid.cells[row, column].type = house.type

			current_cell = grid.cells[row, column]
			
			# Ensure every cell of house location is empty (not water or other house)
			if current_cell.type == None:
				current_cell.type = house.type
			else:
				raise ValueError("Location of house unavailable.")

	all_info = [grid, house_coordinates]

	return all_info


def mandatory_free_space_house(grid, house):
	"""
	Checks that the mandatory free space of a house does not overlap with other 
	mandatory free space. Marks cells as mandatory free space of house.
	"""

	print("Performing mandatory_free_space_house")

	# Set house coordinates including mandatory free space
	house_coordinates_mandatory_free_space = {
		'bottom_left': (house.coordinates['bottom_left'][0] - house.min_free, house.coordinates['bottom_left'][1] - house.min_free), 
		'bottom_right': (house.coordinates['bottom_right'][0] + house.min_free, house.coordinates['bottom_right'][1] + house.min_free), 
		'top_left': (house.coordinates['top_left'][0] - house.min_free, house.coordinates['top_left'][1] - house.min_free),
		'top_right': (house.coordinates['top_right'][0] + house.min_free, house.coordinates['top_right'][1] + house.min_free)
		}

	# Iterate over all grid cells of house including mandatory free space
	for row in range((house.coordinates['top_left'][1] - house.min_free), (house.coordinates['bottom_right'][1] + house.min_free)):
		for column in range((house.coordinates['top_left'][0] - house.min_free), (house.coordinates['bottom_right'][0] + house.min_free)):

			current_cell = grid.cells[row, column]

			# Ensure every cell of mandatory free space is empty (not the mandatory free space of another house)
			if current_cell.type not in [None, 'Water']:
				raise ValueError("Location mandatory free space of house unavailable.")

	# Iterate over all grid cells of house including mandatory free space
	for row in range((house.coordinates['top_left'][1] - house.min_free), (house.coordinates['bottom_right'][1] + house.min_free)):
		for column in range((house.coordinates['top_left'][0] - house.min_free), (house.coordinates['bottom_right'][0] + house.min_free)):

			current_cell = grid.cells[row, column]

			# Set all grid cells mandatory free space of house to according type
			if current_cell.type != house.type:
				current_cell.type = MandatoryFreeSpace(house)
	
	house.min_free_coordinates = house_coordinates_mandatory_free_space

	return grid


def random_assignment(grid):
	# print(f"grid: {grid}")
	# print(f"houses in random: {houses}")

	new_grid = copy.deepcopy(grid)
	houses = new_grid.all_houses
	
	for house in houses.values():

		print(f"HOUSE: {house}")

		succes = False

		while succes == False:
			try:
				random_cell = random_empty_cell(new_grid)
				house_info = random_assignment_house(new_grid, house, random_cell)
				house.coordinates = house_info[1]
				print(f"House coordinates: {house.coordinates}")
				succes = True

				print(f"Updated grid:")
				second_grid.print_grid()
			except:
				print("Error")
				pass

	return second_grid