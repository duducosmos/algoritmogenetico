#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np


from pygenic.populacao import Populacao



func = lambda x, y: (3 * np.exp(-(y + 1) ** 2 - x **2)*(x - 1)**2
                 - (np.exp(-(x+ 1) ** 2 - y **2) / 3 )
                 + np.exp(-x **2 - y ** 2) * (10 * x **3 - 2 * x + 10 * y ** 5)
                )

def bin(x):
    cnt = np.array([2 ** i for i in range(x.shape[1])])
    return np.array([sum(cnt * x[i,:]) for i in range(x.shape[0])])

def avaliacao(populacao):
    colunas = populacao.shape[1]
    meio = int(colunas / 2)
    const = 2.0 ** meio - 1.0
    nmin = -3
    nmax = 3
    const = (nmax - nmin) / const
    x = nmin + const * bin(populacao[:,:meio])
    y = nmin + const * bin(populacao[:,meio:])
    tmp = func(x, y)
    return tmp

cromossos_totais = 8
tamanho_populacao = 5

populacao = Populacao(avaliacao, cromossos_totais, tamanho_populacao)
populacao.gerar_populacao()
populacao.avaliar()


fig = plt.figure(figsize=(100, 100))
ax = fig.add_subplot(111, projection="3d")
X, Y = np.mgrid[-3:3:30j, -3:3:30j]
Z = func(X,Y)

ax.plot_wireframe(X, Y, Z)
#ax.scatter(x, y, func(x, y), s=10, c='red', marker='D')
plt.show()
