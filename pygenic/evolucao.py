#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Evolução.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy.random import randint
from numpy import argsort

class Evolucao:
    """
    Usando operadores genéticos, coloca uma população para evoluir.

    Entrada:
        populacao - Objeto do tipo Populacao
        selecao - Objeto do tipo Selecao
        cruzamento - Objeto do tipo cruzamento
        mutacao - Objeto do tipo  Mutacao.
    """

    def __init__(self, populacao, selecao, cruzamento, mutacao):
        self.populacao = populacao
        self.selecao = selecao
        self.cruzamento = cruzamento
        self.mutacao = mutacao
        self.melhor_solucao = None
        self.nsele = None
        self.pcruz = None

    def evoluir(self):
        """
        Evolução Elitista.

        Entrada:
            nsele - subpopulação a ser considerada na seleção.
            prcruz - probabilidade de cruzamento.
            geracoes - Total de geracoes.
        """

        self.populacao.avaliar()

        self.melhor_solucao = self.populacao.populacao[-1].copy()

        subpopulacao = self.selecao.selecao(self.nsele)
        populacao = self.cruzamento.descendentes(subpopulacao, pcruz=self.pcruz)

        self.mutacao.populacao = populacao
        self.mutacao.mutacao()
        self.populacao.populacao[:] = populacao[:]
        self.populacao.populacao[0] = self.melhor_solucao
