from code.algorithms import randomize as rz
from IPython import embed
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

		if self.type == "single":
			self.width = 8
			self.depth = 8
			self.price = 285000
			self.min_free = 2
			self.percentage = 0.03
		elif self.type == "bungalow":
			self.width = 11
			self.depth = 7
			self.price = 399000
			self.min_free = 3
			self.percentage = 0.04
		else:
			self.width = 12
			self.depth = 10
			self.price = 610000
			self.min_free = 6
			self.percentage = 0.06

	def load_coordinates(self, coordinates):
		object_coordinates = []

		for column in range(coordinates['top_left'][1], coordinates['bottom_right'][1]):
			for row in range(coordinates['top_left'][0], coordinates['bottom_right'][0]):
				current_coordinate = (row, column)
				object_coordinates.append(current_coordinate)

		return object_coordinates 

	def calc_all_coordinates(self, coordinates, rotation):
		self.outer_house_coordinates = self.calc_house_coordinates(coordinates, rotation)
		self.outer_man_free_coordinates = self.calc_man_free_coordinates(self.outer_house_coordinates)
		
		# Retrieve all coordinates of house
		self.house_coordinates = self.load_coordinates(self.outer_house_coordinates) 
		self.man_free_coordinates = list(set(self.load_coordinates(self.outer_man_free_coordinates)) - set(self.house_coordinates))


	def calc_house_coordinates(self, cell_coordinates, rotation):
		"""
		Returns a dictionary of house coordinates (excluding mandatory free space).
		"""

		# Pick random rotation
		if rotation == "random":
			#self.rotation = random_algorithm.random_rotation_choice()
			rotation = ['horizontal', 'vertical']
			self.rotation = random.choice(rotation)

		# Assign according width and depth
		if rotation == "horizontal":
			self.rotation = 'horizontal'
			width = self.width
			depth = self.depth
		else:
			self.rotation = 'vertical'
			width = self.depth
			depth = self.width

		cell_x = cell_coordinates[0]
		cell_y = cell_coordinates[1]

		house_coordinates = {
			'bottom_left': (cell_x, cell_y + depth), 
			'bottom_right': (cell_x + width, cell_y + depth), 
			'top_left': (cell_x, cell_y),
			'top_right': (cell_x + width, cell_y)
			}
		
		return house_coordinates

	def calc_man_free_coordinates(self, house_coordinates):
		"""
		Returns a dictionary of house coordinates (including mandatory free space).
		"""

		coordinates_mandatory_free_space = {
			'bottom_left': (house_coordinates['bottom_left'][0] - self.min_free, house_coordinates['bottom_left'][1] + self.min_free), 
			'bottom_right': (house_coordinates['bottom_right'][0] + self.min_free, house_coordinates['bottom_right'][1] + self.min_free), 
			'top_left': (house_coordinates['top_left'][0] - self.min_free, house_coordinates['top_left'][1] - self.min_free),
			'top_right': (house_coordinates['top_right'][0] + self.min_free, house_coordinates['top_right'][1] - self.min_free)
			}

		return coordinates_mandatory_free_space

	def valid_location(self, grid):

		# embed()

		valid = True

		# Check if coordinates fall within grid 
		for coordinate in self.outer_man_free_coordinates.values():
			if coordinate[0] > grid.width or coordinate[0] < 0:
				valid = False
				return valid
			elif coordinate[1] > grid.depth or coordinate[1] < 0:
				valid = False
				return valid 

		# Location of water, house or man free space other hous unavailable to place house
		not_available = [grid.all_water_coordinates, grid.all_house_coordinates, grid.all_man_free_coordinates]
		
		# Check for every house coordinate if not water or other house
		for coordinate in self.house_coordinates:

			if any(coordinate in sublist for sublist in not_available):
				valid = False

		return valid


	def __repr__(self):
		"""
		Make sure that the object is printed properly if it is in a list/dict.
		"""
		return f"(House {self.id}, {self.type})"