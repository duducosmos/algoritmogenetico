#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Gerador de Labirinto.
"""
from numpy import zeros, array
from random import shuffle, choice
import matplotlib.pyplot as plt



class GerarLabirinto:
    "Gerador de Labirinto"
    def __init__(self, dimensao):

        dimensao = dimensao + 1 if dimensao % 2 == 0 else dimensao
        self._dimensao = dimensao
        self._mapa = zeros((dimensao, dimensao))
        celulas = array([(2*i +1, 2*j + 1) for i in range((dimensao -1) // 2)
                                           for j in range((dimensao -1) // 2)])
        celulas = (celulas[:,0], celulas[:,1])
        self._mapa[celulas] = 1
        self._celulas = list(zip(celulas[0], celulas[1]))
        self._visitados = []
        self._caminhar(*choice(self._celulas))

    @property
    def mapa(self):
        return self._mapa

    def gerar_novo_mapa(self):
        self._mapa = zeros((dimensao, dimensao))
        self._caminhar(*choice(self._celulas))

    def _caminhar(self, x, y):
        vizinhos = [(x - 2, y), (x + 2, y), (x, y - 2),(x, y + 2)]
        vizinhos = [vi for vi in vizinhos if self._cond(*vi)]
        shuffle(vizinhos)
        self._visitados.append((x, y))
        for (xx, yy) in vizinhos:
            if (xx, yy) not in self._visitados:
                if x == xx:
                    yp = y + 1 if y - yy < 0 else y -1
                    self._mapa[x, yp] = 1
                if y == yy:
                    xp = x +1 if x - xx < 0 else x - 1
                    self._mapa[xp, y] = 1
                self._caminhar(xx, yy)

    def _cond(self, x, y):
        return (x >= 0 and x <= self._dimensao - 1 and
                y >= 0 and y <= self._dimensao - 1 )


if __name__ == "__main__":

    lab = GerarLabirinto(35)
    plt.imshow(lab.mapa)
    plt.show()
