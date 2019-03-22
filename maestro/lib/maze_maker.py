import numpy as np
from numpy.random import randint
import matplotlib.pyplot as plt


def generate_maze(width=81, height=51, complexity=0.75, density =0.75):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density = int(density * (shape[0] // 2 * shape[1] // 2))
    # Build actual maze
    maze = np.zeros(shape, dtype=bool)
    # Fill borders
    maze[0, :] = maze[-1, :] = 1
    maze[:, 0] = maze[:, -1] = 1
    # Make isles
    for i in range(density):
        x, y = randint(0, shape[1] // 2) * 2, randint(0, shape[0] // 2) * 2
        maze[y, x] = 1
        for j in range(complexity):
            neighbors = []
            if x > 1: neighbors.append((y, x - 2))
            if x < shape[1] - 2: neighbors.append((y, x + 2))
            if y > 1: neighbors.append((y - 2, x))
            if y < shape[0] - 2: neighbors.append((y + 2, x))
            if len(neighbors):
                y_, x_ = neighbors[randint(0, len(neighbors) - 1)]
                if maze[y_, x_] == 0:
                    maze[y_, x_] = 1
                    maze[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    return maze


def display_maze(maze):
    plt.figure(figsize=(10, 5))
    plt.imshow(maze, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()


if __name__ == '__main__':
    display_maze(generate_maze(80, 40))
