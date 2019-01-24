#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Roleta de Seleção de Indivíduos para cruzamento.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""

from numpy.random import choice
from numpy import array, where

class Torneio:
    """
    Seleciona indivíduos para cruzamento usando
    Torneio.
    Recebe como entrada:
        populacao - Objeto criado a partir da classe Populacao.
    """
    def __init__(self, populacao, tamanho=10):
        self.populacao = populacao
        self.tamanho = tamanho

    def torneio(self):
        """Retorna o indivíduo campeão da rodada."""
        fitness = self.populacao.avaliar()
        grupo = choice(fitness, size=self.tamanho)
        campeao = grupo.max()
        i = where(fitness == campeao)[0][0]
        return i

    def selecao(self, n):
        """
        Retorna uma população de tamanho n,
        selecionanda via roleta.
        """
        progenitores = array([self.torneio()
                              for _ in range(n)])
        return self.populacao.populacao[progenitores]
