from code.classes import grid, house # niet nodig? 
from code.visualization import visualize as vis
from code.algorithms import randomize as rz
from code.algorithms import greedy as gr


if __name__ == "__main__":

	quantity = 20
	map_source = "data/wijken/wijk_3.csv"

	# Create grid from data
	test_grid = grid.Grid(quantity, map_source)

	# ----------------------- Randomize algorithm ---------------------------------
	# random_config = rz.random_assignment(test_grid)

	# # print("New grid:")
	# # print(random_config.cells)

	# # Value of grid
	# print(f"Value random config: {random_config.value}")

	# # Visualize case
	# vis.visualize(random_config)

	# # Create csv output file
	# random_config.create_output()

	# ------------------------ Greedy algorithm -----------------------------------
	greedy = gr.Greedy(test_grid)
	greedy.run()

	# Value of grid 
	print(f"Value greedy config: {greedy.graph.value}")

	# Visualize case
	vis.visualize(greedy.graph)

	# Create csv output file
	greedy.graph.create_output()



