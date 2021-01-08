from code.classes import grid

if __name__ == "__main__":
    test_grid = grid.Grid(20)
    houses = test_grid.all_houses
    
    print(houses[1].type)
    # print(test_grid.cells[0,3].x_coordinate)
    # print(test_grid.cells[0,3].y_coordinate)
    