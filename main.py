import sys, argparse
from code.classes import grid, house 
from code.visualization import visualize as vis
from code.algorithms import randomize as rz
from code.algorithms import greedy as gr
from code.algorithms import hillclimber as hc
from statistics import mean 

def getArgs():
	"""
	Returns command line arguments if they are valid, else issues error.
	Automatically generates help and usage messages.
	"""
	
	parser = argparse.ArgumentParser()
	parser.add_argument('map_name', type = str, choices = ["wijk_1", "wijk_2", "wijk_3"],
						metavar = "map_name", help = "place houses in this neighbourhood (e.g. wijk_1)")
	parser.add_argument('quantity_houses', type = int,
						choices= [20, 40, 60], metavar = "quantity_houses",
						help = "place this amount of houses (e.g. 20)")
	parser.add_argument('algorithm', type = str,
						choices = ["random", "r", "greedy", "gr", "greedy_hill_climber", "gr_hc", "random_hill_climber", "r_hc"],
						metavar = "algorithm", help = "place houses with this algorithm (e.g. random)")
	args = parser.parse_args()

	return args

def implement_random(grid, iterations, map_name, quantity):
	"""
	Runs a specified number of iterations of random algorithm on
	grid for the specified number of times. "Quantity" specifies
	the number of houses to be placed each run and "map_name" the
	underlying map. Returns grid configuration with most value.
	"""
	# Run randomize algorithm on grid as often as user specified
	randomize = rz.Randomize(grid)
	randomize.run(iterations=iterations)

	# Create histogram of all results
	vis.hist_plot(randomize.all_values, map_name, quantity, "randomize")

	# Visualize map and create output file for best result 
	vis.visualize(randomize.best_grid, map_name, quantity, "randomize")
	randomize.best_grid.create_output(map_name, quantity, "randomize")

	return randomize.best_grid
	
def implement_greedy(grid, map_name, quantity, gr_type):
	"""
	Runs greedy algorithm on grid once. "Quantity" specifies the number
	of houses to be placed each run and "map_name" the underlying map.
	Runs strategy or random version of greedy depending on "gr_type".
	"""
	# Run greedy algorithm on grid with type that user specified
	greedy = gr.Greedy(grid)
	greedy.run(gr_type=gr_type)

	# Visualize map and create output file for best result 
	vis.visualize(greedy.grid, map_name, quantity, f"greedy_{gr_type}")
	greedy.grid.create_output(map_name, quantity, f"greedy_{gr_type}")

	return greedy.grid

def implement_hill_climber(grid, map_name, quantity, start_state, hc_type):
	"""
	Runs a specified number of iterations of hillclimber algorithm on
	grid. "Quantity" specifies the number of houses to be placed each
	run and "map_name" the underlying map. Uses random or greedy
	configuration as start state, depending on "start_state". Runs
	switch or rotation version of hilclimber, depending on "gr_type".
	"""
	if start_state == "greedy":
		# Run greedy algorithm on grid with type that user specified
		greedy = gr.Greedy(grid)
		greedy.run(gr_type="strategy")
		starting_grid = greedy.grid
	else:
		# Run randomize algorithm on grid as often as user specified
		randomize = rz.Randomize(grid)
		randomize.run(iterations=5)
		starting_grid = randomize.best_grid
	
	hillclimber = hc.HillClimber(starting_grid)
	hillclimber.run(iterations=5, hc_type=hc_type)

	# Create histogram of all results
	vis.iteration_plot(hillclimber.all_values, map_name, quantity, hc_type, start_state)

	# Visualize map and create output file for best result
	vis.visualize(hillclimber.grid, map_name, quantity, f"{start_state}_hillclimber_{hc_type}")
	hillclimber.grid.create_output(map_name, quantity, f"{start_state}_hillclimber_{hc_type}")

	return hillclimber.grid

