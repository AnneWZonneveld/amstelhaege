class House():
	def __init__(self, type, id):
		self.type = type
		self.id = id
		self.coordinates = None
		self.min_free_cells = []
		self.extra_free_cells = []
		self.extra_free_meters = 0
		self.placed = False

		if self.type == "single":
			self.width = 8
			self.depth = 8
			self.price = 285000
			self.min_free = 2
			self.percentage = 3
		elif self.type == "bungalow":
			self.width = 11
			self.depth = 7
			self.price = 399000
			self.min_free = 3
			self.percentage = 4
		else:
			self.width = 12
			self.depth = 10
			self.price = 610000
			self.min_free = 6
			self.percentage = 6

	def __repr__(self):
		"""
		Make sure that the object is printed properly if it is in a list/dict.
		"""
		return f"(House {self.id}, {self.type})"