from numpy import zeros, array, split, hsplit, where, count_nonzero, concatenate
from numpy.random import randint, choice
import random

BONUS = 1000

class Sudoku:
    def __init__(self):
        self._sudoku = zeros((9,9), dtype=int)
        self._window = array([[0, 1, 2], []])

    @property
    def sudoku(self):
        return self._sudoku

    def quadrante(self, numero, linha, coluna):
        tmp = split(self._sudoku, 3)
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
            return -1000 * c
        return BONUS


    def verificar(self, numero, linha, coluna):
        if numero < 1 or numero > 9:
            return -1000000000

        tmp = -1000 * count_nonzero(self._sudoku[linha,:] == numero)
        tmp += -1000 * count_nonzero(self._sudoku[:,coluna] == numero)
        tmp += self.quadrante(numero, linha, coluna)
        return tmp


    def gerador(self):
        for numero in range(1,10):
            repeticoes = 5
            linha = randint(0, 8)
            coluna = randint(0, 8)
            cont = 0
            while  cont < repeticoes:
                if self.verificar(numero, linha, coluna) == BONUS:
                    cont += 1
                    self._sudoku[linha, coluna] = numero
                linha = randint(0, 8)
                coluna = randint(0, 8)

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
    from pygenic.populacao import Populacao
    from pygenic.selecao.torneio import Torneio
    from pygenic.selecao.roleta import Roleta

    from pygenic.cruzamento.kpontos import KPontos
    from pygenic.cruzamento.embaralhamento import Embaralhamento

    from pygenic.mutacao.sequenciareversa import SequenciaReversa
    from pygenic.mutacao.flip import Flip

    from pygenic.evolucao import Evolucao

    sudoku = Sudoku()
    sudoku.gerador()
    print(sudoku.sudoku)
    input("Enter")

    nozeros = count_nonzero(sudoku.sudoku == 0)

    def valores(populacao):
        bx = hsplit(populacao, nozeros)
        #const = 15
        #const = (9 - 1) / const
        x = [1 + bin(xi) for xi in bx]
        x = concatenate(x).T.astype(int)
        return x

    def avaliacao(populacao):
        linhas, colunas = where(sudoku.sudoku == 0)

        x = valores(populacao)

        peso = []
        for k in range(len(populacao)):
            tmp = sum([sudoku.verificar(num, i, j)
                   for num, i, j in zip(x[k,:], linhas, colunas)
                   ])
            peso.append(tmp)
        peso = array(peso)
        return peso


    cromossos_totais = 4 * nozeros
    tamanho_populacao = 50

    populacao = Populacao(avaliacao, cromossos_totais, tamanho_populacao)
    selecao = Torneio(populacao)
    cruzamento = Embaralhamento(tamanho_populacao)
    mutacao = SequenciaReversa(pmut=0.2)
    evolucao = Evolucao(populacao, selecao, cruzamento, mutacao)

    evolucao.nsele = int(0.1 * tamanho_populacao)
    evolucao.pcruz = 0.6


    for i in range(10000):
        valor, solucao = evolucao.evoluir()
        print(evolucao.geracao)
        print(valor, nozeros, nozeros - int((nozeros*BONUS - valor)/ BONUS))
        if evolucao.geracao % 10 == 0:
            tmp = sudoku.sudoku.copy()
            p = populacao.populacao[-1] == solucao
            v = valores(populacao.populacao)[-1]
            linha, coluna = where(tmp==0)
            tmp = tmp.astype(str)
            for n, k, j in zip(v, linha, coluna):
                tmp[k,j] = "{0}{1}{2}".format(bcolors.WARNING , n, bcolors.ENDC)

            tmp2 = ""

            for l in range(tmp.shape[0]):
                tmp2 += "|" + ", ".join(tmp[l]) + "|\n"

            print(tmp2)
            print("\n")
