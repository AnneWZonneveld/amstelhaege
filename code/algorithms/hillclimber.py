import copy
import random


class HillClimber:
	def __init__(self, grid):
		self.grid = copy.deepcopy(grid)
		self.value = self.grid.value
		self.all_values = []
		self.conv_count = 0

	def switch_house(self, grid):
		"""
		Switches two random houses of different types if possible. Returns true 
		if succesfully switched. 
		"""

		# Pick random house
		house_1 = random.choice(grid.all_houses)
		different_houses = [house for house in grid.all_houses if house.type != house_1.type]
		house_2 = random.choice(different_houses)

		# Save relevant info
		info_house_1 = {
			"top_left": house_1.outer_house_coordinates['top_left'],
			"rotation": house_1.rotation
		}

		info_house_2 = {
			"top_left": house_2.outer_house_coordinates['top_left'],
			"rotation": house_2.rotation
		}

		# Remove houses from map and set new coordinates
		grid.undo_assignment_house(house_1)
		grid.undo_assignment_house(house_2)

		# Calculate new coordinates
		house_1.calc_all_coordinates(info_house_2['top_left'], info_house_2['rotation'])
		house_2.calc_all_coordinates(info_house_1['top_left'], info_house_1['rotation'])

		# Check if new locations are valid
		if house_1.valid_location(grid) and house_2.valid_location(grid):
			print("Switched houses")

			# Assign houses to new location on grid
			grid.assignment_house(house_1)
			grid.assignment_house(house_2)

			succes = True

		# Switch not possible
		else:

			# Calculate old coordinates
			house_1.calc_all_coordinates(info_house_1['top_left'], info_house_1['rotation'])
			house_2.calc_all_coordinates(info_house_2['top_left'], info_house_2['rotation'])

			# Reassign houses to old location on grid
			grid.assignment_house(house_1)
			grid.assignment_house(house_2)

			succes = False

		return succes


	def rotate_house(self, grid):
		"""
		Rotates house if possible. Returns true if succesfully rotated.
		"""

		# Pick random house
		house = random.choice(grid.all_houses)
		house_starting_xy = house.outer_house_coordinates['top_left']

		# Save relvant inf
		info_house = {
			"top_left": house.outer_house_coordinates['top_left'],
			"rotation": house.rotation
		}

		# Remove house from map and set new coordinates
		grid.undo_assignment_house(house)

		# Check rotation and calculate new outer house coordinates
		if house.rotation == "horizontal":
			house.calc_all_coordinates(house_starting_xy, "vertical")

		elif house.rotation == "vertical":
			house.calc_all_coordinates(house_starting_xy, "horizontal")

		# Check if new location is valid 
		if house.valid_location(grid):
			print("Rotated house")

			# Assign house to new location
			grid.assignment_house(house)
			succes = True

		# Rotation not possible
		else:

			# Calculate old coordinates
			house.calc_all_coordinates(info_house['top_left'], info_house['rotation'])
			
			# Reassign house to old orignal location on grid
			grid.assignment_house(house)

			succes = False

		return succes


	def mutate_grid(self, grid, hc_type, nr_houses=1): 
		"""
		Depending on hc_type, this function performs a nr_houses switches or rotates a house
		for nr_houses. 
		"""

		if hc_type == "switch":
			for _ in range(nr_houses):	
				succes = self.switch_house(grid)
		elif hc_type == "rotation":
			for _ in range(nr_houses):
				succes = self.rotate_house(grid)

		return succes 

	def check_solution(self, new_grid):
		"""
		Checks if value of new grid is higher than current highest value.
		If so, current best grid and value are replaced by new grid and value.
		Also keeps track of the convergence count.
		"""

		new_value = new_grid.calculate_worth()
		old_value = self.value

		if new_value > old_value:
			print("FOUND NEW BEST VALUE")

			# Replace best grid and value 
			self.grid = new_grid
			self.value = new_value

			# Reset convergence count
			self.conv_count = 0

		# No improvement
		else:
			self.conv_count += 1


	def run(self, iterations, hc_type="switch", limit=200, mutate_nr_houses=1):
		"""
		Runs the hill climber algorithm for certain amount of iterations. 
		"""

		self.iterations = iterations

		for iteration in range(iterations):

			# Check for convergence
			if self.conv_count < limit:

				print(f"Iteration {iteration}/{iterations}, current value: {self.value}")
				print(f"Conv counter: {self.conv_count}")

				new_grid = copy.deepcopy(self.grid)

				succes = self.mutate_grid(new_grid, hc_type)

				if succes:

					# Add solution to all solutions
					self.all_values.append(new_grid.value)

					# Check if new solution is better 
					self.check_solution(new_grid)