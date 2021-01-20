import copy
import random


class HillClimber:
	def __init__(self, grid):
		self.grid = copy.deepcopy(grid)
		self.value = grid.calculate_worth()


	def switch_house(self, grid):



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

		# Pick random house
		house = random.choice(grid.all_houses_list)
		house_x = house.coordinates['top_left'][0]
		house_y = house.coordinates['top_left'][1]

		# Check rotation
		if house.rotation == "horizontal":
			house_coordinates = house.calc_house_coordinates(house_x, house_y, "vertical")

		elif house.rotation == "vertical":
			house_coordinates = house.calc_house_coordinates(house_x, house_y, "horizontal")

		house_coordinates_mandatroy_free = house.calc_mandatory_free_space_coordinates(house_coordinates)



		# Determine new coordinates


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


