import matplotlib.pyplot as plt
import numpy as np

def visualize(width, depth, grid, wijk):

    plt.axis([0, grid.width, 0, grid.depth]) 
    plt.xticks(np.arange(0, grid.width + 1, 1))
    plt.yticks(np.arange(0, grid.depth + 1, 1)) 
    # how start from bottom left corner from https://stackoverflow.com/questions/44395838/how-to-make-0-0-on-matplotlib-graph-on-the-bottom-left-corner
    plt.xlim([0, grid.width])
    plt.ylim([0, grid.depth])
    plt.grid(True)
    
    # how to draw rectangle in diagram from https://www.codespeedy.com/how-to-draw-shapes-in-matplotlib-with-python/
    
    """
    Todo: load house(s)
    test_house = house.House("single", 1)
    h1 = plt.Rectangle((x, y), 8, 8, fc="orange")
    """

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
        bottom_x = int(water[ident].get('bottom_left_x'))*0.1
        bottom_y = int(water[ident].get('bottom_left_y'))*0.1
        top_x = int(water[ident].get('top_right_x'))*0.1
        top_y = int(water[ident].get('top_right_y'))*0.1
        print(f"{bottom_x}, {bottom_y}, {top_x}, {top_y}")

        water_vis = plt.Rectangle((bottom_x, bottom_y), top_x, top_y, fc="blue")
        # plt.gca().add_patch(h1)
        plt.gca().add_patch(water_vis)

    plt.savefig('visualization.png')