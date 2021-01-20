from code.algorithms import randomize as rz

class House():
	def __init__(self, type, id):
		self.type = type
		self.id = id
		self.coordinates = None
		self.min_free_coordinates = None
		self.min_free_cells = []
		self.extra_free_cells = []
		self.extra_free = 0
		self.placed = False
		self.rotation =  None

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

	def calc_house_coordinates(self, cell_x, cell_y, rotation):
		"""
		Returns a dictionary of house coordinates (excluding mandatory free space).
		"""

		# Pick random rotation
		if rotation == "random":
			rotation = rz.random_rotation_choice()

		# Assign according width and depth
		if rotation == "horizontal":
			self.rotation = "horizontal"
			width = self.width
			depth = self.depth
		else:
			self.rotation = "vertical"
			width = self.depth
			depth = self.width

		house_coordinates = {
			'bottom_left': (cell_x, cell_y + depth), 
			'bottom_right': (cell_x + width, cell_y + depth), 
			'top_left': (cell_x, cell_y),
			'top_right': (cell_x + width, cell_y)
			}
		
		return house_coordinates

	def calc_mandatory_free_space_coordinates(self, house_coordinates):
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

	def __repr__(self):
		"""
		Make sure that the object is printed properly if it is in a list/dict.
		"""
		return f"(House {self.id}, {self.type})"