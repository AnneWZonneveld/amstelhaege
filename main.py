from code.classes import grid, house
from code.visualization import visualize as vis

if __name__ == "__main__":
    test_grid = grid.Grid(20)
    """
    print(test_grid.cells[0,3].x_coordinate)
    print(test_grid.cells[0,3].y_coordinate)
    """

    # visualize wijk_1
    vis.visualize(test_grid.width, test_grid.depth, test_grid, "wijk_3")

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
