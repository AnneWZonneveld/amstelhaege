###############################################################################
# main.py
#
# Programmeertheorie
# Anne Zonneveld, Fleur Tervoort en Seike Appold
#
# - Runs algorithm depending on command line arguments.
###############################################################################


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


def aks_iterations():
	"""
	Prompts for iterations.
	"""

	iterations = input("How many times do you want to run random?\n")
	
	# Valid input must be a positive integer equal to or bigger than 1
	if iterations.isdigit() and int(iterations) >= 1:
		return int(iterations)

	print("Invalid input: Please enter an integer that is equal to or bigger than 1")
	iterations = None

	return iterations


def ask_gr_type():
	"""
	Prompts for greedy type.
	"""

	specification = input("Which type of greedy do you want to run: Random/r or strategy/s?\n")
	gr_type = None

	# Check if valid input
	if specification in ["strategy", "s"]:
		gr_type = "strategy"

	elif specification in ["random", "r"]:
		gr_type = "random"

	else:
		print("Invalid input: Please choose between 'random'/'r' and 'strategy'/'s'")

	return gr_type


def ask_hc_type():
	"""
	Prompts for hillclimber type.
	"""

	specification = input("Which type of HillClimber do you want to run: switch/s or rotation/r?\n")
	hc_type = None

	# Check if valid input
	if specification in ["switch", "s"]:
		hc_type="switch"

	elif specification in ["rotation", "r"]:
		hc_type = "rotation"

	else:
		print("Invalid input: Please choose between 'rotation'/'r' and 'switch'/'s'")

	return hc_type


def implement_random(grid, iterations, map_name, quantity):
	"""
	Runs a specified number of iterations of random algorithm on
	grid for the specified number of times. "Quantity" specifies
	the number of houses to be placed each run and "map_name" the
	underlying map. Returns grid configuration with most value.
	"""

	# Run randomize algorithm on grid as often as user specified
	randomize = rz.Randomize(grid)
	iterations = iterations
	randomize.run(iterations=iterations)

	# Create histogram of all results
	vis.hist_plot(randomize.all_values, map_name, quantity, "randomize")

	# Visualize map and create output file for best result 
	vis.visualize(randomize.best_grid, map_name, quantity, "randomize")
	randomize.best_grid.create_output(map_name, quantity, "randomize")

	print(f"RANDOMIZE MEAN: {mean(randomize.all_values)}")

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


def implement_hill_climber(grid, map_name, quantity, start_state, hc_type, extra_arg):
	"""
	Runs a specified number of iterations of hillclimber algorithm on
	grid. "Quantity" specifies the number of houses to be placed each
	run and "map_name" the underlying map. Uses random or greedy
	configuration as start state, depending on "start_state". Runs
	switch or rotation version of hilclimber, depending on "gr_type".
	"""

	if start_state == "greedy":

		# Run greedy algorithm on grid with type that user specified
		starting_grid = implement_greedy(grid, map_name, quantity, extra_arg)

	else:

		# Run randomize algorithm on grid as often as user specified
		starting_grid = implement_random(grid, extra_arg, map_name, quantity)

	# Run hill climber	
	hillclimber = hc.HillClimber(starting_grid)
	hillclimber.run(iterations=2000, hc_type=hc_type)

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

	# Check for algoritm 
	if algorithm in ["random", "r"]:

		# Prompt for number of iterations until user provides valid input
		iterations = None
		while iterations == None:

			# Ask input
			iterations = aks_iterations()

		# Run random algorithm
		result = implement_random(grid, iterations, map_name, quantity)

	elif algorithm in ["greedy", "gr"]:

		# Prompt for type of greedy algorithm until user provides valid input
		gr_type = None
		while gr_type == None:

			# Ask input
			gr_type = ask_gr_type()
		
		# Run greedy algoithm 
		result = implement_greedy(grid, map_name, quantity, gr_type)

	elif algorithm in ["greedy_hill_climber", "gr_hc", "random_hill_climber", "r_hc"]:

		# Prompt for type of hillclimber algorithm until user provides valid 
		hc_type = None
		while hc_type == None:

			# Ask input
			hc_type = ask_hc_type()

		# If intended start state is greedy
		if algorithm in ["greedy_hill_climber", "gr_hc"]:
			start_state = "greedy"

			# Prompt for greedy type until user provides valid answer
			extra_arg = None
			while extra_arg == None:

				# Ask input
				extra_arg = ask_gr_type()

		# If inteded start state is random
		else:
			start_state = "randomize"

			# Prompt for number of iterations until user provides valid input
			extra_arg = None
			while extra_arg == None:

				# Ask input
				extra_arg = aks_iterations()

		# Run hill climber algorithm
		result = implement_hill_climber(grid, map_name, quantity, start_state, hc_type, extra_arg)

	# Results
	print(f"Highest total map value: {result.value }\n",
	f"You can find a csv file and visualizations of the results at data/output/{map_name}/{quantity}")