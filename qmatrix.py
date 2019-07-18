from numpy import array, zeros, where, max, random



class QMatrix:
    def __init__(self, R, alpha=0.8, verbose=False):
        self.R = R
        self.verbose = verbose
        self.Q = zeros(R.shape)
        self.alpha = alpha
        self.epos, self.apos = self._states()
        self._qsteps = R[(self.epos, self.apos)].size
        self.nocon = 1000000000

    @property
    def get_nqsteps(self):
        return self._qsteps

    @property
    def get_states(self):
        return (self.epos, self.apos)

    def random_action(self):

        e = random.choice(self.epos)
        a = random.choice(self.apos[self.epos == e])
        return e, a

    def _states(self):
        return where(self.R != -1)

    def goal(self):
        a, b = where(self.R == max(self.R))
        return b[0]

    def move(self, e, Q=None, verbose=False):
        if self.verbose is True or verbose is True:
            print("Started at {}".format(e))
        if self.Q is None:
            Q = self.Q

        goal = self.goal()
        e = where(Q[e,:] == max(Q[e,:]))[0][0]

        if self.verbose is True or verbose is True:
            print("Moving to {}".format(e))
            print("Goal to {}".format(goal))

        steps = 0
        maxsteps = False

        while e != goal:
            a = e
            e = where(Q[a,:] == max(Q[a,:]))[0][0]
            if self.verbose is True or verbose is True:
                print("Moving from {0} to {1}".format(a, e))
            steps += 1
            if steps >= self._qsteps:
                maxsteps = True
                steps = self._qsteps * self.nocon
                if self.verbose is True or verbose is True:
                    print("not reached")
                break

        return steps


def gen_R(img, diagonal=True):
    path = img.copy()
    path = path.astype(int)
    path[path == 0 ] = -1
    path[path == 255] = 0

    e, a = where(path != -1)
    states = list(zip(e, a))
    goal = states[random.randint(len(states) - 1)]
    n = len(states)
    R = -1 * ones((n, n))
    for i in range(n):
        for j in range(n):
            tmp1 = states[i]
            tmp2 = states[j]
            diffa = abs(tmp1[0] - tmp2[0])
            diffb = abs(tmp1[1] - tmp2[1])
            if diffa <= 1 and diffb <= 1:
                if diffa == 1 and diffb == 1 and diagonal is False:
                    pass
                else:
                    if tmp1 != tmp2:
                        if tmp2 == goal:
                            R[i,j] = 100
                        else:
                            R[i,j] = 0
    return e, a, states, goal, R

if __name__ == "__main__":
    from makemaze import make_maze

    from numpy import concatenate, hsplit, uint8, ones
    import matplotlib.pyplot as plt

    from pygenic.populacao import Populacao
    from pygenic.selecao.torneio import Torneio
    from pygenic.cruzamento.embaralhamento import Embaralhamento
    from pygenic.mutacao.sequenciareversa import SequenciaReversa
    from pygenic.evolucao import Evolucao

    from pygenic.tools import bcolors, binarray2int

    '''
    R = array([[-1, -1, -1, -1, 0, -1],
               [-1, -1, -1, 0, -1, 255],
               [-1, -1, -1, 0, -1, -1],
               [-1, 0, 0, -1, 0, -1],
               [0, -1, -1, 0, -1, 255],
               [-1, 0, -1, -1, 0, 255],
               ])
    '''

    width = 7
    img = array(make_maze(w=width, h=width)).astype(uint8)


    e, a, states, goal, R = gen_R(img)
    print(R[R != -1].size)

    img2 = img.copy()
    img2[goal] = 150



    ql = QMatrix(R, verbose=False)

    tamanho_populacao = 10
    cromossomos = ql.get_nqsteps
    print(cromossomos)

    plt.imshow(img2)
    plt.show()
    print("Number of possibles states: {}".format(e.size))

    tamanho = int(0.1 * tamanho_populacao)
    tamanho = tamanho if tamanho_populacao > 20 else 5
    genes = 4 * cromossomos
    pmut = 0.2
    pcruz = 0.6
    epidemia = None
    elitista = True

    def valores(populacao):
        bx = hsplit(populacao, cromossomos)
        x = [binarray2int(xi) for xi in bx]
        x = concatenate(x).T.astype(int)
        return x

    def avaliacao(populacao):
        x = valores(populacao)
        n = len(populacao)
        peso = []
        es = list(set(ql.get_states[0]))
        e = random.choice(es, int(len(es) * 0.1))
        Q = zeros(R.shape)

        for k in range(n):
            Q[ql.get_states] = x[k, :]
            #steps = ql.move(e, Q=Q)
            steps = 0
            for e in es:
                steps += ql.move(e, Q=Q)

            peso.append(steps)

        peso = -array(peso).astype(int)
        return peso

    populacao = Populacao(avaliacao,
                               genes,
                               tamanho_populacao)

    selecao = Torneio(populacao, tamanho=tamanho)
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


    while True:
        vmin, vmax = evolucao.evoluir()
        print(evolucao.geracao, vmax)
        if vmax > -(ql.nocon):
            break


    x = valores(populacao.populacao)
    Q = zeros(R.shape)
    Q[ql.get_states] = x[-1, :]
    es = list(set(ql.get_states[0]))
    for e in es:
        print("\n")
        ql.move(e, Q=Q, verbose=True)
    print(evolucao.geracao, vmax)
