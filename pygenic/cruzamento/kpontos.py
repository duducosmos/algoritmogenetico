#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Cruzamento por k-pontos.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""

from numpy.random import randint, random
from numpy import array

from .cruzamento import Cruzamento, NoCompatibleIndividualSize

class KPontos(Cruzamento):
    """
    Gerador de população via cruzamento usando o operador k-pontos.

    Entrada:
        tamanho_populacao - Tamanho final da população resultante.
    """
    def __init__(self, tamanho_populacao):
        super(KPontos, self).__init__(tamanho_populacao)

    def cruzamento(self, progenitor1, progenitor2):
        """
        Cruzamento via k-pontos de dois indivíduos.

        Entrada:
            ind1 - Primeiro indivíduo
            ind2 - Segundo indivíduo
        O tamanho de ambos os indivíduos deve ser igual, do contrário um erro
        será levantado.
        """
        n1 = len(progenitor1)
        n2 = len(progenitor2)

        if n1 != n2:
            msg = "Tamanho ind1 {0} diferente de ind2 {1}".format(n1, n2)
            raise NoCompatibleIndividualSize(msg)

        desc1 = progenitor1.copy()
        desc2 = progenitor2.copy()

        kp = randint(1, n1-2)

        k = []

        while len(k) <= kp:
            p = randint(1, n1-1)
            if p not in k:
                k.append(p)
        k.sort()

        troca = randint(0, 1)

        for i in range(kp):
            if troca == 0:
                troca = 1
            else:
                troca = 0
                desc1[k[i]:k[i + 1]] = progenitor2[k[i]:k[i + 1]]
                desc2[k[i]:k[i + 1]] = progenitor1[k[i]:k[i + 1]]

        return desc1, desc2
