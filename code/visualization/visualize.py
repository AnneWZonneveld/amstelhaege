import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import numpy as np
import os
from IPython import embed;


def visualize(grid):
    """
    Creates a diagram that displays a map of Amstelhaege based on
    a given grid object.
    """

    # Create diagram of size of map
    plt.plot([0, grid.width, grid.depth, 0])
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

    # Create representation of water
    water_coord= grid.load_water()
    water = draw_water(water_coord)

    # Create representation of houses
    houses_coord = grid.all_houses
    houses = draw_houses(houses_coord)

    # Add water and houses to diagram
    objects.extend(water + houses)
    representations = PatchCollection(objects, match_original=True)
    ax.add_collection(representations)

    # Save diagram to current directory
    visualization = os.path.join('.','code', 'visualization', 'visualization.png')
    plt.savefig(visualization)
    
def draw_water(water_coord):
    """
    Returns a list of patches based on given coordinates that represent the
    water surface(s).
    """

    water = []

    for water_object in water_coord:
        bottom_left = water_object.coordinates['bottom_left']
        width = water_object.coordinates['top_right'][0] - bottom_left[0]
        height = water_object.coordinates['top_right'][1] - bottom_left[1]

        water.append(plt.Rectangle(bottom_left, width, height, fc="b"))

    # for ident, coordinates in water_coord.items():
    #     bottom_left =  water_coord[ident].get('bottom_left')
    #     width = water_coord[ident].get('top_right')[0] - bottom_left[0]
    #     height = water_coord[ident].get('top_right')[1] - bottom_left[1]

    #     water.append(plt.Rectangle(bottom_left, width, height, fc="b"))
    
    return water

def draw_houses(houses_coord):
    """
    Returns a list of patches based on given coordinates that represent the
    houses and their surrounding mandatory free space.
    """
    
    houses = []
    
    for house in houses_coord:

        if house.placed == True:
            
            # Load house coordinates without free space
            bottom_left = house.outer_house_coordinates['bottom_left']
            width = house.outer_house_coordinates['bottom_right'][0] - house.outer_house_coordinates['bottom_left'][0]
            height = house.outer_house_coordinates['top_right'][1] - house.outer_house_coordinates['bottom_right'][1]

            # Load house coordinates with free space
            free_space_bottom_left = house.outer_man_free_coordinates['bottom_left']
            free_space_width = house.outer_man_free_coordinates['bottom_right'][0] - house.outer_man_free_coordinates['bottom_left'][0]
            free_space_height = house.outer_man_free_coordinates['top_right'][1] - house.outer_man_free_coordinates['bottom_right'][1]
            
            # Represent each type of house with a different color
            if house.type == "single":
                color = "r"
            elif house.type == "bungalow":
                color = "y"
            else:
                color = "g"
            
            house = plt.Rectangle(bottom_left, width, height, fc=color)
            free_space = plt.Rectangle(free_space_bottom_left, free_space_width, free_space_height, fc=color, alpha=0.3)
            houses.extend((house, free_space))
    
    return houses