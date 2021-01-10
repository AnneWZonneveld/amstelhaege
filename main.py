from code.classes import grid, house
from code.visualization import visualize as vis
from code.algorithms import randomize 

if __name__ == "__main__":

	# Create grid
    test_grid = grid.Grid(20)
    test_grid.print_grid()

    water = test_grid.load_water("data/wijken/wijk_2.csv")
    print(water)

    # visualize wijk_1
    vis.visualize(test_grid.width, test_grid.depth, test_grid, "wijk_3")

    houses = test_grid.all_houses
    # print(f"houses: {houses}")
    
    # Randomize algorithm
    random_config = randomize.random_assignment(test_grid, houses)
    print("New grid:")
    random_config.print_grid()