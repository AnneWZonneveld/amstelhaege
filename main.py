from code.classes import grid
from code.visualization import visualize as vis
from code.algorithms import randomize 

if __name__ == "__main__":

    # visualization
    # vis.visualize()
    test_grid = grid.Grid(20)
    houses = test_grid.all_houses
    # print(f"houses: {houses}")
    # print(test_grid.cells[0,0].x_coordinate)
    # print(test_grid.cells[0,0].y_coordinate)
    test_grid.print_grid()

    # Randomize algorithm
    random_config = randomize.random_assignment(test_grid, houses)
    print("New grid:")
    random_config.print_grid()