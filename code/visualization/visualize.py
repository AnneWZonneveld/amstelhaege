import matplotlib.pyplot as plt
import numpy as np
import os

def visualize(grid):
    """
        Creates a diagram that displays a map of Amstelhaege based
        on a given grid object.
    """

    # Create diagram representing a map of the Amstelhaege
    plt.axis([0, grid.width, grid.depth, 0]) 
    plt.xticks(np.arange(0, grid.width + 1, 1))
    plt.yticks(np.arange(0, grid.depth + 1, 1)) 
    # how start from bottom left corner from https://stackoverflow.com/questions/44395838/how-to-make-0-0-on-matplotlib-graph-on-the-bottom-left-corner
    plt.xlim([0, grid.width])
    plt.ylim([grid.depth, 0])
    plt.grid(True)

    # Load water coordinates from correct map
    water = grid.load_water(grid.map)

    # how to loop through nested dict from https://www.learnbyexample.org/python-nested-dictionary/#:~:text=Access%20Nested%20Dictionary%20Items,key%20in%20multiple%20square%20brackets.&text=If%20you%20refer%20to%20a,dictionary%2C%20an%20exception%20is%20raised.&text=To%20avoid%20such%20exception%2C%20you,special%20dictionary%20get()%20method.
    # Add representation of water to diagram
    for ident, coordinates in water.items():
        # how to draw rectangle in diagram from https://www.codespeedy.com/how-to-draw-shapes-in-matplotlib-with-python/
        # how to draw rectangle in diagram from https://www.codespeedy.com/how-to-draw-shapes-in-matplotlib-with-python/
        bottom_x = int(water[ident].get('bottom_left')[0])
        bottom_y = int(water[ident].get('bottom_left')[1])
        top_x = int(water[ident].get('top_right')[0])
        top_y = int(water[ident].get('top_right')[1])

        water_vis = plt.Rectangle((bottom_x, bottom_y), top_x, top_y, fc="blue")
        plt.gca().add_patch(water_vis)
    
    # Load houses based on grid and add to diagram
    for house in grid.all_houses.values():
        width = house.coordinates['bottom_right'][0] - house.coordinates['bottom_left'][0]
        height = house.coordinates['top_right'][1] - house.coordinates['bottom_right'][1]

        # Create rectangle for specific type 
        if house.type == "single":
            rectangle = plt.Rectangle(house.coordinates['bottom_left'], width, height, fc="m")
        elif house.type == "bungalow":
            rectangle = plt.Rectangle(house.coordinates['bottom_left'], width, height, fc="y")
        else:
            rectangle = plt.Rectangle(house.coordinates['bottom_left'], width, height, fc="g")

        plt.gca().add_patch(rectangle)

    # Save map to current directory
    visualization = os.path.join('.','code', 'visualization', 'visualization.png')
    plt.savefig(visualization)