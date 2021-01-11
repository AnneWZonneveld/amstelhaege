from code.classes import grid
from code.visualization import visualize as vis

if __name__ == "__main__":
    test_grid = grid.Grid(20, "data/wijken/wijk_2.csv")
    print(test_grid.cells[0,3].x_coordinate)
    print(test_grid.cells[0,3].y_coordinate)

    # visualization
    vis.visualize(test_grid.width, test_grid.depth)

    test_grid = grid.Grid(20, "data/wijken/wijk_2.csv")
    houses = test_grid.all_houses
    print(f"houses: {houses}")
    print(houses[1].type)
    print(test_grid.cells[0,0].x_coordinate)
    print(test_grid.cells[0,0].y_coordinate)
    test_grid.print_grid()
