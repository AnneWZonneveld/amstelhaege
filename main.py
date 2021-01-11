from code.classes import grid, house
from code.visualization import visualize as vis
from code.algorithms import randomize 

if __name__ == "__main__":

	# Create grid
    test_grid = grid.Grid(20)
<<<<<<< HEAD
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
=======
    """
    print(test_grid.cells[0,3].x_coordinate)
    print(test_grid.cells[0,3].y_coordinate)
    """
    # visualize case
    vis.visualize(test_grid, "wijk_1")

    """
    test_grid = grid.Grid(20)
    houses = test_grid.all_houses
    print(f"houses: {houses}")
    print(houses[1].type)
    print(test_grid.cells[0,0].x_coordinate)
    print(test_grid.cells[0,0].y_coordinate)
    test_grid.print_grid()
    water = test_grid.load_water("data/wijken/wijk_2.csv")
    print(water)
    """
>>>>>>> f3a6d63a5ded00262dc1aa8c0e40890cf17275f8
