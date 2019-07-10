#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Classe Abstrada de Seleção de Indivíduos para cruzamento.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""

from numpy.random import random
from numpy import array


class Selecao:
    """
    Seleciona indivíduos para cruzamento.
    Recebe como entrada:
        populacao - Objeto criado a partir da classe Populacao.
    """
    def __init__(self, populacao):
        self.populacao = populacao

    def selecionar(self, fitness=None):
        raise NotImplementedError("A ser implementado")

    def selecao(self, n, fitness=None):
        """
        Retorna uma população de tamanho n,
        selecionanda via roleta.
        """
        progenitores = array([self.selecionar(fitness)
                              for _ in range(n)])
        return self.populacao.populacao[progenitores]
