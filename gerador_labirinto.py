from random import shuffle, randrange
from numpy import array, uint8
import matplotlib.pyplot as plt

'''
Based on: http://rosettacode.org/wiki/Maze_generation#Python
Generate a 8 bits numpy array, used by opencv.
'''
def make_maze(w=10, h=10, scale=1):
    if scale == 0:
        scale = 1
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

    ver = [["0" + scale * "1"] * w + ['0'] for _ in range(h)] + [[]]
    hor = [["0" + scale * "0"] * w + ['0'] for _ in range(h + 1)]
    def walk(x, y):
        vis[y][x] = 1
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "0" + scale * "1"
            if yy == y: ver[y][max(x, xx)] = "1" + scale * "1"
            walk(xx, yy)

    walk(randrange(w), randrange(h))

    s = []
    for (a, b) in zip(hor, ver):
        tmp = list("".join(a))
        #tmp = [scale * i for i in tmp]
        s.append([0 if i == '0' else 255 for i in tmp])
        tmp = list("".join(b))
        #tmp = [scale * i for i in tmp]
        s.append([0 if i == '0' else 255 for i in tmp])
    return array(s[:-1]).astype(uint8)

if __name__ == "__main__":
    maze = make_maze(w=10,h=10,scale=1)
    plt.imshow(maze)
    plt.show()
