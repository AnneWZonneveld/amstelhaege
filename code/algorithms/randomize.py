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

	print("Performing random_assignment_house")
	
	# Pick random empty cell
	random_cell_x = random_cell.x_coordinate
	random_cell_y = random_cell.y_coordinate

	for row in range(random_cell_y, random_cell_y + house.depth):
		for column in range(random_cell_x, random_cell_x + house.width):
			# print(f"current cell: {grid.cells[row,column]}")
			grid.cells[row, column].type = house.type

	return grid

def random_assignment(grid, houses):
	# print(f"grid: {grid}")
	# print(f"houses in random: {houses}")

	new_grid = copy.deepcopy(grid)

	for house in houses.values():

		print(f"HOUSE: {house}")

		succes = False

		while succes == False:
			try:
				random_cell = random_empty_cell(new_grid)
				new_grid = random_assignment_house(new_grid, house, random_cell)
				succes = True
				print(f"Updated grid:")
				new_grid.print_grid()
			except:
				print("Error")
				pass

		# print(house)
		# print(new_grid.cells)

		# # Pick random empty cell
		# random_cell = random_empty_cell(new_grid)
		# random_cell_x = random_cell.x_coordinate
		# random_cell_y = random_cell.y_coordinate
		# print(f"random_start_cell: {random_cell}")

		# for row in range(random_cell_y, random_cell_y + house.depth):
		# 	for column in range(random_cell_x, random_cell_x + house.width):
		# 		print(f"current cell: {new_grid.cells[row,column]}")
		# 		new_grid.cells[row, column].type = house.type				

	return new_grid
