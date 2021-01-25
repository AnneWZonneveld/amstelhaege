import random
import copy

# Tools
from IPython import embed
from code.visualization import visualize as vis

class Randomize():
	def __init__(self, grid):
		self.grid = grid
		self.best_grid = None
		self.best_value = 0 
		self.all_values = []

	def random_empty_coordinate(self, grid):
		"""
		Returns a random empty coordinate from grid.
		"""

		random_coordinate = random.choice(grid.all_empty_coordinates)

		return random_coordinate


	def random_rotation(self):
		"""
		Returns a random rotation.
		"""

		rotation = ['horizontal', 'vertical']
		random_rotation = random.choice(rotation)

		return random_rotation


	def random_assignment(self, grid):
		"""
		Places all houses randomly on grid. Returns the new grid.
		"""

		# Copy empty grid 
		copy_grid = copy.deepcopy(grid)
		houses = copy_grid.all_houses
		
		# Try to place all houses on grid at valid location
		for house in houses:
			
			# embed()

			print(f"Trying to place: {house}")

			while house.placed == False:

					random_cell = self.random_empty_coordinate(copy_grid)
					
					rotation = self.random_rotation()

					house.calc_all_coordinates(random_cell, rotation)

					if house.valid_location(copy_grid):
						print("Valid location")

						#Assign house to grid
						copy_grid.assignment_house(house)

					else:
						print("Invalid location, retry")

		print("All houses placed succesfully")

		return copy_grid

	def check_solution(self, grid):
		new_value = grid.value
		old_value = self.best_value

		if new_value > old_value:
			self.best_grid = grid
			self.best_value = new_value

	def run(self, iterations):

		for i in range(0, iterations):

			random_grid = self.random_assignment(self.grid)
			random_grid.calculate_worth()

			#Value of grid
			print(f"RANDOMIZE ITERATION {i}: {random_grid.value}")

			self.all_values.append(random_grid.value)

			self.check_solution(random_grid)


