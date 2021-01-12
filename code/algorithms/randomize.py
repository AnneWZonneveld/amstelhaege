import random
import copy

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

	house_coordinates = {'bottom_left_x': random_cell_x + house.width, 'bottom_left_y': random_cell_y, 'top_right_x': random_cell_x, 'top_right_y': random_cell_y + house.depth}

	# Set all grid cells of house to according house type
	for row in range(random_cell_y, random_cell_y + house.depth):
		for column in range(random_cell_x, random_cell_x + house.width):
			# print(f"current cell: {grid.cells[row,column]}")
			grid.cells[row, column].type = house.type

	all_info = [grid, house_coordinates]

	return all_info

def random_assignment(grid, houses):
	# print(f"grid: {grid}")
	# print(f"houses in random: {houses}")

	new_grid = copy.deepcopy(grid)
	all_house_coordinates = {}

	for house in houses.values():

		print(f"HOUSE: {house}")

		succes = False

		while succes == False:
			try:
				random_cell = random_empty_cell(new_grid)
				house_info = random_assignment_house(new_grid, house, random_cell)
				new_grid = house_info[0]
				house_coordinates = house_info[1]
				all_house_coordinates["%d" % house.id] = house_coordinates
				house.placed = True
				succes = True

				print(f"Updated grid:")
				new_grid.print_grid()
			except:
				print("Error")
				pass

		all_info = [new_grid, all_house_coordinates]

	return all_info
