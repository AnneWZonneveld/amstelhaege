import matplotlib.pyplot as plt

def visualize(width, depth):
    
    x_max = width
    y_max = depth
    w = range(x_max)
    d = range(y_max)

    plt.plot([w], [d])  
    plt.xlim([0, x_max])
    plt.ylim([0, y_max])
    plt.grid(True)
    plt.savefig('visualization.png')