from code.classes import grid, house
from code.visualization import visualize as vis
from code.algorithms import randomize 

if __name__ == "__main__":


	# Create grid
    test_grid = grid.Grid(20, "data/wijken/wijk_1.csv")
    # print(test_grid.load_houses(20))
    # print(test_grid.load_water())
    
    # Randomize algorithm
    random_config = randomize.random_assignment(test_grid)

    # print("New grid:")
    # print(random_config.cells)

    # Visualize case
    vis.visualize(random_config)

    # Create csv output file
    random_config.create_output()
