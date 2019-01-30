from numpy import exp, mgrid, linspace
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.animation import FuncAnimation
from numpy.random import choice

def func(x, y):
    tmp = 3 * exp(-(y + 1) ** 2 - x **2)*(x - 1)**2 \
          - (exp(-(x+ 1) ** 2 - y **2) / 3 )\
          + exp(-x **2 - y ** 2) * (10 * x **3 - 2 * x + 10 * y ** 5)
    return tmp

fig = plt.figure(figsize=(100, 100))
ax = fig.add_subplot(111, projection="3d")
X, Y = mgrid[-3:3:30j, -3:3:30j]
Z = func(X,Y)
ax.plot_wireframe(X, Y, Z)

x, y = linspace(-3, 3, 10), linspace(-3, 3, 10)

newx, newy = choice(x, 5), choice(y, 5)
z = func(newx, newy)
graph = ax.scatter(newx, newy, z, s=50, c='red', marker='D')

def update(frame):
    newx, newy = choice(x, 5), choice(y, 5)
    z = func(newx, newy)
    graph._offsets3d = (newx, newy, z)

ani = FuncAnimation(fig, update, frames=range(10000), repeat=False)
plt.show()
