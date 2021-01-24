import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import numpy as np
import os
# from IPython import embed;


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
    houses = draw_houses(houses_coord, grid)

    # Add water and houses to diagram
    objects.extend(houses + water)
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
    
    return water

def draw_houses(houses_coord, grid):
    """
    Returns a list of patches based on given coordinates that represent the
    houses and their surrounding mandatory free space.
    """
    
    houses = []
    
    for house in houses_coord:
        print(f"DRAWING HOUSE {house}")
        print(f"HOUSE COORDINATES {house.house_coordinates}")
        if house.placed == True:

            # Load house coordinates without free space
            bottom_left = house.outer_house_coordinates['bottom_left']
            width = house.outer_house_coordinates['bottom_right'][0] - house.outer_house_coordinates['bottom_left'][0]
            height = house.outer_house_coordinates['top_right'][1] - house.outer_house_coordinates['bottom_right'][1]
            print(f"{bottom_left},{width},{height}")
            # Load house coordinates with mandatory free space
            free_space_bottom_left = house.outer_man_free_coordinates['bottom_left']
            free_space_width = house.outer_man_free_coordinates['bottom_right'][0] - house.outer_man_free_coordinates['bottom_left'][0]
            free_space_height = house.outer_man_free_coordinates['top_right'][1] - house.outer_man_free_coordinates['bottom_right'][1]
            print(f"{free_space_bottom_left},{free_space_width},{free_space_height}")
            """# Load house coordinates with extra free space
            grid.calculate_extra_free_meters(house)
            extra_free = house.extra_free
            print(f"EXTRA FREE: {extra_free}")

            bottom_left_x = house.outer_man_free_coordinates['bottom_left'][0] - extra_free
            bottom_left_y = house.outer_man_free_coordinates['bottom_left'][1] + extra_free
            extra_free_bottom_left = (bottom_left_x,bottom_left_y)
            print(f"BOTTOM_LEFT: {extra_free_bottom_left}")

            bottom_right_x = house.outer_man_free_coordinates['bottom_right'][0] + extra_free
            extra_free_width = bottom_right_x-bottom_left_x
            print(f"WIDTH: {extra_free_width}")

            top_left_y = house.outer_man_free_coordinates['top_left'][1] - extra_free
            extra_free_height = top_left_y - bottom_left_y
            print(f"HEIGHT: {extra_free_height}")"""

            # Represent each type of house with a different color
            if house.type == "single":
                color = "r"
            elif house.type == "bungalow":
                color = "y"
            else:
                color = "g"
            
            house = plt.Rectangle(bottom_left, width, height, fc=color)
            free_space = plt.Rectangle(free_space_bottom_left, free_space_width, free_space_height, fc=color, alpha=0.3)
            #extra_free_space = plt.Rectangle(extra_free_bottom_left, extra_free_width, extra_free_height, fc=color, alpha=0.4)
            houses.extend((house, free_space))
    
    return houses