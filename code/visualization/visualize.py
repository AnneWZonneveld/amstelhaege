import matplotlib.pyplot as plt

def visualize():
    print("runs visualize()")

    plt.plot([1,2,3, 4, 5, 6])
    plt.show()
    plt.savefig('visualization.png')