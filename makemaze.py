from random import shuffle, randrange
from numpy import array, uint8

'''
Based on: http://rosettacode.org/wiki/Maze_generation#Python
Generate a 8 bits numpy array, used by opencv.
'''
def make_maze(w=10, h=10):

    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

    ver = [["01"] * w + ['0'] for _ in range(h)] + [[]]
    hor = [["00"] * w + ['0'] for _ in range(h + 1)]
    def walk(x, y):
        vis[y][x] = 1
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "01"
            if yy == y: ver[y][max(x, xx)] = "11"
            walk(xx, yy)

    walk(randrange(w), randrange(h))

    s = []
    for (a, b) in zip(hor, ver):
        tmp = list("".join(a))
        s.append([0 if i == '0' else 255 for i in tmp])
        tmp = list("".join(b))
        s.append([0 if i == '0' else 255 for i in tmp])
    return array(s[:-1]).astype(uint8)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    maze = make_maze(w=10, h=10)
    plt.imshow(maze)
    plt.show()
