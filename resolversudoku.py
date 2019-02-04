#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Usa algoritmo genético para resolver o sudoku.
"""
import sys
from numpy import loadtxt

from sudoku import Sudoku
from solucionarsudoku import SolucionarSudoku

jogo = loadtxt(sys.argv[1], dtype=int, delimiter=",")
sudoku = Sudoku()
sudoku.sudoku = jogo
solucionarsudoku = SolucionarSudoku(sudoku, 4, 30)
solucionarsudoku.inicializar()
solucionarsudoku.solucionar()
