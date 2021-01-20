from code.classes import grid, house # niet nodig? 
from code.visualization import visualize as vis
from code.algorithms import randomize as rz
# from code.algorithms import greedy as gr

if __name__ == "__main__":

    quantity = 20
    map_source = "data/wijken/wijk_3.csv"

    # Create grid from data
    test_grid = grid.Grid(quantity, map_source)

    # Value of grid 
    # print(f"Value greedy config: {greedy.graph.value}")
    random = rz.random_assignment(test_grid)
    # Visualize case
    vis.visualize(random)

    # Create csv output file
    # greedy.graph.create_output()



