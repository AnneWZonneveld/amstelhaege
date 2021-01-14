import random
import copy
from code.classes.mandatory import MandatoryFreeSpace
# from IPython import embed

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

	# embed()

	print("Performing random_assignment_house")
	
	# Retrieve coordinates random starting cell (top-left)
	random_cell_x = random_cell.x_coordinate
	random_cell_y = random_cell.y_coordinate

	# Set house coordinates
	house_coordinates = {
		'bottom_left': (random_cell_x, random_cell_y + house.depth), 
		'bottom_right': (random_cell_x + house.width, random_cell_y + house.depth), 
		'top_left': (random_cell_x, random_cell_y),
		'top_right': (random_cell_x + house.width, random_cell_y)
		}

	# Set house coordinates including mandatory free space
	house_coordinates_mandatory_free_space = {
		'bottom_left': (house_coordinates['bottom_left'][0] - house.min_free, house_coordinates['bottom_left'][1] + house.min_free), 
		'bottom_right': (house_coordinates['bottom_right'][0] + house.min_free, house_coordinates['bottom_right'][1] + house.min_free), 
		'top_left': (house_coordinates['top_left'][0] - house.min_free, house_coordinates['top_left'][1] - house.min_free),
		'top_right': (house_coordinates['top_right'][0] + house.min_free, house_coordinates['top_right'][1] - house.min_free)
		}

	# Check for all cells of possible house location if occupied 
	occupied = False

	for row in range(random_cell_y, random_cell_y + house.width):
		for column in range(random_cell_x, random_cell_x + house.depth):

			current_cell = grid.cells[row, column]
			
			if current_cell.type != None:
				occupied = True
	
	# Iterate over all grid cells of house including mandatory free space
	for row in range((house_coordinates['top_left'][1] - house.min_free), (house_coordinates['bottom_right'][1] + house.min_free)):
		for column in range((house_coordinates['top_left'][0] - house.min_free), (house_coordinates['bottom_right'][0] + house.min_free)):

			current_cell = grid.cells[row, column]

			# Ensure every cell of mandatory free space is empty (not the mandatory free space of another house)
			if current_cell.type not in [None, 'Water']:
				occupied = True
	
	# If all cells of possible location are still availabe 
	if occupied == False:

		# Set cells to according house type
		for row in range(random_cell_y, random_cell_y + house.depth):
			for column in range(random_cell_x, random_cell_x + house.width):
				current_cell = grid.cells[row, column]
				current_cell.type = house.type

		# Iterate over all grid cells of house including mandatory free space
		for row in range((house_coordinates['top_left'][1] - house.min_free), (house_coordinates['bottom_right'][1] + house.min_free)):
			for column in range((house_coordinates['top_left'][0] - house.min_free), (house_coordinates['bottom_right'][0] + house.min_free)):

				current_cell = grid.cells[row, column]

				# Set all grid cells mandatory free space of house to according type
				if current_cell.type != house.type:
					current_cell.type = MandatoryFreeSpace(house)

		# Save coordinates
		house.coordinates = house_coordinates
		house.min_free_coordinates = house_coordinates_mandatory_free_space

	else:
		raise ValueError("Location of house unavailable.")

	return grid


def random_assignment(grid):

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

				print(f"Updated grid:")
				new_grid.print_grid()
			except:
				print("Error")
				pass

	return new_grid
