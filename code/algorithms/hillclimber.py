import copy
import random


class HillClimber:
	def __init__(self, grid):
		self.grid = copy.deepcopy(grid)
		self.value = grid.calculate_worth()


	def switch_house(self, grid):
		pass 


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

	def mutate_grid(self, grid, hc_type, nr_houses=1): # type: switch or rotation?
	    """
        Depending on hc_type, this function performs a switch or rotates a house
        for nr_houses. 
        """

		if hc_type = "switch":
			for _ in range(nr_houses):
            	self.switch_house(grid)
		elif hc_type = "rotation":
			for _ in range(nr_houses):
            	self.rotate_house(grid)
		else:
			# Error


	def run(self, iterations, hc_type="switch", mutate_nr_houses=1):

		self.iterations = iterations

		for interation in range(iterations):

			print(f'Iteration {iteration}/{iterations}, current value: {self.value}')

			new_grid = copy.deepcopy(self.grid)

			self.mutate_grid(new_grid, "switch")

			# Make changes to grid --> 
			# - switch two random houses of different types
			# - rotate certain house

			# Check if new solution is better 


