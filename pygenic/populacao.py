#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Gerador aleatório de população.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""

from numpy.random import randint
from numpy import argsort

class Populacao:
    """
    Cria e avalia uma população.
    Recebe como entrada:
        avaliacao - Função que recebe um indivíduo como entrada e retorna
                    um valor numérico.
        cromossos_totais - Numero inteiro representando o tamanho da cadeia
                           genética do indivíduo.
        tamanho_populacao - Numero inteiro representando o número total de
                            indivíduos na população.
    """

    def __init__(self, avaliacao, genes_totais, tamanho_populacao):
        self.avaliacao = avaliacao
        self.genes_totais = genes_totais
        self.tamanho_populacao = tamanho_populacao
        self.gerar_populacao()

    def gerar_populacao(self):
        """Gerador aleatório de população."""
        self.populacao = randint(0, 2, size=(self.tamanho_populacao,
                                             self.genes_totais),
                                             dtype='b')
    def avaliar(self):
        """Avalia e ordena a população."""
        valores = self.avaliacao(self.populacao)
        ind = argsort(valores)
        self.populacao[:] = self.populacao[ind]
        valores = valores[ind]
        return valores[ind]
