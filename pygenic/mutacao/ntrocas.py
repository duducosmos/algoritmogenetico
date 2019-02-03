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


class NTrocas(Mutacao):
    """
    Mutaçao dupla troca.

    Entrada:
        populacao - vetor de população que deverá sofrer mutação.
        pmut - probabilidade de ocorrer uma mutação.
    """
    def __init__(self, pmut, bits_por_intervalo):
        super(NTrocas, self).__init__(pmut)
        self.bits_por_intervalo = bits_por_intervalo

    def mutacao(self, ):
        """Alteração genética de membros da população usando dupla troca."""
        nmut = self.selecao()
        cromossos_totais = self.populacao[0].size

        if nmut.size != 0:
            intervalos = [[i, i + self.bits_por_intervalo]
                           for i in range(0,
                                          cromossos_totais,
                                          self.bits_por_intervalo
                                          )
                          ]
            ninter = len(intervalos)


            for i in nmut:
                inter1 = intervalos[randint(0, ninter)]
                inter2 = intervalos[randint(0, ninter)]

                while inter1 == inter2:
                    inter2 = intervalos[randint(0, ninter)]

                self.populacao[nmut,inter1[0]:inter1[1]], \
                self.populacao[nmut,inter2[0]:inter2[1]] = \
                self.populacao[nmut,inter2[0]:inter2[1]][::-1], \
                self.populacao[nmut,inter1[0]:inter1[1]][::-1]
