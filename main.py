from code.classes import grid, house
from code.visualization import visualize as vis
from code.algorithms import randomize 

if __name__ == "__main__":

<<<<<<< HEAD
	# Create grid
    test_grid = grid.Grid(20, "data/wijken/wijk_1.csv")
    # test_grid.print_grid()
=======
	Create grid
    test_grid = grid.Grid(20, "data/wijken/wijk_1.csv")
    test_grid.print_grid()
>>>>>>> 6de122252cabee852620633ffd45d5247b35334e

    test_grid.print_grid()
    water = test_grid.load_water("data/wijken/wijk_2.csv")
    print(water)
    
    Randomize algorithm

    random_config = randomize.random_assignment(test_grid)

    print("New grid:")
    random_config.print_grid()

<<<<<<< HEAD
    # Visualize case
    vis.visualize(random_config)
=======
    Visualize case
    vis.visualize(test_grid)
>>>>>>> 6de122252cabee852620633ffd45d5247b35334e

    # Create csv output file
    test_grid.create_output()
