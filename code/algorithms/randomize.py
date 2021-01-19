import random
import copy
from IPython import embed
# from code.classes.mandatory import MandatoryFreeSpace


def random_empty_cell(grid, house):
	"""
	Returns a random empty cell from grid.
	"""

	print("Performing picking empty cell")

	random_cell = random.choice(grid.define_empty_cells(house))
	return random_cell


def random_rotation_choice():
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
	all_houses = copy_grid.list_all_houses()
	for house in reversed(all_houses):
		# embed()

		print(f"Trying to place: {house}")

		while house.placed == False:
			try:
				random_cell = random_empty_cell(copy_grid, house)
				copy_grid.assignment_house(house, random_cell, rotation = "random")
				house.placed = True

			except:
				print("Error")
				pass

	print("All houses placed succesfully")

	return copy_grid
