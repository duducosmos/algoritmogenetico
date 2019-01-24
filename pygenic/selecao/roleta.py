#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Roleta de Seleção de Indivíduos para cruzamento.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""

from numpy.random import random
from numpy import array

class Roleta:
    """
    Seleciona indivíduos para cruzamento usando
    roleta de seleção.
    Recebe como entrada:
        populacao - Objeto criado a partir da classe Populacao.
    """
    def __init__(self, populacao):
        self.populacao = populacao

    def roleta(self):
        """Roleta de seleção de indivíduos."""
        fitness = self.populacao.avaliar()
        fmin = fitness.min()
        fitness = fitness - fmin
        total = fitness.sum()
        parada = total * (1.0 - random())
        parcial = 0
        i = 0
        while True:
            if i > fitness.size - 1:
                break
            parcial += fitness[i]
            if parcial >= parada:
                break
            i += 1
        return i - 1

    def selecao(self, n):
        """
        Retorna uma população de tamanho n,
        selecionanda via roleta.
        """
        progenitores = array([self.roleta()
                              for _ in range(n)])
        return self.populacao.populacao[progenitores]
