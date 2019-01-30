from numpy import zeros, array, split, hsplit, where, count_nonzero, concatenate
from numpy.random import randint, choice, shuffle
import random

BONUS = 1
PERDA = -5

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


    @property
    def sudoku(self):
        return self._sudoku

    def quadrante(self, numero, linha, coluna, valorlc):
        tmp = split(self.solucao, 3)
        quad = []

        for sub in tmp:
            sub2 = split(sub, 3, axis=1)
            tmp2 = []
            for sub3 in sub2:
                tmp2.append(sub3.tolist())
            quad.append(tmp2)

        quad = array(quad)
        subquad = quad[int(linha / 3), int(coluna / 3)]

        repeticoes = count_nonzero(subquad == numero)
        nzeros = count_nonzero(subquad == 0)

        if repeticoes != 0:
            return PERDA * repeticoes * 100

        if valorlc < 0:
            sudo_linha = count_nonzero(self.sudoku[linha,:] == numero)
            sudo_coluna = count_nonzero(self.sudoku[:,coluna] == numero)
            p = 0

            if sudo_linha != 0:
                p += 1

            if sudo_coluna != 0:
                p += 1

            if p == 0:
                return PERDA * 10

            return PERDA * p

        if nzeros == 1:
            return BONUS * 100

        return BONUS * 3


    def verificar(self, numero, linha, coluna):
        if numero < 1 or numero > 9:
            return -1000000000

        valorlc = PERDA * count_nonzero(self.solucao[linha,:] == numero)
        valorlc += PERDA * count_nonzero(self.solucao[:,coluna] == numero)
        valorlc += self.quadrante(numero, linha, coluna, valorlc)
        if valorlc > 0:
            self.solucao[linha, coluna] = numero

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


            restante =  count_nonzero(sudoku.sudoku == 0)
            restante -= count_nonzero(sudoku.solucao == 0)
            tmp -= restante
            peso.append(tmp)
        peso = array(peso)
        return peso


    cromossos_totais = bits * nozeros
    tamanho_populacao = 30

    populacao = Populacao(avaliacao, cromossos_totais, tamanho_populacao)
    selecao = Torneio(populacao, tamanho=int(0.1 * tamanho_populacao))
    cruzamento = KPontos(tamanho_populacao)
    mutacao = DuplaTroca(pmut=0.1)
    evolucao = Evolucao(populacao, selecao, cruzamento, mutacao)

    evolucao.nsele = int(0.1 * tamanho_populacao)
    evolucao.pcruz = 0.6
    evolucao.epidemia = 100
    evolucao.manter_melhor = True

    convergencia = nozeros


    while convergencia > 0:
        valor, vmin = evolucao.evoluir()
        print(evolucao.geracao)

        sudoku.solucao = sudoku.sudoku.copy()
        p = populacao.populacao[-1] == solucao
        v = valores(populacao.populacao)[-1]
        linha, coluna = where(sudoku.solucao==0)
        data = list(zip(v, linha, coluna))
        for n, k, j in data:
            sudoku.verificar(n, k, j)

        tmp = sudoku.solucao.astype(str)
        convergencia = count_nonzero(sudoku.solucao == 0)
        print(nozeros - convergencia, nozeros, valor, vmin)
        for k, j in zip(linha, coluna):
            if tmp[k,j] != "0":
                tmp[k,j] = "{0}{1}{2}".format(bcolors.WARNING , tmp[k,j], bcolors.ENDC)

        tmp2 = ""

        for l in range(tmp.shape[0]):
            tmp2 += "|" + ", ".join(tmp[l]) + "|\n"

        print(tmp2)
        print("\n")
    print("".join(solucao.astype(str)))
