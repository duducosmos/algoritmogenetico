from numpy import zeros, array, split, hsplit, where, count_nonzero, concatenate
from numpy.random import randint, choice, shuffle
import random

BONUS = 1
PERDA = -1

class Sudoku:
    def __init__(self):

        self._sudoku = array([[0, 0, 9, 5, 3, 0, 8, 0, 0],
                              [0, 3, 1, 7, 4, 0, 0, 9, 0],
                              [8, 7, 0, 0, 6, 0, 3, 2, 0],

                              [7, 9, 0, 4, 0, 0, 1, 8, 5],
                              [4, 1, 0, 0, 5, 6, 7, 3, 0],
                              [0, 0, 0, 9, 1, 0, 0, 6, 2],

                              [0, 2, 3, 6, 0, 0, 0, 1, 8],
                              [1, 0, 0, 0, 9, 0, 6, 4, 3],
                              [0, 6, 4, 3, 8, 1, 0, 0, 0]
                              ])
        '''
        self._sudoku = array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 3, 0, 8, 5],
                              [0, 0, 1, 0, 2, 0, 0, 0, 0],

                              [0, 0, 0, 5, 0, 7, 0, 0, 0],
                              [0, 0, 4, 0, 0, 0, 1, 0, 0],
                              [0, 9, 0, 0, 0, 0, 0, 0, 0],

                              [5, 0, 0, 0, 0, 0, 0, 7, 3],
                              [0, 0, 2, 0, 1, 0, 0, 0, 0],
                              [0, 0, 0, 0, 4, 0, 0, 0, 9]
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
        c = count_nonzero(subquad == numero)
        if c != 0:
            return PERDA * c

        nzeros = count_nonzero(subquad == 0)
        if nzeros == 1:
            if valorlc < 0:
                return PERDA * 100
            else:
                return BONUS * 50

        return BONUS


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

    bits = 32

    def valores(populacao):
        bx = hsplit(populacao, nozeros)

        const = 2 ** bits - 1
        const = (9 - 1) / const
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

            convergencia = 10 * count_nonzero(sudoku.solucao == 0)
            tmp -= convergencia
            peso.append(tmp)
        peso = array(peso)
        return peso


    cromossos_totais = bits * nozeros
    tamanho_populacao = 50

    populacao = Populacao(avaliacao, cromossos_totais, tamanho_populacao)
    selecao = Torneio(populacao, tamanho=5)
    cruzamento = KPontos(tamanho_populacao)
    mutacao = DuplaTroca(pmut=0.1)
    evolucao = Evolucao(populacao, selecao, cruzamento, mutacao)

    evolucao.nsele = int(0.1 * tamanho_populacao)
    evolucao.pcruz = 0.6

    convergencia = nozeros


    while convergencia > 0:
        valor, solucao = evolucao.evoluir()
        os.system("clear")
        print(evolucao.geracao)
        print(valor, nozeros)
        sudoku.solucao = sudoku.sudoku.copy()
        p = populacao.populacao[-1] == solucao
        v = valores(populacao.populacao)[-1]
        linha, coluna = where(sudoku.solucao==0)
        data = list(zip(v, linha, coluna))
        #shuffle(data)
        for n, k, j in data:
            sudoku.verificar(n, k, j)

        tmp = sudoku.solucao.astype(str)
        convergencia = count_nonzero(sudoku.solucao == 0)
        print(nozeros - convergencia)
        for k, j in zip(linha, coluna):
            if tmp[k,j] != "0":
                tmp[k,j] = "{0}{1}{2}".format(bcolors.WARNING , tmp[k,j], bcolors.ENDC)

        tmp2 = ""

        for l in range(tmp.shape[0]):
            tmp2 += "|" + ", ".join(tmp[l]) + "|\n"

        print(tmp2)
        print("\n")
    print("".join(solucao.astype(str)))
