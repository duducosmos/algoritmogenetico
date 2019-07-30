#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
'''
Converte Labiritno em um grafo.
'''
from numpy import array, where, random
import networkx as nx


class LabGrafo:
    def __init__(self, img):
        self._img = img
        self._nos, self._nome_nos, self._grafo = self._criar_grafo()

    def _criar_grafo(self):
        '''
        Gera grafo a partir da matriz imagem, que representa o labirinto.
        Valores iguais a -1 indicam muro.
        '''
        no_zeros = where(self._img != -1)
        nos = list(zip(no_zeros[0], no_zeros[1]))
        nnos = len(nos)
        nos = array(nos)
        vertices = LabGrafo.encontrar_vertices(nos)
        grafo = nx.Graph()
        nome_nos = list(range(nnos - 1))
        grafo.add_nodes_from(nome_nos)
        grafo.add_edges_from(vertices)
        return nos, nome_nos, grafo

    def _no_correspondente(self, pos):
        tmp = self._nos == pos
        cond = (tmp[:,0] == True) & (tmp[:,1] == True)
        nome_no = self._nome_nos[where(cond)[0][0]]
        return nome_no


    def avaliacao(self, individuo, inicio, meta):
        '''
        Dado um indivíduo, verifica se o mesmo representa uma solução
        para o labirinto.
        '''
        partida = self._no_correspondente(inicio)
        fim = self._no_correspondente(meta)
        caminho = [partida]
        atual = partida
        chegou = False
        total = 0
        i0 = 0

        while True:
            possibilidades = {ng for ng in graph.neighbors(atual)}
            possibilidades = list(possibilidades - set(caminho))
            nposs = len(possibilidades)
            if nposs > 1:
                genes = individuo[i0: i0 + nposs]
                escolhido = possibilidades[where(genes == max(genes))[0][0]]
                i0 += nposs
                caminho.append(v)
                atual = escolhido
            elif nposs == 1:
                caminho += possibilidades
                atual = possibilidades[0]
            else:
                break

            if atual == fim:
                chegou = True
                break

        if chegou is False:
            d += 1000
        d += len(path)

        return 1.0 / d


    @property
    def nos(self):
        '''Retorna os nomes dos nós.'''
        return self._nome_nos

    @property
    def nos_ij(self):
        '''
        Retorna o vetor contendo o par que relaciona posição com nó
        na matriz da imagem de entrada.
        '''
        return self._nos

    @property
    def grafo(self):
        '''
        Retorna o grafo que representa os caminhos possíveis no labirinto.
        '''
        return self._grafo

    @staticmethod
    def encontrar_vertices(nos):
        """
        Encontra os vertices nas regiões de movimentos permitidos entre os nós.
        """
        n = nos.shape[0]
        vertices = []
        for i in range(0, n - 1):
            for j in range(i, n):
                if abs(nos[i, 0] - nos[j, 0]) > 1:
                    break
                elif abs(nos[i, 0] - nos[j, 0]) == 1 and \
                     abs(nos[i, 1] - nos[j, 1]) == 0:
                     vertices.append([i, j])
                elif abs(nos[i, 0] - nos[j, 0]) == 0 and \
                     abs(nos[i, 1] - nos[j, 1]) == 1:
                     vertices.append([i, j])
        return array(vertices)

if __name__ == "__main__":
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

    labgrafo = LabGrafo(img)
    ind = random.rand(len(labgrafo.nos))
    labgrafo.avaliacao(ind, startpoint, goal)
