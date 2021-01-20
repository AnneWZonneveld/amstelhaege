
class Cell():
	def __init__(self, x_coordinate, y_coordinate):
		self.x_coordinate = x_coordinate
		self.y_coordinate = y_coordinate
		self.type = None

	def occupied_by_house(self):
		"""
		Designates cells on which any type of apartment is placed as occupied 
		by a house.
		"""
		if self.type in ['maison', 'bungalow', 'single']:
			return True
		else:
			return False
   
	def __repr__(self):
		"""
		Make sure that the object is printed properly if it is in a list/dict.
		"""
		return f" ({self.x_coordinate}, {self.y_coordinate}: {self.type})"    