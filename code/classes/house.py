###############################################################################
# house.py
#
# Programmeertheorie
# Anne Zonneveld, Fleur Tervoort, Seike Appold
#
# - A class to create House instances.
###############################################################################


from code.algorithms import randomize as rz
from code.constants import *
import random


class House():
	def __init__(self, type, id):
		self.type = type
		self.id = id
		self.outer_house_coordinates = None
		self.outer_man_free_coordinates = None
		self.house_coordinates =[]
		self.man_free_coordinates = []
		self.extra_free = 0
		self.rotation = None
		self.placed = False
		self.rotation =  None

		if self.type == "single":
			self.width = SINGLE_WIDTH
			self.depth = SINGLE_DEPTH
			self.price = SINGLE_PRICE
			self.min_free = SINGLE_MIN_FREE
			self.percentage = SINGLE_PERC

		elif self.type == "bungalow":
			self.width = BUNGALOW_WIDTH
			self.depth = BUNGALOW_DEPTH
			self.price = BUNGALOW_PRICE
			self.min_free = BUNGALOW_MIN_FREE
			self.percentage = BUNGALOW_PERC

		else:
			self.width = MAISON_WIDTH
			self.depth = MAISON_DEPTH
			self.price = MAISON_PRICE
			self.min_free = MAISON_MIN_FREE
			self.percentage = MAISON_PERC


	def load_coordinates(self, coordinates):
		"""
		Returns a list of all coordinates based on a dictionary with the four 
		outer coordinates. 
		"""

		object_coordinates = []

		for column in range(coordinates["top_left"][1], coordinates["bottom_right"][1]):

			for row in range(coordinates["top_left"][0], coordinates["bottom_right"][0]):
				current_coordinate = (row, column)
				object_coordinates.append(current_coordinate)

		return object_coordinates 


	def calc_all_coordinates(self, coordinates, rotation):
		"""
		Calculates all coordinates of house and assigns them to the house.
		"""

		# Retrieve outer coordinates of house
		self.outer_house_coordinates = self.calc_house_coordinates(coordinates, rotation)
		self.outer_man_free_coordinates = self.calc_man_free_coordinates(self.outer_house_coordinates)
		
		# Retrieve all coordinates of house
		self.house_coordinates = self.load_coordinates(self.outer_house_coordinates) 
		self.man_free_coordinates = list(set(self.load_coordinates(self.outer_man_free_coordinates)) - set(self.house_coordinates))


	def calc_house_coordinates(self, coordinates, rotation):
		"""
		Returns a dictionary of house coordinates (excluding mandatory free space).
		"""

		# Pick random rotation
		if rotation == "random":
			rotation = rz.random_rotation()

		# Assign according width and depth
		if rotation == "horizontal":
			self.rotation = "horizontal"
			width = self.width
			depth = self.depth

		else:
			self.rotation = "vertical"
			width = self.depth
			depth = self.width

		coordinate_x = coordinates[0]
		coordinate_y = coordinates[1]

		# Define house coordinates
		house_coordinates = {
			"bottom_left": (coordinate_x, coordinate_y + depth), 
			"bottom_right": (coordinate_x + width, coordinate_y + depth), 
			"top_left": (coordinate_x, coordinate_y),
			"top_right": (coordinate_x + width, coordinate_y)
			}
		
		return house_coordinates


	def calc_man_free_coordinates(self, house_coordinates):
		"""
		Returns a dictionary of house coordinates (including mandatory free space).
		"""

		coordinates_mandatory_free_space = {
			"bottom_left": (house_coordinates["bottom_left"][0] - self.min_free, house_coordinates["bottom_left"][1] + self.min_free), 
			"bottom_right": (house_coordinates["bottom_right"][0] + self.min_free, house_coordinates["bottom_right"][1] + self.min_free), 
			"top_left": (house_coordinates["top_left"][0] - self.min_free, house_coordinates["top_left"][1] - self.min_free),
			"top_right": (house_coordinates["top_right"][0] + self.min_free, house_coordinates["top_right"][1] - self.min_free)
			}

		return coordinates_mandatory_free_space


	def valid_location(self, grid):
		"""
		Checks if coordinates of house are located within the grid, but not on 
		water, on another house, or on the mandatory free space of another 
		house. Returns True or False.
		"""

		valid = True

		# Check if coordinates fall within grid 
		for coordinate in self.outer_man_free_coordinates.values():

			if coordinate[0] > grid.width or coordinate[0] < 0:
				valid = False
				return valid

			elif coordinate[1] > grid.depth or coordinate[1] < 0:
				valid = False
				return valid 

		# Location of water, house or mandatory free space other house, unavailable to place house
		not_available = [grid.all_water_coordinates, grid.all_house_coordinates, grid.all_man_free_coordinates]
		
		# Check for every house coordinate if available
		for coordinate in self.house_coordinates:
			
			if any(coordinate in sublist for sublist in not_available):
				valid = False

		return valid


	def __repr__(self):
		"""
		Make sure that the object is printed properly if it is in a list/dict.
		"""

		return f"(House {self.id}, {self.type})"