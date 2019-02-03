import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import matplotlib.ticker as ticker
from matplotlib import cm
from numpy import mgrid


X, Y = mgrid[0:30, 0:10]
func = lambda profundidade,ilegais: 0.1 * ((ilegais + profundidade) / ( 1e-3 * profundidade + 1)
                                             + (ilegais**3 + profundidade) / (ilegais + 1))

Z = func(X, Y)
z = func(22, 2)
fig = plt.figure()
ax = fig.gca(projection="3d")
ax.plot_wireframe(X, Y, -Z)

cset = ax.contour(X, Y, -Z, zdir='z', offset=-15, cmap=cm.coolwarm)
cset = ax.contour(X, Y, -Z, zdir='x', offset=-2, cmap=cm.coolwarm)
cset = ax.contour(X, Y, -Z, zdir='y', offset=10, cmap=cm.coolwarm)

ax.set_xlabel('X')
ax.set_xlim(-5, 31)
ax.set_ylabel('Y')
ax.set_ylim(-2, 10)
ax.set_zlabel('Z')
ax.set_zlim(-15, 0)


ax.set_xlabel("Até o topo")
ax.set_ylabel("Ilegais")
ax.set_zlabel("Objetivo")
plt.show()
