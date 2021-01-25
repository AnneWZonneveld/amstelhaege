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

	def place_first_house(self):
		""" 
		Places first house on a random valid location on grid copy and
		returns updated grid copy. 
		"""
		copy_grid = copy.deepcopy(self.grid)
		random = rz.Randomize(copy_grid)

		# Retrieve first house
		first_house = copy_grid.all_houses[0]

		# Place house on random valid spot on grid
		while first_house.placed == False:
			# Randomly determine bottom left corner and rotation of first house
			random_empty_coordinate = random.random_empty_coordinate(copy_grid)
			rotation = random.random_rotation()
			
			# Define house coordinates based on randomly picked coordinate			
			first_house.calc_all_coordinates(random_empty_coordinate, rotation)

			# Check if location is valid
			if first_house.valid_location(copy_grid):
				print("Valid location")
				copy_grid.assignment_house(first_house)
				first_house.placed = True
	
		return copy_grid


	def check_solution(self, new_grid):
		"""
		Returns true if placement of house on new_grid adds more value
		to map than all previously tested locations, else false.
		"""

		success = False

		new_value = new_grid.calculate_worth()
		old_value = self.value

		if new_value > old_value:
			self.value = new_value
			success = True
			
		return success

	def run(self):
		
		# Randomly place first house on map
		copy_grid = self.place_first_house()
		print("Placed first house")

		spare_houses = copy_grid.all_houses[1:]

		# For each remaining house, find location that adds most value to map
		for i in range(0, len(spare_houses)):
			house = spare_houses[i]
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
					
					# Check solution
					if self.check_solution(copy_grid):
						best_coordinate = starting_coordinate
						best_rotation = house.rotation
					
					copy_grid.undo_assignment_house(house)
			
			# Definite assignment of house at location that yiedl
			house.calc_all_coordinates(best_coordinate, rotation=best_rotation)
			copy_grid.assignment_house(house)
			copy_grid.all_houses[i + 1] = house
		
		self.grid = copy_grid
		