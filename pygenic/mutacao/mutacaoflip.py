#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Mutação flip.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""

from numpy.random import randint
from numpy import array

from .mutacao import Mutacao


class Mutacaoflip(Mutacao):
    """
    Mutaçao flip.

    Entrada:
        populacao - vetor de população que deverá sofrer mutação.
        pmut - probabilidade de ocorrer uma mutação.
    """
    def __init__(self, populacao, pmut):
        super(Mutacaoflip, self).__init__(populacao, pmut)

    def mutacao(self):
        """Alteração genética de membros da população usando mutação flip."""
        nmut = self.selecao()
        genflip = array([randint(0, self.ngen - 1) for _ in nmut])
        self.populacao[nmut, genflip] = 1-self.populacao[nmut, genflip]
