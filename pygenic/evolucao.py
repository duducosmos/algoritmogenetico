#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Evolução.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""


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
        self._melhor_solucao = None
        self._geracao = 0
        self._nsele = None
        self._pcruz = None

    def _set_nsele(self, nsele):
        self._nsele = nsele

    def _get_nsele(self):
        return self._nsele

    def _set_pcruz(self, pcruz):
        self._pcruz = pcruz

    def _get_pcruz(self):
        return self._pcruz

    @property
    def melhor_solucao(self):
        return self._melhor_solucao

    @property
    def geracao(self):
        return self._geracao

    def evoluir(self):
        """
        Evolução elitista, por uma geração, da popução.
        """
        self.populacao.avaliar()
        self._melhor_solucao = self.populacao.populacao[-1].copy()

        subpopulacao = self.selecao.selecao(self._nsele)
        populacao = self.cruzamento.descendentes(subpopulacao, pcruz=self._pcruz)

        self.mutacao.populacao = populacao
        self.mutacao.mutacao()
        self.populacao.populacao[:] = populacao[:]
        self.populacao.populacao[0] = self._melhor_solucao
        valores = self.populacao.avaliar()

        self._geracao += 1
        return valores[-1], self.populacao.populacao[-1].copy()

    nsele = property(_get_nsele, _set_nsele)
    pcruz = property(_get_pcruz, _set_pcruz)
