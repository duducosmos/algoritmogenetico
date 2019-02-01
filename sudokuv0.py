from numpy import zeros, array, split, hsplit, where, count_nonzero, concatenate
from numpy import isin
from numpy.random import randint, choice, shuffle
import random

BONUS = 1
PERDA = -1

class Sudoku:
    def __init__(self):

        self._sudoku = array([[0, 0, 0, 6, 0, 3, 1, 7, 0],
                              [0, 7, 0, 4, 1, 0, 0, 3, 8],
                              [4, 0, 1, 7, 5, 0, 0, 6, 2],

                              [0, 8, 0, 3, 0, 0, 2, 1, 0],
                              [0, 9, 6, 2, 4, 1, 0, 8, 5],
                              [1, 0, 7, 0, 0, 0, 3, 4, 6],

                              [9, 4, 2, 1, 3, 0, 0, 5, 0],
                              [0, 1, 0, 0, 7, 0, 6, 0, 0],
                              [7, 6, 3, 0, 0, 5, 4, 0, 0]
                              ])
        '''
        self._sudoku = array([[0, 0, 0, 4, 0, 9, 0, 0, 0],
                              [0, 0, 4, 7, 3, 0, 0, 0, 0],
                              [0, 5, 0, 0, 0, 0, 9, 0, 0],

                              [1, 0, 0, 9, 0, 8, 0, 4, 0],
                              [7, 0, 9, 0, 2, 0, 5, 0, 6],
                              [0, 8, 0, 5, 0, 4, 0, 0, 3],

                              [0, 0, 8, 0, 0, 0, 0, 7, 0],
                              [0, 0, 0, 0, 5, 7, 6, 0, 0],
                              [0, 0, 0, 1, 0, 2, 0, 0, 0]
                              ])
        '''



        self.solucao = None
        self._possiveis = array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self._quadrante_linha = {0:0, 1:3, 2:6}
        self._quadrante_coluna = {0:0, 1:3, 2:6}


    @property
    def sudoku(self):
        return self._sudoku

    def finalizar_quadrante(self):
        """Usar quando faltar menos de 5 pontos para finalizar"""
        qij = [[0,0], [0,1], [0, 2],
               [1,0], [1,1], [1, 2],
               [2,0], [2,1], [2, 2]
              ]

        for x, y in qij:
            quadrante = self.obter_quadrante(x, y)
            l0 = self._quadrante_linha[x]
            c0 = self._quadrante_coluna[y]
            linhas, colunas = where(quadrante == 0)
            if linhas.size != 0:
                linhas = linhas + l0
                colunas = colunas + c0
                testar = self._possiveis[~isin(self._possiveis, quadrante)]
                if testar.size != 0:
                    ij = list(zip(linhas, colunas))
                    for numero in testar:
                        for i,j in ij:
                            a = count_nonzero(self.solucao[i, :] == numero)
                            b = count_nonzero(self.solucao[:, j] == numero)
                            if a == 0 and b == 0:
                                self.solucao[i, j] = numero

    def teste_ilegalidade(self, x, y):
        quadrante = self.obter_quadrante(x, y)
        l0 = self._quadrante_linha[x]
        c0 = self._quadrante_coluna[y]

        linhas, colunas = where(quadrante == 0)
        if linhas.size != 0:
            linhas = linhas + l0
            colunas = colunas + c0
            testar = self._possiveis[~isin(self._possiveis, quadrante)]
            ij = list(zip(linhas, colunas))

            invalidas = 0
            for numero in testar:
                tmp = 0
                for i,j in ij:
                    a = count_nonzero(self.solucao[i, :] == numero)
                    b = count_nonzero(self.solucao[:, j] == numero)
                    if a != 0 or b != 0:
                        tmp += 1

                if tmp == len(ij):
                    invalidas += 1

            return invalidas
        return 0

    def obter_quadrante(self, x, y):
        tmp = split(self.solucao, 3)
        quad = []

        for sub in tmp:
            sub2 = split(sub, 3, axis=1)
            tmp2 = []
            for sub3 in sub2:
                tmp2.append(sub3.tolist())
            quad.append(tmp2)
        quad = array(quad)
        subquad = quad[x, y]
        return subquad



    def quadrante(self, numero, linha, coluna, valorlc):

        x, y = (int(linha / 3), int(coluna / 3))
        subquad = self.obter_quadrante(x, y)

        repeticoes = count_nonzero(subquad == numero)
        nzeros = count_nonzero(subquad == 0)

        if repeticoes != 0:
            return PERDA * 3

        if valorlc < 0:
            sudo_linha = count_nonzero(self.sudoku[linha,:] == numero)
            sudo_coluna = count_nonzero(self.sudoku[:,coluna] == numero)

            if sudo_linha != 0 or sudo_coluna != 0:
                return PERDA * 3
            return PERDA

        return BONUS


    def verificar(self, numero, linha, coluna):
        if numero < 1 or numero > 9:
            return -1000000000

        valorlc = PERDA * count_nonzero(self.solucao[linha,:] == numero)
        valorlc += PERDA * count_nonzero(self.solucao[:,coluna] == numero)
        valorlc += self.quadrante(numero, linha, coluna, valorlc)

        if valorlc > 0:
            self.solucao[linha, coluna] = numero
            return BONUS

        return valorlc


