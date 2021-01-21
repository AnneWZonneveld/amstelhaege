"""
	Pseudocode
	- Place first house randomly
	- Repeat until no houses left
		- Draw a house from list
		- For each valid location of the house
			- If new worth of map > current worth of map
				- Save location as best solution
		- Place house at location of best solution
"""

import copy, random
import code.algorithms.randomize as rz
from code.visualization import visualize as vis

# Tools
from IPython import embed; 

class Greedy():
	"""
	Greedy class that assigns the best possible location (that results 
	in highest map value) for a house one by one.
	"""

	def __init__(self, grid):
		self.grid = grid

	def place_first_house(self):
		""" 
		Places first house on a random valid location on grid copy and
		returns updated grid copy. 
		"""

		copy_grid = copy.deepcopy(self.grid)

		# Retrieve first house
		first_house = copy_grid.all_houses_list.pop(0)

		# Place house on grid
		while house.placed = False:
			random_empty_coordinate = rz.random_empty_coordinate(copy_grid, first_house)
			copy_grid.assignment_house(first_house, random_empty_coordinate)
			
			# Check if location is valid
			if house.valid_location(copy_grid):
				first_house.placed = True
			
		return copy_grid

	def run(self):
		
		# Place first house
		copy_grid = self.place_first_house()

		highest_value = copy_grid.calculate_worth()

		# For each house, find location that adds most value to map
		for house in copy_grid.all_houses:
			for starting_coordinate in copy_grid.empty_coordinates:

				# HOW TO ADDRESS ROTATION?
				rotation = random_rotation()

				# Define potential coordinates based on starting coordinate
				house.outer_house_coordinates = house.calc_house_coordinates(starting_coordinate, rotation)
				house.outer_man_free_coordinates = house.calc_man_free_coordinates(house.outer_house_coordinates)

				if house.valid_location(copy_grid) and copy_grid.calculate_worth() > highest_value:
					print("Update greedy house and highest value")
					# Save house with (preliminary) best coordinates
					greedy_house = house 
					highest_value = copy_grid.calculate_worth()
			
			# Place house that 
			copy_grid.assignment_house(greedy_house)
			greedy_house.placed = True
		
		return copy_grid