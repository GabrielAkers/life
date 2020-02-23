import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# mostly followed this tutorial: https://www.geeksforgeeks.org/conways-game-life-python-implementation/
# i think i'll reimpliment with a sparse matrix representation for performance improvements
# i learned a decent amount about animating using matplotlib from this

ALIVE = 1
DEAD = 0
vals = [ALIVE, DEAD]


def random_grid(n):
    return np.random.choice(vals, n*n).reshape(n, n)


def add_glider(x, y, grid):
    glider = np.array([[0, 0, 1],
                       [1, 0, 1],
                       [0, 1, 1]])
    grid[x:x+3, y:y+3] = glider


def add_blinker(x, y, grid):
    blinker = np.array([[0, 1, 0],
                        [0, 1, 0],
                        [0, 1, 0]])
    grid[x:x+3, y:y+3] = blinker


def update(frame, img, grid, n):
    temp_grid = grid.copy()
    for x in range(n):
        for y in range(n):
            # the modulo is so the grid wraps
            neighbor_total = int((grid[x, (y-1) % n] + grid[x, (y+1) % n] +
                                  grid[(x-1) % n, y] + grid[(x+1) % n, y] +
                                  grid[(x-1) % n, (y-1) % n] + grid[(x-1) % n, (y+1) % n] +
                                  grid[(x+1) % n, (y-1) % n] + grid[(x+1) % n, (y+1) % n]))
            if grid[x, y] == ALIVE:
                if neighbor_total < 2 or neighbor_total > 3:
                    temp_grid[x, y] = DEAD
            elif neighbor_total == 3:
                temp_grid[x, y] = ALIVE
    img.set_data(temp_grid)
    grid[:] = temp_grid[:]
    return img


def main():

    parser = argparse.ArgumentParser(description="Conway's game of life")

    parser.add_argument('--grid-size', dest='n', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--blinker', action='store_true', required=False)
    args = parser.parse_args()

    n = 50
    if args.n and int(args.n) > 8:
        n = int(args.n)

    update_time = 50
    if args.interval:
        update_time = int(args.interval)

    if args.glider:
        grid = np.zeros(n*n).reshape(n, n)
        add_glider(1, 1, grid)
    elif args.blinker:
        grid = np.zeros(n*n).reshape(n, n)
        add_blinker(int(n/2), int(n/2), grid)
    else:
        grid = random_grid(n)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    anim = animation.FuncAnimation(fig, update, fargs=(img, grid, n, ),
                                   frames=10,
                                   interval=update_time,
                                   save_count=50)

    if args.movfile:
        anim.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


if __name__ == '__main__':
    main()





