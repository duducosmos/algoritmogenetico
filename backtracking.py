#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Usa força bruta para resolver o sudoku.
"""
from sudoku import Sudoku
import os
import time
from numpy import array, where

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

sudoku = Sudoku()

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


#Muito Dificil
sudoku.sudoku = array([[0, 0, 7, 0, 4, 9, 3, 1, 0],
                       [0, 4, 0, 1, 8, 0, 0, 0, 0],
                       [0, 0, 5, 0, 0, 6, 0, 0, 4],

                       [0, 0, 0, 0, 0, 8, 0, 0, 2],
                       [0, 0, 3, 0, 0, 0, 1, 0, 0],
                       [5, 0, 0, 4, 0, 0, 0, 0, 0],

                       [3, 0, 0, 6, 0, 0, 8, 0, 0],
                       [0, 0, 0, 0, 9, 1, 0, 6, 0],
                       [0, 6, 9, 8, 5, 0, 4, 0, 0]
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

sudoku.solucao = sudoku.sudoku.copy()
linha, coluna = where(sudoku.solucao==0)
licol = list(zip(linha, coluna))
l = 0
t0 = time.time()
while l < len(licol):
    encaixou = 0
    i, j = licol[l][0], licol[l][1]
    inicio = sudoku.solucao[i, j]
    sudoku.solucao[i, j] = 0
    for numero in range(inicio + 1,10):
        encaixou = sudoku.verificar(numero, i, j)
        if encaixou > 0:
            break
            
    if encaixou > 0:
        l = l + 1
    else:
        l = l - 1

    tmp = sudoku.solucao.astype(str)
    for i, j in licol:
        if tmp[i,j] != "0":
            tmp[i,j] = "{0}{1}{2}".format(bcolors.WARNING , tmp[i,j], bcolors.ENDC)

    tmp2 = ""

    for k in range(tmp.shape[0]):
        tmp2 += "|" + ", ".join(tmp[k]) + "|\n"

    #time.sleep(0.01)
    #os.system("clear")

    print(tmp2)
    print("\n")
print("Tempo: ", (time.time() - t0) / 60)
