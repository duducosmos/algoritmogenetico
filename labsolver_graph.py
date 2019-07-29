from numpy import concatenate, hsplit, uint8, ones, array, where
from numpy import array, zeros, where, max, random, count_nonzero, sqrt, abs

import matplotlib.pyplot as plt

from pathos.multiprocessing import ProcessingPool as Pool
from pathos.helpers import cpu_count

from pygenic.populacao import Populacao
from pygenic.selecao.torneio import Torneio
from pygenic.selecao.roleta import Roleta
from pygenic.cruzamento.embaralhamento import Embaralhamento
from pygenic.cruzamento.kpontos import KPontos
from pygenic.mutacao.sequenciareversa import SequenciaReversa
from pygenic.evolucao import Evolucao

from pygenic.tools import bcolors, binarray2int

from labmove import LabMove
from makemaze import make_maze
from numpy import load, save


def _mout_edges(nodes):
    """Find edges using vertices representing xy position vertices."""
    n = nodes.shape[0]
    edges = []
    for i in range(0, n - 1):
        for j in range(i, n):
            if abs(nodes[i, 0] - nodes[j, 0]) > 1:
                break
            elif abs(nodes[i, 0] - nodes[j, 0]) == 1 and \
                 abs(nodes[i, 1] - nodes[j, 1]) == 0:
                 edges.append([i, j])
            elif abs(nodes[i, 0] - nodes[j, 0]) == 0 and \
                 abs(nodes[i, 1] - nodes[j, 1]) == 1:
                 edges.append([i, j])
    return array(edges)

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
    width = 7
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

nlines, ncols = img.shape
tmp = img.copy()
tmp[goal] = 0
print(tmp)
#plt.imshow(tmp, interpolation='none', aspect='auto')
#plt.show()

no_zeros = where(tmp != -1)
nodes = list(zip(no_zeros[0], no_zeros[1]))
nnodes = len(nodes)
nodes = array(nodes)
edges = _mout_edges(nodes)
print("\n")
print(edges)
