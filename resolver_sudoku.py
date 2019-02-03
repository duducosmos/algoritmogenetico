#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Usa algoritmo genético para resolver o sudoku.
"""
from numpy import array, count_nonzero, where, hsplit, concatenate, exp
from sudoku import Sudoku

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
from pygenic.mutacao.ntrocas import NTrocas

from pygenic.evolucao import Evolucao
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def bin(x):
    cnt = array([2 ** i for i in range(x.shape[1])])
    return array([(cnt * x[i,:]).sum()
                  for i in range(x.shape[0])]).reshape(1, x.shape[0])


sudoku = Sudoku()

'''
# Muito Fácil
sudoku.sudoku = array([[0, 0, 0, 6, 0, 3, 1, 7, 0],
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
'''
# Muito Fácil
sudoku.sudoku = array([[0, 0, 7, 0, 0, 1, 8, 0, 0],
                       [0, 3, 0, 2, 6, 7, 9, 0, 5],
                       [0, 0, 2, 8, 5, 9, 7, 3, 4],

                       [0, 0, 4, 0, 7, 8, 3, 0, 9],
                       [0, 1, 0, 0, 0, 2, 4, 0, 0],
                       [0, 0, 0, 6, 4, 0, 0, 0, 0],

                       [3, 2, 0, 9, 8, 0, 1, 0, 7],
                       [0, 4, 1, 3, 2, 5, 0, 9, 8],
                       [9, 0, 5, 0, 0, 6, 2, 4, 3]
                      ])


'''
'''
#Fácil
sudoku.sudoku = array([[0, 0, 0, 0, 9, 0, 2, 0, 0],
                       [0, 5, 0, 1, 6, 0, 0, 4, 0],
                       [6, 0, 2, 4, 0, 0, 5, 0, 0],

                       [0, 0, 0, 0, 0, 0, 3, 6, 0],
                       [4, 7, 0, 0, 0, 0, 0, 5, 9],
                       [0, 1, 8, 0, 0, 0, 0, 0, 0],

                       [0, 0, 3, 0, 0, 9, 8, 0, 7],
                       [0, 8, 0, 0, 2, 7, 0, 3, 0],
                       [0, 0, 5, 0, 8, 0, 0, 0, 0]
                      ])

'''

'''
#Facil
sudoku.sudoku = array([[9, 0, 0, 1, 0, 0, 5, 0, 0],
                       [0, 3, 2, 5, 0, 0, 0, 0, 0],
                       [0, 0, 5, 0, 0, 0, 0, 3, 1],

                       [0, 1, 0, 0, 0, 0, 8, 4, 0],
                       [6, 0, 8, 3, 0, 7, 9, 0, 2],
                       [0, 4, 7, 0, 0, 0, 0, 5, 0],

                       [8, 6, 0, 0, 0, 0, 3, 0, 0],
                       [0, 0, 0, 0, 0, 6, 1, 2, 0],
                       [0, 0, 1, 0, 0, 5, 0, 0, 6]
                      ])
'''
'''
sudoku.sudoku = array([[0, 4, 0, 2, 0, 1, 0, 3, 0],
                       [0, 0, 7, 0, 8, 9, 0, 0, 0],
                       [0, 0, 9, 0, 5, 0, 0, 0, 4],

                       [1, 0, 0, 5, 0, 0, 0, 0, 0],
                       [0, 9, 3, 0, 0, 0, 7, 4, 0],
                       [0, 0, 0, 0, 0, 3, 0, 0, 2],

                       [3, 0, 0, 0, 2, 0, 5, 0, 0],
                       [0, 0, 0, 8, 3, 0, 4, 0, 0],
                       [0, 6, 0, 9, 0, 5, 0, 2, 0]
                      ])
'''

'''
#Dificil
sudoku.sudoku = array([[0, 0, 0, 3, 0, 0, 0, 0, 4],
                       [0, 0, 9, 0, 0, 0, 6, 5, 3],
                       [0, 2, 0, 0, 5, 4, 0, 1, 0],

                       [0, 9, 0, 5, 2, 0, 0, 0, 7],
                       [0, 0, 0, 1, 0, 7, 0, 0, 0],
                       [1, 0, 0, 0, 8, 6, 0, 3, 0],

                       [0, 8, 0, 6, 3, 0, 0, 4, 0],
                       [2, 5, 6, 0, 0, 0, 3, 0, 0],
                       [9, 0, 0, 0, 0, 1, 0, 0, 0]
                      ])
'''

#Muito Dificil para maquina
sudoku.sudoku = array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 3, 0, 8, 5],
                       [0, 0, 1, 0, 2, 0, 0, 0, 0],

                       [0, 0, 0, 5, 0, 7, 0, 0, 0],
                       [0, 0, 4, 0, 0, 0, 1, 0, 0],
                       [0, 9, 0, 0, 0, 0, 0, 0, 0],

                       [5, 0, 0, 0, 0, 0, 0, 7, 3],
                       [0, 0, 2, 0, 1, 0, 0, 0, 0],
                       [0, 0, 0, 0, 4, 0, 0, 0, 9]
                      ])


nozeros = count_nonzero(sudoku.sudoku == 0)

bits = 4

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

        tmp = 10 * sum([sudoku.verificar(num, i, j)
               for num, i, j in data
               ])

        profundidade, ilegais, resposta = sudoku.tentar_preencher()
        if profundidade is not None:
            objetivo = (profundidade + ilegais) / (1e-3 * profundidade + 1.0)
            objetivo += (profundidade + ilegais ** 3) / (ilegais + 1.0)
            tmp += sudoku.perda * int(1000 * objetivo)

        peso.append(tmp)

    peso = array(peso)
    return peso


cromossos_totais = bits * nozeros
tamanho_populacao = 30

populacao = Populacao(avaliacao, cromossos_totais, tamanho_populacao)
selecao = Torneio(populacao, tamanho=int(0.1 * tamanho_populacao))
cruzamento = Embaralhamento(tamanho_populacao)
mutacao = NTrocas(pmut=0.5, bits_por_intervalo=bits)
#mutacao = SequenciaReversa(pmut=0.5)
evolucao = Evolucao(populacao, selecao, cruzamento, mutacao)

evolucao.nsele = int(0.1 * tamanho_populacao)
evolucao.pcruz = 0.1
evolucao.epidemia = 1000
evolucao.manter_melhor = True

convergencia = nozeros

sem_mudancas = 0
ultima_mudanca = -10
t0 = time.time()
solucoes_ruins = []
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

    if convergencia < 15:
        print(sudoku.total_ilegais())

    if len(solucoes_ruins) != 0:
        if populacao.populacao[-1].tolist() in solucoes_ruins:
            print("Repetindo Minimo Local: Reiniciar")
            populacao.gerar_populacao()



    if ultima_mudanca == convergencia:

        sem_mudancas += 1
        if sem_mudancas == 2000:
            print("Minimo Local, Reiniciar")
            solucoes_ruins.append(populacao.populacao[-1].tolist())
            populacao.gerar_populacao()
            sem_mudancas = 0
    else:
        sem_mudancas = 0

    ultima_mudanca = convergencia

    profundidade, ilegais, resposta = sudoku.tentar_preencher()
    print("Para Superficie:{0}, Ilegais:{1}".format(profundidade, ilegais))

    if profundidade == 0:
        tmp = resposta.astype(str)
    else:
        tmp = sudoku.solucao.astype(str)

    ultima_mudanca = convergencia
    print(nozeros - convergencia, nozeros, valor, vmin)
    for k, j in zip(linha, coluna):
        if tmp[k,j] != "0":
            tmp[k,j] = "{0}{1}{2}".format(bcolors.WARNING , tmp[k,j], bcolors.ENDC)

    tmp2 = ""

    for l in range(tmp.shape[0]):
        tmp2 += "|" + ", ".join(tmp[l]) + "|\n"

    print(tmp2)
    print("\n")
    if profundidade == 0:
        break

print("Tempo: ", (time.time() - t0) / 60)
print("\n")
