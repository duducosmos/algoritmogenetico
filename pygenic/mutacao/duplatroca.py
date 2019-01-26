#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Mutação dupla troca.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""

from numpy.random import randint
from numpy import array

from .mutacao import Mutacao


class DuplaTroca(Mutacao):
    """
    Mutaçao dupla troca.

    Entrada:
        populacao - vetor de população que deverá sofrer mutação.
        pmut - probabilidade de ocorrer uma mutação.
    """
    def __init__(self, pmut):
        super(DuplaTroca, self).__init__(pmut)

    def mutacao(self):
        """Alteração genética de membros da população usando dupla troca."""
        nmut = self.selecao()
        if nmut.size != 0:
            gen1 = array([randint(0, self.ngen - 1) for _ in nmut])
            gen2 = array([randint(0, self.ngen - 1) for _ in nmut])

            self.populacao[nmut, gen1], self.populacao[nmut, gen2] = \
            self.populacao[nmut, gen2], self.populacao[nmut, gen1]
