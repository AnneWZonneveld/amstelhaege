from code.classes import grid, house 
from code.visualization import visualize as vis
from code.algorithms import randomize as rz
from code.algorithms import greedy as gr
from code.algorithms import hillclimber as hc

from statistics import mean 

if __name__ == "__main__":

	quantity = 20
	map_source = "data/wijken/wijk_1.csv"

	# Create grid from data
	test_grid = grid.Grid(quantity, map_source)

	# ----------------------- Randomize algorithm ---------------------------------
	print("PERFORMING RANDOMIZE")

	randomize = rz.Randomize(test_grid)

	randomize.run(iterations=10)

	#Visualize best case
	vis.visualize(randomize.best_grid)

	# Visualize histogram
	vis.hist_plot(randomize.all_values, "randomize_histogram")

	#Create csv output file best case
	randomize.best_grid.create_output()

	# Determine highest value and mean
	print(f"HIGHEST RANDOMIZE VALUE: {randomize.best_value}")
	print(f"MEAN RANDOMIZE VALUE: {mean(randomize.all_values)}")


	# ------------------------ Greedy algorithm -----------------------------------
	# greedy = gr.Greedy(test_grid)
	# greedy.run()

	# # Value of grid 
	# print(f"Value greedy config: {greedy.value}")

	# # Visualize case
	# vis.visualize(greedy.grid)

	# # # Create csv output file
	# greedy.grid.create_output()

	# ------------------------- Hill Climber algortihm ------------------------------
	print("PERFORMING HC")

	hillclimber = hc.HillClimber(randomize.best_grid)
	hillclimber.run(iterations=30)

	# Value of grid
	print(f"HILLCLIMBER VALUE: {hillclimber.value}")

	# Visualize case
	vis.visualize(hillclimber.grid)

	# Visualize iterations
	vis.iteration_plot(hillclimber.all_values, "hillclimber_plot")

	# Create csv output file
	hillclimber.grid.create_output()






