################################################################################
# visualize.py
#
# Programmeertheorie
# Anne Zonneveld, Fleur Tervoort, Seike Appold
#
# Generates visualizations of a solution for the Amstelhaege case.
################################################################################

import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection

def hist_plot(values, map_name, quantity, name):
    """
    Creates a histogram that represents the total value of a map in relation to
    the number of times an algorithm has been run. (?)
    """
    
    fig, ax = plt.subplots()
    q_iterations = len(values)

    plt.title(f"{name.capitalize()}: {q_iterations} iterations")
    plt.xlabel("Value (€)")
    plt.ylabel("Frequency")

    # Draw diagram based on passed on results
    plt.hist(values)

    path = os.path.join(".","data", "output", f"{map_name}", f"{quantity}", "figures", "analysis")

    if not os.path.exists(path):
        os.makedirs(path)

    # Save diagram to matching directory
    new_path = os.path.join(path, f"{name}_hist.png" )
    plt.savefig(new_path)


def iteration_plot(values, map_name, quantity, hc_type, start_state):
    """
    Creates a plot that shows how the value of a map is distributed across
    the development of grid value over iterations. (?)
    """

    fig, ax = plt.subplots()
    plt.title(f"Hillclimber; type {hc_type}")
    plt.xlabel("Iterations")
    plt.ylabel("Value (€)")

    q_iterations = len(values)
    iterations = np.arange(1, q_iterations + 1)

     # Draw plot based on passed on results and iterations
    plt.plot(iterations, values)
    plt.xticks(np.arange(0, q_iterations +1, int(0.25*q_iterations)))

    path = os.path.join(".","data", "output", f"{map_name}", f"{quantity}", "figures", "analysis")

    if not os.path.exists(path):
        os.makedirs(path)
    
    # Save diagram to matching directory
    new_path = os.path.join(path, f"{start_state}_hillclimber_{hc_type}.png")
    plt.savefig(new_path)


def visualize(grid, map_name, quantity, name=""):
        """
        Creates a diagram that displays a map of Amstelhaege based on
        a given grid object.
        """

        # Create diagram of size of map
        plt.plot([0, grid.width, grid.depth, 0])
        plt.title(f"{name.capitalize()}: €{str(round(grid.value, 2))}")
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

        # Make grid visible on map
        plt.grid(True)

        # Create representation of water
        water_coord= grid.load_water()
        water = draw_water(water_coord)

        # Create representation of houses
        houses_coord = grid.all_houses
        houses = draw_houses(houses_coord, grid)

        # Add water and houses to diagram
        objects.extend(water + houses)
        representations = PatchCollection(objects, match_original=True)
        ax.add_collection(representations)

        path = os.path.join(".","data", "output", f"{map_name}", f"{quantity}", "figures", "maps")

        if not os.path.exists(path):
            os.makedirs(path)

        # Save map to matching directory
        new_path = os.path.join(path, f"{name}.png")
        plt.savefig(new_path)


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

        if house.placed == True:

            # Load house coordinates without free space
            bottom_left = house.outer_house_coordinates['bottom_left']
            width = house.outer_house_coordinates['bottom_right'][0] - house.outer_house_coordinates['bottom_left'][0]
            height = house.outer_house_coordinates['top_right'][1] - house.outer_house_coordinates['bottom_right'][1]
            
            # Load house coordinates with mandatory free space
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


    