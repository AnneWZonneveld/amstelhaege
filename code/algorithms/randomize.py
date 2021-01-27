###############################################################################
# randomize.py
#
# Programmeertheorie
# Anne Zonneveld, Fleur Tervoort, Seike Appold
#
# - Implements random algorithm to generate a solution for the Amstelhaege 
# case.
#
###############################################################################

import random
import copy


def random_empty_coordinate(grid):
		"""
		Returns a random empty coordinate from grid.
		"""

		random_coordinate = random.choice(grid.all_empty_coordinates)

		return random_coordinate


def random_rotation():
		"""
		Returns a random rotation.
		"""

		rotation = ["horizontal", "vertical"]
		random_rotation = random.choice(rotation)

		return random_rotation


class Randomize():
	def __init__(self, grid):
		self.grid = grid
		self.best_grid = None
		self.best_value = 0 
		self.all_values = []

	def random_assignment(self, grid):
		"""
		Places all houses randomly on grid. Returns the new grid.
		"""

		# Copy empty grid 
		copy_grid = copy.deepcopy(grid)
		houses = copy_grid.all_houses
		
		# Try to place all houses on grid at valid location
		for house in houses:
			
			print(f"Trying to place: {house}")

			while house.placed == False:

					# Pick random cell
					random_cell = random_empty_coordinate(copy_grid)

					# Calculate all coordinates for random cell and random rotation
					house.calc_all_coordinates(random_cell, rotation="random")

					# Check if location is valid
					if house.valid_location(copy_grid):
						print("Valid location")

						# Assign house to grid
						copy_grid.assignment_house(house)

					else:
						print("Invalid location, retry")

		print("All houses placed succesfully")

		return copy_grid

	def check_solution(self, grid):
		"""
		Checks if value of new grid is higher than current highest value.
		If so, current best grid and value are replaced by new grid and value.
		"""

		new_value = grid.value
		old_value = self.best_value

		if new_value > old_value:
			self.best_grid = grid
			self.best_value = new_value

	def run(self, iterations):
		"""
		Runs randomize for a specifc amount of iterations.
		"""

		for i in range(0, iterations):
			# Randomly assign grid and calculate worth
			random_grid = self.random_assignment(self.grid)
			random_grid.calculate_worth()

			print(f"RANDOMIZE ITERATION {i}: {random_grid.value}")
			
			# Add value to all_values and check if value is higher than current highest value
			self.all_values.append(random_grid.value)
			self.check_solution(random_grid)