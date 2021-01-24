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
		self.value = 0

	def place_first_house(self):
		""" 
		Places first house on a random valid location on grid copy and
		returns updated grid copy. 
		"""
		print("Placing first house")

		copy_grid = copy.deepcopy(self.grid)

		# Retrieve first house
		first_house = copy_grid.all_houses[0]

		# Place house on random valid spot on grid
		while first_house.placed == False:
			random_empty_coordinate = (rz.random_empty_coordinate(copy_grid))
		
			rotation = rz.random_rotation()
			
			# Define house coordinates based on randomly picked coordinate			
			first_house.calc_all_coordinates(random_empty_coordinate,rotation)

			# Check if location is valid
			if first_house.valid_location(copy_grid):
				print("Valid location")
				copy_grid.assignment_house(first_house)
				first_house.placed = True
	
		return copy_grid


	def check_solution(self, new_grid, house):

		new_value = new_grid.calculate_worth()
		old_value = self.value

		if new_value > old_value:
			print("FOUND NEW BEST VALUE")
			greedy_house = copy.deepcopy(new_grid)
			self.value = new_value


	def run(self):
		
		# Randomly place first house on map
		copy_grid = self.place_first_house()
		
		highest_value = 0

		spare_houses = copy_grid.all_houses[1:]

		# For each remaining house, find location that adds most value to map
		for i in range(0, len(spare_houses)):
			house = spare_houses[i]
			counter = 1

			for starting_coordinate in copy_grid.all_empty_coordinates:
				print(f"Try {counter} for {house}")
				counter += 1
				
				# Set house coordinates
				house.calc_all_coordinates(starting_coordinates, rotation="random")
				
				if house.valid_location(copy_grid):
					print("Valid location")
					# Preliminary assignment of house
					copy_grid.assignment_house(house)

					# Check solution
					greedy_house = self.check_solution(copy_grid, house)

					# new_worth = copy_grid.calculate_worth()
				
					# if new_worth > highest_value:

					# 	# Save house with (preliminary) best coordinates
					# 	greedy_house = copy.deepcopy(house)
					# 	highest_value = new_worth
					# 	print(f"New highest value: {highest_value}")
					
					copy_grid.undo_assignment_house(house)
			
			# Place house with best location
			copy_grid.assignment_house(greedy_house)
			copy_grid.all_houses[i + 1] = greedy_house
		
		self.value = highest_value
		self.grid = copy_grid