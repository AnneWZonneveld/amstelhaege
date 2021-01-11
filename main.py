from code.classes import grid, house
from code.visualization import visualize as vis
from code.algorithms import randomize 

if __name__ == "__main__":

	# Create grid
    test_grid = grid.Grid(20, "data/wijken/wijk_2.csv")
    test_grid.print_grid()

    # water = test_grid.load_water("data/wijken/wijk_2.csv")
    # print(water)

    # Obtain all houses
    houses = test_grid.all_houses
    # # print(f"houses: {houses}")
    
    # Randomize algorithm
    random_config_info = randomize.random_assignment(test_grid, houses)
    random_grid = random_config_info[0]
    random_house_coordinates = random_config_info[1]
    print(f"House coordinates: {random_house_coordinates}")

    print("New grid:")
    random_grid.print_grid()

    # # visualize case
    # vis.visualize(test_grid, "wijk_1")