if __name__ == "__main__":
	
	args = getArgs()

	map_name = args.map_name
	map_file = f"data/wijken/{args.map_name}.csv"
	quantity = args.quantity_houses
	algorithm = args.algorithm

	# Create grid based on quantity of houses and map requested by user
	grid = grid.Grid(quantity, map_file)

	if algorithm in ["random", "r"]:
		# Prompt for number of iterations until user provides valid input
		while True:
			iterations = input("How many times do you want to run random?\n")
			
			# Valid input must be a positive integer equal to or bigger than 1
			if iterations.isdigit() and int(iterations) >= 1:
				break
			else:
				print("Invalid input: Please enter an integer that is equal to or bigger than 1")

		result = implement_random(grid, int(iterations), map_name, quantity)
	elif algorithm in ["greedy", "gr"]:
		# Prompt for type of greedy algorithm until user provides valid input
		while True:
			specification = input("Which type of greedy do you want to run: Random/r or strategy/s?\n")
			
			# Run requested greedy algorithm if possible, else re-prompt user
			if specification in ["strategy", "s"]:
				gr_type = "strategy"
				break
			elif specification in ["random", "r"]:
				gr_type = "random"
				break
			else:
				print("Invalid input: Please choose between 'random'/'r' and 'strategy'/'s'")
		
		result = implement_greedy(grid, map_name, quantity, gr_type)
	elif algorithm in ["greedy_hill_climber", "gr_hc", "random_hill_climber", "r_hc"]:
		# Prompt for type of greedy algorithm until user provides valid input
		while True:
			specification = input("Which type of HillClimber do you want to run: Switch/s or rotation/r?\n")
			
			# Run requested greedy algorithm if possible, else re-prompt user
			if specification in ["switch", "s"]:
				hc_type="switch"
				break
			elif specification in ["rotation", "r"]:
				hc_type = "rotation"
				break
			else:
				print("Invalid input: Please choose between 'rotation'/'r' and 'switch'/'s'")

		if algorithm in ["greedy_hill_climber", "gr_hc"]:
			start_state = "greedy"
		else:
			start_state = "randomize"

		result = implement_hill_climber(grid, map_name, quantity, start_state, hc_type)

	# Add runtime?
	print(f"Highest total map value: {result.value}\n",
	f"You can find a csv file and visualizations of the results at data/output/{map_name}/{quantity}")

	"""quantity = 20
	map_name = "wijk_3"
	map_source = f"data/wijken/{map_name}.csv"

	# Create grid from data
	test_grid = grid.Grid(quantity, map_source)

	# ----------------------- Randomize algorithm ---------------------------------
	print("PERFORMING RANDOMIZE")

	randomize = rz.Randomize(test_grid)

	randomize.run(iterations=10)

	#Visualize best case
	vis.visualize(randomize.best_grid, map_name, quantity, "randomize")

	# Visualize histogram
	vis.hist_plot(randomize.all_values, map_name, quantity, "randomize")

	# Create csv output file best case
	randomize.best_grid.create_output(map_name, quantity, "randomize") 

	# Determine highest value and mean
	print(f"HIGHEST RANDOMIZE VALUE: {randomize.best_value}")
	# print(f"MEAN RANDOMIZE VALUE: {mean(randomize.all_values)}")


	# # ------------------------ Greedy algorithm -----------------------------------
	# print("PERFORMING GREEDY")

	# greedy = gr.Greedy(test_grid)
	# greedy.run(gr_type="strategy")

	# # Value of grid 
	# print(f"Value greedy config: {greedy.value}")

	# # Visualize case
	# vis.visualize(greedy.grid, map_name, quantity, "greedy")

	# # Create csv output file
	# greedy.grid.create_output(map_name, quantity, "greedy")

	# # ------------------------- Hill Climber algorithm ------------------------------
	# print("PERFORMING HC")
	# start_state = "greedy" # randomize or greedy

	# # ------------------------------- SWITCH -----------------------------------------
	# hillclimber = hc.HillClimber(greedy.grid)

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
	# hillclimber = hc.HillClimber(greedy.grid)

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

	# print(f"MEAN RANDOMIZE VALUE: {mean(randomize.all_values)}")"""
