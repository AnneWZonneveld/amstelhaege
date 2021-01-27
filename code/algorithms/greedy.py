################################################################################
# greedy.py
#
# Programmeertheorie
# Anne Zonneveld, Fleur Tervoort, Seike Appold
#
# Implements greedy algorithm to generate a solution for the Amstelhaege case.
#
################################################################################

import copy, random
from code.algorithms import randomize as rz 
from code.visualization import visualize as vis

class Greedy():
	"""
	Places first house either randomly (type: "random") or in one of the corners
	of the map (type: "strategy"). Places each subsequent greedily, by choosing
	the location that renders most valuable map.
	"""

	def __init__(self, grid):
		self.grid = grid
		self.value = 0

	def place_first_house_randomly(self):
		""" 
		Places first house on a random valid location and returns updated copy
		of the grid. 
		"""
		copy_grid = copy.deepcopy(self.grid)

		# Pick a house of the biggest type first (heuristic)
		first_house = copy_grid.all_houses[0]

		# Place house on random valid spot on grid
		while first_house.placed == False:
			# Set potential house coordinates based on random starting coordinate
			starting_coordinate = rz.random_empty_coordinate(copy_grid)		
			first_house.calc_all_coordinates(starting_coordinate, rotation="random")

			# If location is valid, place house
			if first_house.valid_location(copy_grid):
				print("Valid location")
				copy_grid.assignment_house(first_house)
	
		return copy_grid

	def place_first_house_strategically(self):
		"""
		Places first house in one of the corners of the map if possible, else 
		randomly, and returns updated copy of initial grid.
		"""
		
		copy_grid = copy.deepcopy(self.grid)

		# Pick a house of the biggest type first (heuristic)
		first_house = copy_grid.all_houses[0]
		
		# Find starting coordinate to place house horizontally in each map corner
		bl_corner = (first_house.min_free, copy_grid.depth - first_house.depth - first_house.min_free)
		tl_corner = (first_house.min_free, first_house.min_free)
		br_corner = (copy_grid.width - first_house.width - first_house.min_free, copy_grid.depth - first_house.depth - first_house.min_free)
		tr_corner = (copy_grid.width - first_house.width - first_house.min_free, first_house.min_free)
		
		corner_coordinates = [bl_corner, tl_corner, br_corner, tr_corner]
		
		# Place house horizontally in one of the map corners if possible
		for coordinate in corner_coordinates:
			first_house.calc_all_coordinates(coordinate, "horizontal")

			# If location is valid, place house and stop trying corners
			if first_house.valid_location(copy_grid):
				print("Valid location")
				copy_grid.assignment_house(first_house)
				break
		
		# Place house randomly if it could not be placed in one of the corners
		if first_house.placed == False:
			copy_grid = self.place_first_house_randomly()
	
		return copy_grid

	def check_solution(self, new_grid):
		"""
		Returns true if current placement of house adds more value to map than
		all previously tested locations, else false.
		"""

		success = False

		new_value = new_grid.calculate_worth()
		old_value = self.value

		if new_value > old_value:
			self.value = new_value
			success = True
			
		return success

	def run(self, gr_type):
		"""
		Runs greedy algortihm and updates grid based on result.
		"""
		
		# Place first house depening on chosen greedy type
		if gr_type == "random":
			copy_grid = self.place_first_house_randomly()

		elif gr_type == "strategy":
			copy_grid = self.place_first_house_strategically()
		
		spare_houses = copy_grid.all_houses[1:]

		# For each remaining house, find location that adds most value to map
		for house_nr in range(6):
			house = spare_houses[house_nr]
	
			counter_tries = 1
			counter_valid_tries = 0

			# For each unoccupied coordinate, try placing house
			for starting_coordinate in copy_grid.all_empty_coordinates:
				print(f"Try {counter_tries} for {house}")
				counter_tries += 1
				
				# Set potential house coordinates based on starting coordinate
				house.calc_all_coordinates(starting_coordinate, rotation="random")
				
				if house.valid_location(copy_grid):
					print("Valid location")
					counter_valid_tries += 1

					# Assign house preliminarily
					copy_grid.assignment_house(house)
					
					# If first valid location for this house, update grid value
					if counter_valid_tries == 1:
						self.value = copy_grid.calculate_worth()
					
					# Save location if it adds more value than previous locations
					if self.check_solution(copy_grid):
						best_coordinate = starting_coordinate
						best_rotation = house.rotation
					
					# Undo assignment of house to test further locations
					copy_grid.undo_assignment_house(house)
			
			# Permanently place house at location that generated most value
			house.calc_all_coordinates(best_coordinate, rotation=best_rotation)
			copy_grid.assignment_house(house)
			copy_grid.all_houses[house_nr + 1] = house

		self.grid = copy_grid