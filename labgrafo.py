#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
'''
Converte Labiritno em um grafo.
'''
from numpy import array, where, random, log
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers
import networkx as nx


class LabGrafo:
    def __init__(self, img):
        self._img = img
        self._nos, self._nome_nos, self._grafo = self._criar_grafo()
        self._caminho = None

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


    def avaliacao(self, individuo, inicio, meta, upcaminho=True):
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
            possibilidades = {ng for ng in  self._grafo.neighbors(atual)}
            possibilidades = list(possibilidades - set(caminho))
            nposs = len(possibilidades)
            if nposs > 1:
                genes = individuo[i0: i0 + nposs]
                escolhido = possibilidades[where(genes == max(genes))[0][0]]
                i0 += nposs
                caminho.append(escolhido)
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
            total += len(caminho) ** 2.0 / 1e9
        else:
            total = 1.0 / len(caminho)

        if upcaminho is True:
            self._caminho = caminho

        return total

    def plot(self, individuo, inicio, meta, geracao=None, save_file=None, interval=100):
        '''
        Gera um vídeo do percurso definido pelos genes de um dado indivíduo.
        '''
        self.avaliacao(individuo, inicio, meta)

        i_fim, j_fim = meta

        fig, ax = plt.subplots()
        img = self._img.copy()

        img[i_fim, j_fim] = 200
        img[img == 0] = 255
        img[img == -1] = 0
        img[inicio] = 0

        im = ax.imshow(img, animated=True, interpolation='none', aspect='auto')

        def updatefig(frame):
            img = self._img.copy()
            img[inicio] = 0
            img[img == 0] = 255
            img[img == -1] = 0
            img[i_fim, j_fim] = 200
            atl = self._nos[self.caminho[frame]]
            img[atl[0], atl[1]] = 100
            if geracao is not None:
                label = "Geração {}".format(geracao)
                ax.set_title(label)
            im.set_array(img)
            return im,

        ani = FuncAnimation(fig,
                            updatefig,
                            frames=len(self.caminho),
                            interval=interval,
                            blit=False)

        if save_file is not None:
            Writer = writers['ffmpeg']
            writer = Writer(fps=29, metadata=dict(artist='Me'), bitrate=1800)
            ani.save(save_file, writer=writer)
        else:
            plt.show()


    @property
    def caminho(self):
        return self._caminho

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
