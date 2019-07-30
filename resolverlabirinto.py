#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
'''
Resolver Labirinto
'''


from numpy import load, save, where, array, random, hsplit, concatenate
from pathos.multiprocessing import ProcessingPool as Pool
from pathos.helpers import cpu_count
import matplotlib.pyplot as plt

from pygenic.populacao import Populacao
from pygenic.selecao.torneio import Torneio
from pygenic.selecao.roleta import Roleta
from pygenic.cruzamento.embaralhamento import Embaralhamento
from pygenic.cruzamento.kpontos import KPontos
from pygenic.mutacao.sequenciareversa import SequenciaReversa
from pygenic.evolucao import Evolucao

from pygenic.tools import bcolors, binarray2int

from labgrafo import LabGrafo
from makemaze import make_maze

loadorsave = input("Carregar ou Salvar [c/s]: ")
filname = "./labirinto_grap.npy"

if loadorsave == "c":
    img = load(filname)
    goal = where(img == 255)
    goal = (goal[0][0], goal[1][0])
    startpoint = where(img == 100)
    img[startpoint] = 0
    startpoint = (startpoint[0][0], startpoint[1][0])
    s0, s1 = where(img == 0)
    options = list(zip(s0.tolist(), s1.tolist()))

else:
    width = 20
    img = array(make_maze(w=width, h=width)).astype(int)
    img[img == 0] = -1
    img[img == 255] = 0

    s0, s1 = where(img == 0)
    options = list(zip(s0.tolist(), s1.tolist()))
    goal = options[random.choice(list(range(len(options))))]

    img[goal] = 255

    s0, s1 = where(img == 0)
    options = list(zip(s0.tolist(), s1.tolist()))
    startpoint = options[random.choice(list(range(len(options))))]
    img[startpoint] = 100
    print(startpoint)
    save(filname, img)

img2 = img.copy()
img2[goal] = 200
img2[img2 == 0] = 255
img2[img2 == -1] = 0
img2[startpoint] = 100
plt.imshow(img2)
plt.show()

labgrafo = LabGrafo(img)

tamanho_populacao = 100
cromossomos = len(labgrafo.nos)
tamanho = int(0.1 * tamanho_populacao)
bits = 4
genes = bits * cromossomos
pmut = 0.1
pcruz = 0.6
epidemia = 25
elitista = True

def valores(populacao):
    bx = hsplit(populacao, cromossomos)
    #x = [binarray2int(xi) for xi in bx]
    const = 2 ** bits - 1
    const = 100 / const
    x = [const * binarray2int(xi) for xi in bx]
    x = concatenate(x).T.astype(int)
    return x

def avaliacao(populacao):
    x = valores(populacao)
    n = len(populacao)

    def steps(k):
        individuo = x[k, :]
        t =  labgrafo.avaliacao(individuo, startpoint, goal, upcaminho=False)
        return t

    peso = None
    ncpu = cpu_count()
    with Pool(ncpu) as pool:
        peso = array(pool.map(steps, range(n)))

    #peso = array([steps(k) for k in range(n)])
    return peso

populacao = Populacao(avaliacao,
                           genes,
                           tamanho_populacao)

selecao = Torneio(populacao, tamanho=tamanho)
cruzamento = KPontos(tamanho_populacao)
mutacao = SequenciaReversa(pmut=pmut)

evolucao = Evolucao(populacao,
                         selecao,
                         cruzamento,
                         mutacao)

evolucao.nsele = tamanho
evolucao.pcruz = pcruz
evolucao.manter_melhor = elitista
evolucao.epidemia = epidemia

for i in range(100):
    vmin, vmax = evolucao.evoluir()
    print(evolucao.geracao, vmax, vmin)

x = valores(populacao.populacao)
individuo = x[-1, :]
print("Gerando Video")
labgrafo.plot(individuo, startpoint, goal, save_file="./videos/lab.mp4")
