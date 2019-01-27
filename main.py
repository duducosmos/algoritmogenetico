#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Obetenção de máximo de função.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy import exp, array, mgrid
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.animation import FuncAnimation

from pygenic.populacao import Populacao
from pygenic.selecao.roleta import Roleta
from pygenic.cruzamento.kpontos import KPontos
from pygenic.mutacao.flip import Flip
from pygenic.evolucao import Evolucao



def func(x, y):
    tmp = 3 * exp(-(y + 1) ** 2 - x **2)*(x - 1)**2 \
          - (exp(-(x+ 1) ** 2 - y **2) / 3 )\
          + exp(-x **2 - y ** 2) * (10 * x **3 - 2 * x + 10 * y ** 5)
    return tmp


def bin(x):
    cnt = array([2 ** i for i in range(x.shape[1])])
    return array([(cnt * x[i,:]).sum() for i in range(x.shape[0])])


def xy(populacao):
    colunas = populacao.shape[1]
    meio = int(colunas / 2)
    const = 2.0 ** meio - 1.0
    nmin = -3
    nmax = 3
    const = (nmax - nmin) / const
    x = nmin + const * bin(populacao[:,:meio])
    y = nmin + const * bin(populacao[:,meio:])
    return x, y


def avaliacao(populacao):
    x, y = xy(populacao)
    tmp = func(x, y)
    return tmp


cromossos_totais = 16
tamanho_populacao = 100

populacao = Populacao(avaliacao, cromossos_totais, tamanho_populacao)
selecao = Roleta(populacao)
cruzamento = KPontos(tamanho_populacao)
mutacao = Flip(pmut=0.9)
evolucao = Evolucao(populacao, selecao, cruzamento, mutacao)

evolucao.nsele = 10
evolucao.pcruz = 0.5


fig = plt.figure(figsize=(100, 100))
ax = fig.add_subplot(111, projection="3d")
X, Y = mgrid[-3:3:30j, -3:3:30j]
Z = func(X,Y)
ax.plot_wireframe(X, Y, Z)

x, y = xy(populacao.populacao)
z = func(x, y)
graph = ax.scatter(x, y, z, s=50, c='red', marker='D')

def update(frame):
    evolucao.evoluir()
    x, y = xy(populacao.populacao)
    z = func(x, y)
    graph._offsets3d = (x, y, z)

ani = FuncAnimation(fig, update, frames=range(10000), repeat=False)
plt.show()
