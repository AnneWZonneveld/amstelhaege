import matplotlib.pyplot as plt
import numpy as np
import os

def visualize(grid):
    """
        Creates a diagram that displays a map of Amstelhaege based
        on a given grid object.
    """

    # Create diagram representing a map of the Amstelhaege
    plt.axis([0, grid.depth, grid.width, 0])

    # Define scaling of axes 
    plt.xticks(np.arange(0, grid.depth + 1, 10))
    plt.yticks(np.arange(0, grid.width + 1, 10)) 

    # Label axes
    plt.xlabel("Depth")
    plt.ylabel("Width")

    # Begin scaling where x- and y-axis meet
    # from https://stackoverflow.com/questions/44395838/how-to-make-0-0-on-matplotlib-graph-on-the-bottom-left-corner
    plt.xlim([0, grid.depth])
    plt.ylim([grid.width, 0])

    # Show grid
    plt.grid(True)

    # Load water coordinates from correct map
    water = grid.load_water(grid.map)
    # print(f" Water: {water}")

    # how to loop through nested dict from https://www.learnbyexample.org/python-nested-dictionary/#:~:text=Access%20Nested%20Dictionary%20Items,key%20in%20multiple%20square%20brackets.&text=If%20you%20refer%20to%20a,dictionary%2C%20an%20exception%20is%20raised.&text=To%20avoid%20such%20exception%2C%20you,special%20dictionary%20get()%20method.
    # Add representation of water to diagram
    for ident, coordinates in water.items():

        # how to draw rectangle in diagram from https://www.codespeedy.com/how-to-draw-shapes-in-matplotlib-with-python/
        
        bottom_left =  water[ident].get('bottom_left')
        top_right = water[ident].get('top_right')

        water_vis = plt.Rectangle(bottom_left, int(top_right[0]), int(top_right[1]), fc="blue")
        plt.gca().add_patch(water_vis)

    # Load houses based on grid and add to diagram
    for house in grid.all_houses.values():

        rectangle_width = house.coordinates['bottom_right'][0] - house.coordinates['bottom_left'][0]
        rectangle_height = house.coordinates['top_right'][1] - house.coordinates['bottom_right'][1]

        # Create rectangle for specific type 
        if house.type == "single":
            rectangle = plt.Rectangle(house.coordinates['bottom_left'], rectangle_width, rectangle_height, fc="r")
        elif house.type == "bungalow":
            rectangle = plt.Rectangle(house.coordinates['bottom_left'], rectangle_width, rectangle_height, fc="y")
        else:
            rectangle = plt.Rectangle(house.coordinates['bottom_left'], rectangle_width, rectangle_height, fc="g")

        plt.gca().add_patch(rectangle)

    # Save map to current directory
    visualization = os.path.join('.','code', 'visualization', 'visualization.png')
    plt.savefig(visualization)