import copy, random
from code.algorithms import randomize as rz 
from code.visualization import visualize as vis

# Tools
from IPython import embed; 

class Greedy():
	"""
	Greedy class that places houses one after another. It assigns the
	first house randomly. For each subsequent house, it chooses the
	location that adds most value to the map (i.e. local optimum).
	"""

	def __init__(self, grid):
		self.grid = grid
		self.value = 0

	def place_first_house_randomly(self):
		""" 
		Places first house on a random valid location on grid copy and
		returns updated grid copy. 
		"""
		copy_grid = copy.deepcopy(self.grid)
		random = rz.Randomize(copy_grid)

		# Randomly pick first house
		first_house = copy_grid.all_houses[0]

		# Place house on random valid spot on grid
		while first_house.placed == False:
			# Define house coordinates based on randomly picked rotation and top left corner
			random_empty_coordinate = random.random_empty_coordinate(copy_grid)
			rotation = random.random_rotation()			
			first_house.calc_all_coordinates(random_empty_coordinate, rotation)

			# If location is valid, place house
			if first_house.valid_location(copy_grid):
				print("Valid location")
				copy_grid.assignment_house(first_house)
	
		return copy_grid

	def place_first_house_strategically(self):
		"""
		Places first house in one of the corners of the map if possible,
		else randomly. Places the biggest type of house first. Returns
		updated grid copy.
		"""
		
		copy_grid = copy.deepcopy(self.grid)

		# Pick one of the biggest houses first
		first_house = copy_grid.all_houses[0]
		
		# For each corner of the map, define coordinates of top left corner of house
		bl_corner = (first_house.min_free, copy_grid.depth - first_house.depth - first_house.min_free)
		tl_corner = (first_house.min_free, first_house.min_free + first_house.depth)
		br_corner = (copy_grid.width - first_house.width - first_house.min_free, copy_grid.depth - first_house.depth - first_house.min_free)
		tr_corner = (copy_grid.width - first_house.width - first_house.min_free, first_house.min_free)

		corner_coordinates = [bl_corner, tl_corner, br_corner, tr_corner]
		
		# Place house in one of the corners of the map if possible
		for coordinate in corner_coordinates:

			first_house.calc_all_coordinates(coordinate, "horizontal")

			# Check if location is valid
			if first_house.valid_location(copy_grid):
				print("Valid location")
				copy_grid.assignment_house(first_house)
				break
		
		# Place house randomly if it cannot be placed in one of the corners
		if first_house.placed == False:
			copy_grid = self.place_first_house_randomly()
	
		return copy_grid

	def check_solution(self, new_grid):
		"""
		Returns true if current placement of house on new_grid adds more
		value to map than all previously tested locations, else false.
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
		Runs greedy algortihm. Depending on "gr_type" first house is either
		placed randomly or strategically based on heuristics. Each remaining 
		house is placed at the location that adds most value to the map.
		"""
		
		if gr_type == "random":
			# Randomly place first house on map
			copy_grid = self.place_first_house_randomly()
		elif gr_type == "strategy":
			# Place first house based on heuristics
			copy_grid = self.place_first_house_strategically()
		
		print("Placed first house")

		spare_houses = copy_grid.all_houses[1:]

		# For each remaining house, find location that adds most value to map
		for house_nr in range(len(spare_houses)):
			house = spare_houses[house_nr]
			counter = 1

			for starting_coordinate in copy_grid.all_empty_coordinates:
				print(f"Try {counter} for {house}")
				counter += 1
				
				# Set house coordinates
				house.calc_all_coordinates(starting_coordinate, rotation="random")
				
				if house.valid_location(copy_grid):
					print("Valid location")
					# Preliminary assignment of house
					copy_grid.assignment_house(house)
					
					# Save location if it adds more value than previous locations
					if self.check_solution(copy_grid):
						best_coordinate = starting_coordinate
						best_rotation = house.rotation
					
					# Undo assignment of house to test further locations
					copy_grid.undo_assignment_house(house)
			
			# Permanently place house at location that yielded most value
			house.calc_all_coordinates(best_coordinate, rotation=best_rotation)
			copy_grid.assignment_house(house)
			copy_grid.all_houses[house_nr + 1] = house
		
		self.grid = copy_grid
		