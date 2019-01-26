#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Cruzamento por por um ponto.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""

from numpy.random import randint
from numpy import array

from .cruzamento import Cruzamento, NoCompatibleIndividualSize


class UmPonto(Cruzamento):
    """
    Gerador de população via cruzamento usando o operador de um ponto.

    Entrada:
        tamanho_populacao - Tamanho final da população resultante.
    """
    def __init__(self, tamanho_populacao):
        super(UmPonto, self).__init__(tamanho_populacao)

    def cruzamento(selfself, progenitor1, progenitor2):
        """
        Cruzamento de dois indivíduos via um pontos.

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

        ponto = randint(1, n1 - 1)
        desc1 = progenitor1.copy()
        desc2 = progenitor2.copy()

        desc1[ponto:] = progenitor2[ponto:]
        desc2[ponto:] = progenitor1[ponto:]
        return desc1, desc2
