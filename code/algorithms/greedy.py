import copy
import random
import code.algorithms.randomize as rz

# Tools
from IPython import embed; 
from code.visualization import visualize as vis

class Greedy():
	"""
	Greedy class that assigns the best possible location (that results 
	in highest map value) for a house one by one.
	"""

	def __init__(self, grid):
		self.grid = grid


	def place_first_house(self):
		""" 
		Places first house at random location on grid. 
		"""

		copy_grid = copy.deepcopy(self.grid)

		# Retrieve first house 
		first_house = copy_grid.all_houses_list.pop(0)

		# Succesfully place house on grid
		while first_house.placed == False:
			try:
				random_empty_cell = rz.random_empty_cell(copy_grid, first_house)
				first_house_grid = rz.random_assignment_house(copy_grid, first_house, random_empty_cell)
				first_house.placed = True
			except:
				pass

		print("Placed first house")
		return first_house_grid


	def run(self):
		# embed()

		# Place first house
		first_house_grid = self.place_first_house()
		current_grid = first_house_grid

		# Loop through all houses 
		for i in range(0, len(first_house_grid.all_houses_list)):

			# Determine empty cells
			empty_cells = rz.define_empty_cells(current_grid, current_grid.all_houses_list[i])

			# Keep track of all possible states 
			possibilities = []

			# Try placing next house on one of empty cells
			for cell in empty_cells:

				# print(f"current cell: {cell}")

				try:

					# Create new grid for new possible state
					copy_grid = copy.deepcopy(current_grid)

					# Place house on copy grid
					grid = rz.random_assignment_house(copy_grid, copy_grid.all_houses_list[i], cell)
					grid.all_houses_list[i].placed = True

					# Calculate worth of grid and add to possible states
					grid.calculate_worth()
					possibilities.append(grid)

				except:
					print("House could not be placed on this cell")	

			# Determine possible state with highest value --> best_grid list
			highest_value = 0
			for grid in possibilities:
				if grid.value > highest_value:
					highest_value = grid.value
					best_grid = grid

			current_grid = best_grid

			print(f"Placed {best_grid.all_houses_list[i]}")

		self.grid = current_grid








