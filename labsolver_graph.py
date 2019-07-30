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
import networkx as nx
import time
import os


def mout_edges(nodes):
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

def create_graph(img):
    no_zeros = where(img != -1)
    nodes = list(zip(no_zeros[0], no_zeros[1]))
    nnodes = len(nodes)
    nodes = array(nodes)
    edges = mout_edges(nodes)
    graph = nx.Graph()
    nodes_names = list(range(nnodes - 1))
    graph.add_nodes_from(nodes_names)
    graph.add_edges_from(edges)
    return nodes, nodes_names, graph

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
    width = 25
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


nodes, nodes_names, graph = create_graph(img)

def avaliacao(ind):
    a = nodes == startpoint
    start = nodes_names[where((a[:,0] == True) & (a[:,1] == True))[0][0]]
    a = nodes == goal
    end = nodes_names[where((a[:,0] == True) & (a[:,1] == True))[0][0]]
    path = [start]
    current = start
    chegou = False
    d = 0
    i0 = 0

    while True:
        possibles = {ng for ng in graph.neighbors(current)}
        possibles = list(possibles - set(path))
        nposs = len(possibles)
        if nposs > 0:
            vs = ind[i0: i0 + nposs]
            v = possibles[where(vs == max(vs))[0][0]]
            i0 += nposs
            path.append(v)
            current = v
            if current == end:
                chegou = True
                break
        else:
            break

    if chegou is False:
        d += 1000
    d += len(path)

    return 1.0 / d

for i in range(1):
    ind = random.rand(len(nodes_names))
    avaliacao(ind)
