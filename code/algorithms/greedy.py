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
		first_house = copy_grid.all_houses.pop(0)

		# Place house on random valid spot on grid
		while first_house.placed == False:
			random_empty_coordinate = rz.random_empty_coordinate(copy_grid)

			rotation = rz.random_rotation()
			
			# Define house coordinates based on randomly picked coordinate
			first_house.outer_house_coordinates = first_house.calc_house_coordinates(random_empty_coordinate, rotation)
			first_house.outer_man_free_coordinates = first_house.calc_man_free_coordinates(first_house.outer_house_coordinates)
			
			# Check if location is valid
			if first_house.valid_location(copy_grid):
				copy_grid.assignment_house(first_house)
				first_house.placed = True
			
		return copy_grid

	def run(self):
		
		# Place first house
		copy_grid = self.place_first_house()

		highest_value = copy_grid.calculate_worth()

		# For each house, find location that adds most value to map
		for house in copy_grid.all_houses:
			print(house)
			counter = 0
			for starting_coordinate in copy_grid.all_empty_coordinates:
				print(starting_coordinate)
				counter += 1
				print(counter)
				rotation = rz.random_rotation()

				# Define potential coordinates based on starting coordinate
				house.outer_house_coordinates = house.calc_house_coordinates(starting_coordinate, rotation)
				house.outer_man_free_coordinates = house.calc_man_free_coordinates(house.outer_house_coordinates)
				
				if house.valid_location(copy_grid) and copy_grid.calculate_worth() > highest_value:
					# Save house with (preliminary) best coordinates
					greedy_house = house 
					highest_value = copy_grid.calculate_worth()
			
			# Place house that 
			print("Made it outside inner for loop")
			copy_grid.assignment_house(greedy_house)
			greedy_house.placed = True
		
		return copy_grid