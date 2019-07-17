from numpy import array, zeros, where, max, random

class QMatrix:
    def __init__(self, R, alpha=0.8, verbose=False):
        self.R = R
        self.verbose = verbose
        self.Q = zeros(R.shape)
        self.alpha = alpha
        self.epos, self.apos = self._states()
        self._qsteps = epos.size

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

    def move(self, e, Q=None):
        if self.verbose:
            print("Started at {}".format(e))
        if self.Q is None:
            Q = self.Q

        moviments = [e]

        goal = self.goal()
        e = where(self.Q[e,:] == max(self.Q[e,:]))[0][0]
        moviments.append(e)

        if self.verbose:
            print("Moving to {}".format(e))

        steps = 0

        while e != goal:
            a = e
            e = where(self.Q[a,:] == max(self.Q[a,:]))[0][0]
            moviments.append(e)

            if self.verbose:
                print("Moving from {0} to {1}".format(a, e))
            steps += 1
            if stpes >= self._qsteps:
                break
        if self.verbose:
            print("The goal was reached...")
        return moviments

if __name__ == "__main__":
    from numpy import concatenate, hsplit

    from pygenic.populacao import Populacao
    from pygenic.selecao.torneio import Torneio
    from pygenic.cruzamento.embaralhamento import Embaralhamento
    from pygenic.mutacao.sequenciareversa import SequenciaReversa
    from pygenic.evolucao import Evolucao

    from pygenic.tools import bcolors, binarray2int


    R = array([[-1, -1, -1, -1, 0, -1],
               [-1, -1, -1, 0, -1, 255],
               [-1, -1, -1, 0, -1, -1],
               [-1, 0, 0, -1, 0, -1],
               [0, -1, -1, 0, -1, 255],
               [-1, 0, -1, -1, 0, 255],
               ])

    ql = QLearning(R)

    tamanho_populacao = 50
    cromossomos = ql.get_qsteps()

    tamanho = int(0.1 * tamanho_populacao)
    genes = 8 * cromossomos

    def valores(populacao, cromossomos):
        bx = hsplit(populacao, cromossomos)
        x = [binarray2int(xi) for xi in bx]
        x = concatenate(x).T.astype(int)
        return x

    def avaliacao(populacao):
        x = valores(populacao)
        n = len(populacao)
        Q = zeros(R.shape)

        peso = []

        e, a = ql.random_action()

        for k in range(n):
            Q[ql.get_states()] = x[k, :]
            moviments = ql.move(self, e, Q=None)
            peso.append(len(moviments))
        peso = array(peso)
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
