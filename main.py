#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Obetenção de máximo de função.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy import exp, array, mgrid
from pygenic.populacao import Populacao
from pygenic.selecao.torneio import Torneio
from pygenic.cruzamento.kpontos import KPontos

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d


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


cromossos_totais = 8
tamanho_populacao = 100

populacao = Populacao(avaliacao, cromossos_totais, tamanho_populacao)
populacao.gerar_populacao()

classificacao = Torneio(populacao, tamanho=10)
subpopulacao = classificacao.selecao(10)

kpontos = KPontos(tamanho_populacao)
pop = kpontos.descendentes(subpopulacao, pcruz=0.5)

x, y = xy(pop)

fig = plt.figure(figsize=(100, 100))
ax = fig.add_subplot(111, projection="3d")
X, Y = mgrid[-3:3:30j, -3:3:30j]
Z = func(X,Y)

ax.plot_wireframe(X, Y, Z)
ax.scatter(x, y, func(x, y), s=50, c='red', marker='D')
plt.show()
