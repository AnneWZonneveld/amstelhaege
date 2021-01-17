import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import numpy as np
import os

def visualize(grid):
    """
    Creates a diagram that displays a map of Amstelhaege based on
    a given grid object.
    """

    # Create diagram representing a map of Amstelhaege
    plt.axis([0, grid.width, grid.depth, 0])
    plt.xlabel("Width")
    plt.ylabel("Depth")

    # Prepare for drawing multiple objects at once
    fig, ax = plt.subplots()
    objects = []

    # Set scaling properties
    plt.xticks(np.arange(0, grid.width + 1, 10))
    plt.yticks(np.arange(0, grid.depth + 1, 10)) 
    plt.xlim([0, grid.width])
    plt.ylim([grid.depth, 0])

    # Set grid properties
    plt.grid(True)
    plt.gca().set_aspect("equal")

    # Load water coordinates from correct map
    water_coord = grid.load_water()

    # Add representation of water to diagram
    for ident, coordinates in water_coord.items():
        bottom_left =  water_coord[ident].get('bottom_left')
        width = water_coord[ident].get('top_right')[0] - bottom_left[0]
        height = water_coord[ident].get('top_right')[1] - bottom_left[1]

        water = plt.Rectangle(bottom_left, width, height, fc="b")
        objects.append(water)

    # Add representation of houses to diagram
    for house in grid.all_houses.values():
        # Load house coordinates without free space
        bottom_left = house.coordinates['bottom_left']
        width = house.coordinates['bottom_right'][0] - house.coordinates['bottom_left'][0]
        height = house.coordinates['top_right'][1] - house.coordinates['bottom_right'][1]

        # Load house coordinates with free space
        free_space_bottom_left = house.min_free_coordinates['bottom_left']
        free_space_width = house.min_free_coordinates['bottom_right'][0] - house.min_free_coordinates['bottom_left'][0]
        free_space_height = house.min_free_coordinates['top_right'][1] - house.min_free_coordinates['bottom_right'][1]
        
        # Represent each type of house with a different color
        if house.type == "single":
            color = "r"
        elif house.type == "bungalow":
            color = "y"
        else:
            color = "g"
        
        house = plt.Rectangle(bottom_left, width, height, fc=color)
        free_space = plt.Rectangle(free_space_bottom_left, free_space_width, free_space_height, fc=color, alpha=0.3)
        objects.extend((house, free_space))
    
    representations = PatchCollection(objects, match_original=True)
    ax.add_collection(representations)

    # Save diagram to current directory
    visualization = os.path.join('.','code', 'visualization', 'visualization.png')
    plt.savefig(visualization)