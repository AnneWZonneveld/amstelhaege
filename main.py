from code.classes import grid
from code.visualization import visualize as vis

if __name__ == "__main__":
    test_grid = grid.Grid()
    print(test_grid.cells[0,3].x_coordinate)
    print(test_grid.cells[0,3].y_coordinate)

    # visualization
    vis.visualize()