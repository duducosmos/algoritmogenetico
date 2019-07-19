from numpy import array, zeros, where, max, random



class LabMove:
    def __init__(self, R, verbose=False):
        self.R = R
        self.verbose = verbose
        self.nocon = -100

    def goal(self):
        return max(self.R)

    def move(self, start, sequence, verbose=False):
        '''
        0 - no-move
        1 - up
        2 - down
        3 - left
        4 - right

        '''
        if len(start) != 2:
            return None

        if self.verbose is True or verbose is True:
            print("Started at {}".format(start))

        endi, endj = where(self.R == max(self.R))
        endi, endj = endi[0], endj[0]

        if start[0] == endi and start[1] == endj:
            return 0
        lines, cols = self.R.shape

        current = start
        steps = self.nocon

        for step in sequence:
            i, j = current
            if step == 1:
                i = i - 1
                if i < 0:
                    steps += self.nocon
                    break
            elif step == 2:
                i = i + 1
                if i >= lines:
                    steps += self.nocon
                    break
            elif step == 3:
                j = j - 1
                if j < 0:
                    steps += self.nocon
                    break
            elif step == 4:
                j = j + 1
                if j >= cols:
                    steps += self.nocon
                    break

            current = [i, j]

            if self.R[i, j] == -1:
                steps += self.nocon
                break

            if self.R[i, j] == self.goal():
                steps += 1000
                break
            if self.R[i, j] == 0:
                steps += 1
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
    from pathos.pools import ProcessPool as Pool

    from makemaze import make_maze

    from numpy import concatenate, hsplit, uint8, ones
    import matplotlib.pyplot as plt

    from pygenic.populacao import Populacao
    from pygenic.selecao.torneio import Torneio
    from pygenic.selecao.roleta import Roleta
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
    s0, s1 = where(R != max(R)))
    startpoint = random.choice(zip(s0.tolist(), s1.tolist()))
    print(startpoint)

    img2 = img.copy()
    img2[goal] = 150

    lm = LabMove(R, verbose=False)

    tamanho_populacao = 30
    cromossomos = 30

    plt.imshow(img2)
    plt.show()
    print("Number of possibles states: {}".format(e.size))

    tamanho = int(0.1 * tamanho_populacao)
    tamanho = tamanho if tamanho_populacao > 20 else 5
    bits = 3
    genes = bits * cromossomos
    pmut = 0.2
    pcruz = 0.6
    epidemia = 100
    elitista = True

    def valores(populacao):
        bx = hsplit(populacao, cromossomos)
        #x = [binarray2int(xi) for xi in bx]
        const = 2 ** bits - 1
        const = 4 / const
        x = [const * binarray2int(xi) for xi in bx]
        x = concatenate(x).T.astype(int)
        return x

    def avaliacao(populacao):
        x = valores(populacao)
        n = len(populacao)
        def steps(k):
            sequence = x[k, :]
            return lm.move(startpoint, sequence=sequence)

        pool = Pool(nodes=12)
        peso = -array(list(pool.imap(steps, range(n)))).astype(int)
        return peso

    populacao = Populacao(avaliacao,
                               genes,
                               tamanho_populacao)

    selecao = Torneio(populacao, tamanho=tamanho)
    #selecao = Roleta(populacao)
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
