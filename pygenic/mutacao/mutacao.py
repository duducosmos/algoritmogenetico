#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Mutação.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""

from numpy.random import randint, random
from numpy import array


class Mutacao:
    """
    Classe base para operadores de mutação:
    Entrada:
        populacao - vetor de população que deverá sofrer mutação.
        pmut - probabilidade de ocorrer uma mutação.
    """

    def __init__(self, populacao, pmut):
        self.populacao = populacao
        self.pmut = pmut
        self.npop = self.populacao.shape[0]
        self.ngen = self.populacao.shape[1]

    def selecao(self):
        nmut = array([i for i in range(self.npop) if random() < self.pmut])
        return nmut

    def mutacao(self):
        raise NotImplementedError("A ser implementado")
