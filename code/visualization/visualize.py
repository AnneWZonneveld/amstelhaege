import matplotlib.pyplot as plt
import numpy as np

def visualize(width, depth, house):

    plt.axis([0, width, 0, depth])  

    # how start from bottom left corner from https://stackoverflow.com/questions/44395838/how-to-make-0-0-on-matplotlib-graph-on-the-bottom-left-corner
    plt.xlim([0, width])
    plt.ylim([0, depth])

    plt.grid(True)

    # how to draw rectangle in diagram from https://www.codespeedy.com/how-to-draw-shapes-in-matplotlib-with-python/
    x = 4
    y = 0

    h1 = plt.Rectangle((x, y), house.width, house.depth, fc="orange")
    w1 = plt.Rectangle((0, 0), 3.2, 18, fc="blue")

    plt.gca().add_patch(h1)
    plt.gca().add_patch(w1)

    plt.savefig('visualization.png')