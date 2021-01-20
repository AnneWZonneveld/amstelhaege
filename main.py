from code.classes import grid, house 
from code.visualization import visualize as vis
from code.algorithms import randomize as rz
from code.algorithms import greedy as gr


if __name__ == "__main__":

	quantity = 20
	map_source = "data/wijken/wijk_3.csv"

	# Create grid from data
	test_grid = grid.Grid(quantity, map_source)

	# ----------------------- Randomize algorithm ---------------------------------
	random_config = rz.random_assignment(test_grid)
	random_config.calculate_worth()

	Value of grid
	print(f"Value random config: {random_config.value}")

	# Visualize case
	vis.visualize(random_config)

	# Create csv output file
	random_config.create_output()

	# ------------------------ Greedy algorithm -----------------------------------
	# greedy = gr.Greedy(test_grid)
	# greedy.run()

	# # Value of grid 
	# print(f"Value greedy config: {greedy.value}")

	# # Visualize case
	# vis.visualize(greedy.grid)

	# # Create csv output file
	# greedy.graph.create_output()



