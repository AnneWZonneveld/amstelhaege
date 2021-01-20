import random
import copy

from IPython import embed


def random_empty_cell(grid):
	"""
	Returns a random empty cell from grid.
	"""

	print("Performing picking empty cell")

	random_cell = random.choice(grid.empty_coordinates)
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
	for house in reversed(houses):
		# embed()

		print(f"Trying to place: {house}")

		while house.placed == False:
				random_cell = random_empty_cell(copy_grid)
				house.outer_coordinates = house.calc_house_coordinates()
				house.outer_man_free_coordinates = house.calc_man_free_coordinates()

				if house.valid_location(copy_grid):
					
					# if true -- >assign coordinates
					copy_grid.assignment_house(house, random_cell, rotation = "random")
					house.placed = True

	print("All houses placed succesfully")

	return copy_grid
