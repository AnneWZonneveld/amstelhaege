import copy
import random

# Tools
from IPython import embed
from code.visualization import visualize as vis


class HillClimber:
	def __init__(self, grid):
		self.grid = copy.deepcopy(grid)
		self.value = self.grid.value
		self.all_values = []

	def switch_house(self, grid):
		"""
		Switches two houses of different types if possible
		"""

		# Pick random house
		house_1 = random.choice(grid.all_houses)
		different_houses = [house for house in grid.all_houses if house.type != house_1.type]
		house_2 = random.choice(different_houses)


		houses = [house_1, house_2]

		info_house_1 = {
			"outer_house_coordinates": house_1.outer_house_coordinates,
			"outer_man_free_coordinates": house_1.outer_man_free_coordinates,
			"house_coordinates": house_1.house_coordinates,
			"man_free_coordinats": house_1.man_free_coordinates,
			"rotation": house_1.rotation
		}

		# Retrieve list of all houses of different type and pick random one
		info_house_2 = {
			"outer_house_coordinates": house_2.outer_house_coordinates,
			"outer_man_free_coordinates": house_2.outer_man_free_coordinates,
			"house_coordinates": house_2.house_coordinates,
			"man_free_coordinats": house_2.man_free_coordinates,
			"rotation": house_1.rotation
		}

		# Remove houses from map and set new coordinates
		grid.undo_assignment_house(house_1)
		grid.undo_assignment_house(house_2)

		house_1_top_left = house_1.outer_house_coordinates['top_left']
		house_2_top_left = house_2.outer_house_coordinates['top_left']
		house_1_rotation = house_1.rotation
		house_2_rotation = house_2.rotation

		house_1.calc_all_coordinates(house_2_top_left, house_2_rotation)
		house_2.calc_all_coordinates(house_1_top_left, house_1_rotation)

		# Check if new locations are valid
		if house_1.valid_location(grid) and house_2.valid_location(grid):
			print("Switched houses")

			# Assign houses to new location on grid
			grid.assignment_house(house_1)
			grid.assignment_house(house_2)

			succes = True

		else:
			house_1.outer_house_coordinates = info_house_1['outer_house_coordinates']
			house_1.outer_man_free_coordinates = info_house_1['outer_man_free_coordinates']
			house_1.house_coordinates = info_house_1['house_coordinates']
			house_1.man_free_coordinats = info_house_1['man_free_coordinats']

			house_2.outer_house_coordinates = info_house_2['outer_house_coordinates']
			house_2.outer_man_free_coordinates = info_house_2['outer_man_free_coordinates']
			house_2.house_coordinates = info_house_2['house_coordinates']
			house_2.man_free_coordinats = info_house_2['man_free_coordinats']

			# Assign houses to new location on grid
			grid.assignment_house(house_1)
			grid.assignment_house(house_2)

			succes = False

		return succes


	def rotate_house(self, grid):
		"""
		Rotates house if possible.

		- pick random house
		- check rotation
		- set rotation to opposite value
		- calculate new possible coordinates
		- see if possible
		- if possible, set original cells to empty and then new cells to House
		"""

		success = False

		while success == False:

			# Pick random house
			house = random.choice(grid.all_houses)
			house_starting_xy = house.outer_house_coordinates['top_left']

			# Save current coordinates
			old_outer_house_coordinates = house.outer_house_coordinates
			old_outer_man_free_coordinates = house.outer_man_free_coordinates

			# Check rotation and calculate new outer house coordinates
			if house.rotation == "horizontal":
				house.outer_house_coordinates = house.calc_house_coordinates(house_starting_xy, "vertical")

			elif house.rotation == "vertical":
				house.outer_house_coordinates = house.calc_house_coordinates(house_starting_xy, "horizontal")

			# Calculate new outer mandatory free space coordinates
			house.outer_man_free_coordinates = house.calc_mandatory_free_space_coordinates(house.outer_house_coordinates)

			# Check if house can be placed on these coordinates 
			if house.valid_location(grid):
				# Undo the old assignment
				grid.undo_assignment_house(house)
				# Do the new assignment
				grid.assignment_house(house)
				success = True
			else:
				print("Could not rotate this house, retry")

				# Set outer house coordinates back to old values
				house.outer_house_coordinates = old_outer_house_coordinates
				house.outer_man_free_coordinates = old_outer_man_free_coordinates

	def mutate_grid(self, grid, hc_type, nr_houses=1): # type: switch or rotation
		"""
		Depending on hc_type, this function performs a switch or rotates a house
		for nr_houses. 
		"""

		# Misschien nr-houses weghalen, overbodig en incompatible met succes boolean

		if hc_type == "switch":
			for _ in range(nr_houses):	
				succes = self.switch_house(grid)
		elif hc_type == "rotation":
			for _ in range(nr_houses):
				succes = self.rotate_house(grid)

		return succes 

	def check_solution(self, new_grid):

		new_value = new_grid.calculate_worth()
		old_value = self.value

		if new_value > old_value:
			print("FOUND NEW BEST VALUE")
			self.grid = new_grid
			self.value = new_value


	def run(self, iterations, hc_type="switch", mutate_nr_houses=1):

		self.iterations = iterations

		for iteration in range(iterations):

			print(f'Iteration {iteration}/{iterations}, current value: {self.value}')

			new_grid = copy.deepcopy(self.grid)

			succes = self.mutate_grid(new_grid, hc_type)

			if succes:

				# Add solution to all solutions
				self.all_values.append(new_grid.value)

				# Check if new solution is better 
				self.check_solution(new_grid)