def bin(x):
    cnt = array([2 ** i for i in range(x.shape[1])])
    return array([(cnt * x[i,:]).sum() for i in range(x.shape[0])]).reshape(1, x.shape[0])

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == "__main__":

    import os
    from pygenic.populacao import Populacao
    from pygenic.selecao.torneio import Torneio
    from pygenic.selecao.roleta import Roleta
    from pygenic.selecao.classificacao import Classificacao


    from pygenic.cruzamento.kpontos import KPontos
    from pygenic.cruzamento.embaralhamento import Embaralhamento
    from pygenic.cruzamento.umponto import UmPonto

    from pygenic.mutacao.sequenciareversa import SequenciaReversa
    from pygenic.mutacao.flip import Flip
    from pygenic.mutacao.duplatroca import DuplaTroca

    from pygenic.evolucao import Evolucao

    sudoku = Sudoku()
    print(sudoku.sudoku)
    input("Enter")

    nozeros = count_nonzero(sudoku.sudoku == 0)

    bits = 6

    def valores(populacao):
        bx = hsplit(populacao, nozeros)

        const = 2 ** bits - 1
        const = (10 - 1) / const
        x = [1 + const * bin(xi) for xi in bx]
        x = concatenate(x).T.astype(int)
        return x

    def avaliacao(populacao):
        linhas, colunas = where(sudoku.sudoku == 0)
        x = valores(populacao)

        peso = []
        for k in range(len(populacao)):
            sudoku.solucao = sudoku.sudoku.copy()
            y = x[k,:].copy()
            data = list(zip(y, linhas, colunas))

            tmp = sum([sudoku.verificar(num, i, j)
                   for num, i, j in data
                   ])

            qij = [[0,0], [0,1], [0, 2],
                   [1,0], [1,1], [1, 2],
                   [2,0], [2,1], [2, 2]
                  ]

            ilegais = sum([sudoku.teste_ilegalidade(xy[0], xy[1]) for xy in qij])
            tmp += PERDA * ilegais * 100000

            restante = count_nonzero(sudoku.solucao == 0)

            if restante < 10:
                sudoku.finalizar_quadrante()
                restante = count_nonzero(sudoku.solucao == 0)
                if restante != 0:
                    tmp += PERDA * 100

            peso.append(tmp)

        peso = array(peso)
        return peso


    cromossos_totais = bits * nozeros
    tamanho_populacao = 40

    populacao = Populacao(avaliacao, cromossos_totais, tamanho_populacao)
    selecao = Torneio(populacao, tamanho=int(0.3 * tamanho_populacao))
    cruzamento = Embaralhamento(tamanho_populacao)
    mutacao = SequenciaReversa(pmut=0.1)
    evolucao = Evolucao(populacao, selecao, cruzamento, mutacao)

    evolucao.nsele = int(0.1 * tamanho_populacao)
    evolucao.pcruz = 0.4
    evolucao.epidemia = 50
    evolucao.manter_melhor = True

    convergencia = nozeros


    while convergencia > 0:
        valor, vmin = evolucao.evoluir()
        print(evolucao.geracao)

        sudoku.solucao = sudoku.sudoku.copy()
        v = valores(populacao.populacao)[-1]
        linha, coluna = where(sudoku.solucao==0)
        data = list(zip(v, linha, coluna))
        for n, k, j in data:
            sudoku.verificar(n, k, j)

        convergencia = count_nonzero(sudoku.solucao == 0)

        if convergencia < 10:
            sudoku.finalizar_quadrante()
            convergencia = count_nonzero(sudoku.solucao == 0)

        tmp = sudoku.solucao.astype(str)
        print(nozeros - convergencia, nozeros, valor, vmin)
        for k, j in zip(linha, coluna):
            if tmp[k,j] != "0":
                tmp[k,j] = "{0}{1}{2}".format(bcolors.WARNING , tmp[k,j], bcolors.ENDC)

        tmp2 = ""

        for l in range(tmp.shape[0]):
            tmp2 += "|" + ", ".join(tmp[l]) + "|\n"

        print(tmp2)
        print("\n")
