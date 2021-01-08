from code.classes import grid

if __name__ == "__main__":
    test_grid = grid.Grid()
    print(test_grid.cells[0,0].x_coordinate)
    print(test_grid.cells[0,0].y_coordinate)
    print(test_grid.draw())
    