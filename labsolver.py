from numpy import concatenate, hsplit, uint8, ones, array, where
from numpy import array, zeros, where, max, random, count_nonzero, sqrt, abs

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from pathos.multiprocessing import ProcessingPool as Pool

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




width = 3
img = array(make_maze(w=width, h=width)).astype(int)
print(img)
img[img == 0] = -1
img[img == 255] = 0

s0, s1 = where(img == 0)
options = list(zip(s0.tolist(), s1.tolist()))
goal = options[random.choice(list(range(len(options))))]

img[goal] = 255
print(img)


gs0, s1 = where(img == 0)
options = list(zip(s0.tolist(), s1.tolist()))
startpoint = options[random.choice(list(range(len(options))))]


print(startpoint)
imgview = img.copy()
imgview[goal] = 5
imgview[startpoint] = 5


plt.imshow(imgview)
plt.show()

lm = LabMove(img)

tamanho_populacao = 100
cromossomos = 300

tamanho = int(0.1 * tamanho_populacao)
tamanho = tamanho if tamanho_populacao > 20 else 5
bits = 3
genes = bits * cromossomos
pmut = 0.3
pcruz = 0.5
epidemia = 500
elitista = True

def valores(populacao):
    bx = hsplit(populacao, cromossomos)
    #x = [binarray2int(xi) for xi in bx]
    const = 2 ** bits - 1
    const = (4 -1)/ const
    x = [1 + const * binarray2int(xi) for xi in bx]
    x = concatenate(x).T.astype(int)
    return x

def avaliacao(populacao):
    x = valores(populacao)
    n = len(populacao)
    def steps(k):
        sequence = x[k, :]
        t =  lm.move(startpoint, sequence=sequence)
        return t


    peso = None
    with Pool(4) as pool:
        peso = - array(pool.map(steps, range(n)))

    #peso = - array([steps(k) for k in range(n)])
    return peso

populacao = Populacao(avaliacao,
                           genes,
                           tamanho_populacao)

selecao = Torneio(populacao, tamanho=tamanho)
#selecao = Roleta(populacao)
#cruzamento = KPontos(tamanho_populacao)
cruzamento = Embaralhamento(tamanho_populacao)
mutacao = SequenciaReversa(pmut=pmut)

evolucao = Evolucao(populacao,
                         selecao,
                         cruzamento,
                         mutacao)

evolucao.nsele = tamanho
evolucao.pcruz = pcruz
evolucao.epidemia = epidemia
evolucao.manter_melhor = elitista

'''
for i in range(15000):
    vmin, vmax = evolucao.evoluir()
    print(evolucao.geracao, vmax)
'''

while 1:
    vmin, vmax = evolucao.evoluir()
    print(evolucao.geracao, vmax, vmin)
    vc = vmax
    if vmax >= 0 or evolucao.geracao >= 5000:
        break


x = valores(populacao.populacao)
sequence = x[-1, :]
lm.plot(startpoint, sequence=sequence)
