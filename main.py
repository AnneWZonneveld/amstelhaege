from code.classes import grid, house 
from code.visualization import visualize as vis
from code.algorithms import randomize as rz
from code.algorithms import greedy as gr
from code.algorithms import hillclimber as hc

from statistics import mean 

if __name__ == "__main__":

	quantity = 20
	map_name = "wijk_3"
	map_source = f"data/wijken/{map_name}.csv"

	# Create grid from data
	test_grid = grid.Grid(quantity, map_source)

	# ----------------------- Randomize algorithm ---------------------------------
	print("PERFORMING RANDOMIZE")

	randomize = rz.Randomize(test_grid)

	randomize.run(iterations=1)

	#Visualize best case
	vis.visualize(randomize.best_grid, map_name, quantity, "randomize")

	# Visualize histogram
	vis.hist_plot(randomize.all_values, map_name, quantity, "randomize")

	# Create csv output file best case
	randomize.best_grid.create_output(map_name, quantity, "randomize") 

	# Determine highest value and mean
	print(f"HIGHEST RANDOMIZE VALUE: {randomize.best_value}")
	# print(f"MEAN RANDOMIZE VALUE: {mean(randomize.all_values)}")


	# ------------------------ Greedy algorithm -----------------------------------
	#greedy = gr.Greedy(test_grid)
	#greedy.run(gr_type="random")

	# # Value of grid 
	#print(f"Value greedy config: {greedy.value}")

	# # Visualize case
	# vis.visualize(greedy.grid, map, quantity, "greedy")

	# # Create csv output file
	#greedy.grid.create_output("greedy")

	# ------------------------- Hill Climber algorithm ------------------------------
	# print("PERFORMING HC")
	# start_state = "randomize" # randomize or greedy

	# # ------------------------------- SWITCH -----------------------------------------
	# hillclimber = hc.HillClimber(randomize.best_grid)

	# hc_type = "switch"
	# hillclimber.run(iterations=2000, hc_type=hc_type)

	# # Value of grid
	# print(f"HILLCLIMBER VALUE: {hillclimber.value}")

	# # Visualize case
	# vis.visualize(hillclimber.grid, map_name, quantity, f"{start_state}_hillclimber_{hc_type}")

	# # Visualize iterations
	# vis.iteration_plot(hillclimber.all_values, map_name, quantity, hc_type, start_state)

	# # Create csv output file
	# hillclimber.grid.create_output(map_name, quantity, f"{start_state}_hillclimber_{hc_type}") 

	# # ---------------------------------- ROTATION --------------------------------------
	# hillclimber = hc.HillClimber(randomize.best_grid)

	# hc_type = "rotation"
	# hillclimber.run(iterations=2000, hc_type=hc_type)

	# # Value of grid
	# print(f"HILLCLIMBER VALUE: {hillclimber.value}")

	# # Visualize case
	# vis.visualize(hillclimber.grid, map_name, quantity, f"{start_state}_hillclimber_{hc_type}")

	# # Visualize iterations
	# vis.iteration_plot(hillclimber.all_values, map_name, quantity, hc_type, start_state)

	# # Create csv output file
	# hillclimber.grid.create_output(map_name, quantity, f"{start_state}_hillclimber_{hc_type}") 

	# print(f"MEAN RANDOMIZE VALUE: {mean(randomize.all_values)}")


