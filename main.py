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
						choices = ["random", "r", "greedy", "gr", "greedy_hill_climber", "random_hill_climber"],
						metavar = "algorithm", help = "place houses with this algorithm (e.g. random)")
	args = parser.parse_args()

	return args

if __name__ == "__main__":
	
	"""quantity = 20
	map_name = "wijk_1"
	map_source = f"data/wijken/{map_name}.csv"

	# Create grid from data
	test_grid = grid.Grid(quantity, map_source)

	greedy = gr.Greedy(test_grid)
	greedy.run(gr_type="strategy")

	# # Value of grid 
	print(f"Value greedy config: {greedy.value}")

	# # Visualize case
	vis.visualize(greedy.grid, map_name, quantity, "greedy")

	# # Create csv output file
	greedy.grid.create_output(map_name)"""
	
	args = getArgs()

	# Derive path to correct source file from map name
	map_file = f"data/wijken/{args.map_name}.csv"
	# Create grid based on quantity of houses and file requested by user
	grid = grid.Grid(args.quantity_houses, args.map_file)

	if args.algorithm in ["random", "r"]:
		
		# Prompt for number of iterations until user provides valid input
		while True:
			iterations = input("How many times do you want to run random?")
			
			# Valid input must be a positive integer equal to or bigger than 1
			if iterations.isdigit() and int(iterations) >= 1:
				break
			else:
				print("Invalid input: Please enter an integer that is equal to or bigger than 1")

		# Run randomize algorithm on grid as often as user specified
		randomize = rz.Randomize(grid)
		randomize.run(iterations=int(iterations))

		# Create visualization of map for best result
		vis.visualize(randomize.best_grid, args.map_name, args.quantity_houses, "randomize")

		# Create histogram 
		vis.hist_plot(randomize.all_values, args.map_name, args.quantity_houses, "randomize")

		# Create csv output file for the best result
		randomize.best_grid.create_output(args.map_name, args.quantity_houses, "randomize")

		# Determine highest value and mean
		print(f"HIGHEST RANDOMIZE VALUE: {randomize.best_value}")
		print(f"MEAN RANDOMIZE VALUE: {mean(randomize.all_values)}")
	elif args.algorithm in ["greedy", "gr"]:
		greedy = gr.Greedy(test_grid)

		# Prompt for type of greedy algorithm until user provides valid input
		while True:
			gr_type = input("Which type of greedy do you want to run: Random/r or strategic/s?")
			
			# Run requested greedy algorithm if possible, else re-prompt user
			if gr_type in ["strategic", "s"]:
				print("RUNNING STRATEGIC GREEDY")
				greedy.run(gr_type="strategy")
				break
			elif gr_type in ["random", "r"]:
				print("RUNNING RANDOM GREEDY")
				greedy.run(gr_type="random")
				break
			else:
				print("Invalid input: Please choose between 'random'/'r' and 'strategic'/'s'")
		
		# Create visualization of map for best result
		vis.visualize(greedy.grid, args.map_file, args.quantity_houses, f"greedy_{gr_type}")

		# Create histogram 
		vis.hist_plot(greedy.all_values, args.map_file, args.quantity_houses, f"greedy_{gr_type}")

		# Create csv output file for the best result
		greedy.grid.create_output(f"greedy_{gr_type}")

		# Value of grid 
		print(f"GREEDY VALUE: {greedy.value}")

	elif args.algorithm in ["greedy_hill_climber", "random_hill_climber"]:
		# start_state = args.algorithm
		# Prompt for type of greedy algorithm until user provides valid input
		while True:
			gr_type = input("Which type of greedy do you want to run: Random/r or strategic/s?")
			
			# Run requested greedy algorithm if possible, else re-prompt user
			if gr_type in ["strategic", "s"]:
				print("RUNNING STRATEGIC GREEDY")
				greedy.run(gr_type="strategy")
				break
			elif gr_type in ["random", "r"]:
				print("RUNNING RANDOM GREEDY")
				greedy.run(gr_type="random")
				break
			else:
				print("Invalid input: Please choose between 'random'/'r' and 'strategic'/'s'")
		#Ask which hill climber
		#Run hill climber

	# ------------------------- Hill Climber algorithm ------------------------------
	#print("PERFORMING HC")
	#start_state = "randomize" # randomize or greedy

	# ------------------------------- SWITCH -----------------------------------------
	#hillclimber = hc.HillClimber(randomize.best_grid)

	#hc_type = "switch"
	#hillclimber.run(iterations=2000, hc_type=hc_type)

	# Value of grid
	#print(f"HILLCLIMBER VALUE: {hillclimber.value}")

	# Visualize case
	# vis.visualize(hillclimber.grid, map, quantity, f"{start_state}_hillclimber_{hc_type}")

	# Visualize iterations
	# vis.iteration_plot(hillclimber.all_values, map, quantity, f"{start_state}_hillclimber_{hc_type}")

	# Create csv output file
	# hillclimber.grid.create_output(f"hillclimber_{hc_type}")

	# ---------------------------------- ROTATION --------------------------------------
	#hillclimber = hc.HillClimber(randomize.best_grid)

	#hc_type = "rotation"
	#hillclimber.run(iterations=2000, hc_type=hc_type)

	# Value of grid
	#print(f"HILLCLIMBER VALUE: {hillclimber.value}")

	# Visualize case
	# vis.visualize(hillclimber.grid, map, quantity, f"{start_state}_hillclimber_{hc_type}")

	# Visualize iterations
	# vis.iteration_plot(hillclimber.all_values, map, quantity, f"{start_state}_hillclimber_{hc_type}")

	# Create csv output file
	# hillclimber.grid.create_output(f"hillclimber_{hc_type}")



