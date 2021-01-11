import matplotlib.pyplot as plt
import numpy as np
import os

def visualize(grid, wijk):
    # create diagram representing a map of the Amstelhaege
    plt.axis([0, grid.width, 0, grid.depth]) 
    plt.xticks(np.arange(0, grid.width + 1, 1))
    plt.yticks(np.arange(0, grid.depth + 1, 1)) 
    # how start from bottom left corner from https://stackoverflow.com/questions/44395838/how-to-make-0-0-on-matplotlib-graph-on-the-bottom-left-corner
    plt.xlim([0, grid.width])
    plt.ylim([0, grid.depth])
    plt.grid(True)

    # load correct map
    if wijk == "wijk_1":
        water = grid.load_water("data/wijken/wijk_1.csv")
    elif wijk == "wijk_2":
        water = grid.load_water("data/wijken/wijk_2.csv")
    else:
        water = grid.load_water("data/wijken/wijk_3.csv")
    
    # how to loop through nested dict from https://www.learnbyexample.org/python-nested-dictionary/#:~:text=Access%20Nested%20Dictionary%20Items,key%20in%20multiple%20square%20brackets.&text=If%20you%20refer%20to%20a,dictionary%2C%20an%20exception%20is%20raised.&text=To%20avoid%20such%20exception%2C%20you,special%20dictionary%20get()%20method.
    for ident, coordinates in water.items():
        # *0.1 adjusts coordinates to smaller map for testing
        # how to draw rectangle in diagram from https://www.codespeedy.com/how-to-draw-shapes-in-matplotlib-with-python/
        bottom_x = int(water[ident].get('bottom_left_x'))*0.1
        bottom_y = int(water[ident].get('bottom_left_y'))*0.1
        top_x = int(water[ident].get('top_right_x'))*0.1
        top_y = int(water[ident].get('top_right_y'))*0.1

        water_vis = plt.Rectangle((bottom_x, bottom_y), top_x, top_y, fc="blue")
        # plt.gca().add_patch(h1)
        plt.gca().add_patch(water_vis)

    # load house, todo: load based on grid
    print(grid.all_houses)
    """
        for house in grid.all_houses:
            print(house)
    """
    # Hardcode house for test
    house = plt.Rectangle((0, 0), 0.8, 0.8, fc="orange")
    plt.gca().add_patch(house)
    
    # Todo: load houses based on grid

    # save map to current directory
    visualization = os.path.join('.','code', 'visualization', 'visualization.png')
    plt.savefig(visualization)