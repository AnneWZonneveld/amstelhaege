import matplotlib.pyplot as plt

def visualize(width, depth):

    w = range(width)
    d = range(depth)

    plt.plot([w], [d])  
    
    # how start from bottom left corner from https://stackoverflow.com/questions/44395838/how-to-make-0-0-on-matplotlib-graph-on-the-bottom-left-corner
    plt.xlim([0, width])
    plt.ylim([0, depth])
    
    plt.grid(True)

    # how to draw rectangle in diagram from https://www.codespeedy.com/how-to-draw-shapes-in-matplotlib-with-python/
    house = plt.Rectangle((0, 0), 2, 2.32, fc="blue")
    plt.gca().add_patch(house)
    plt.savefig('visualization.png')