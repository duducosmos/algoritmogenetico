from numpy import array, uint8, where, max, random, count_nonzero
from numpy import sqrt, abs, log, exp, floor
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers


class LabMove:

    def __init__(self, R, premio=100, penalidade=10, moeda=1, introns=100):
        self.R = R
        self._penalidade = penalidade
        self._premio = premio
        self._moeda = moeda
        self._introns = introns
        self.size_lab = count_nonzero(R != -1)
        self._x = None
        self._y = None
        self._endx, self._endy = self.ends()
        self._lines, self._cols = self.R.shape


    def set_x(self, x):
        if x < 0:
            x = 0
        if x >= self._cols:
            x = self._cols - 1
        self._x = x

    def set_y(self, y):
        if y < 0:
            y = 0
        if y >= self._lines:
            y = self._lines - 1
        self._y = y

    def get_y(self):
        return self._y

    def get_x(self):
        return self._x

    def _limits(self):
        if self._y < 0:
            self._y += 1
        if self._y >= self._lines:
            self._y -= 1

    def move_up(self):
        self._limits()
        self._y -= 1
        if self.R[self._x, self._y] == -1:
            self._y += 1

    def move_down(self):
        self._limits()
        self._y += 1
        if self.R[self._x, self._y] == -1:
            self._y -= 1

    def move_left(self):
        self._limits()
        self._x -= 1
        if self.R[self._x, self._y] == -1:
            self._x += 1

    def move_right(self):
        self._limits()
        self._x += 1
        if self.R[self._x, self._y] == -1:
            self._x -= 1

    def goal(self):
        return max(self.R)

    def ends(self):
        endi, endj = where(self.R == max(self.R))
        return endi[0], endj[0]

    def plot(self, start, sequence, interval=10, save_file=None):
        fig = plt.figure()
        img2 = self.R.copy()
        img2[self._endx, self._endy] = 200
        im = plt.imshow(img2, animated=True)

        self.x, self.y = start
        self._stop = False

        self._curr0 = 0
        self._curr1 = 1


        def updatefig(frame):
            img2 = self.R.copy()
            img2[img2 == 0] = 255
            img2[img2 == -1] = 0
            img2[self._endx, self._endy] = 150
            nseq = len(sequence)
            if self._curr0 >= nseq or self._curr1 >= nseq:
                self._curr0 -= 2
                self._curr1 -= 2

            steps = sequence[self._curr0] * [sequence[self._curr1]]

            if sequence[self._curr1] in [1, 2, 3, 4]:
                for step in steps:
                    if step == 1:
                        self.move_up()
                    elif step == 2:
                        self.move_down()
                    elif step == 3:
                        self.move_left()
                    elif step == 4:
                        self.move_right()

                    if self.x == self._endx and self.y == self._endy and self._stop == False:
                        self._stop = True
                        img2[self._endx, self._endy] = 100
                        print("Alcançado")


                    if self._stop == False:
                        img2[self.x, self.y] = 50

            im.set_array(img2)

            self._curr0 += 2
            self._curr1 += 2

            return im,

        ani = FuncAnimation(fig,
                            updatefig,
                            frames=len(sequence) // 2,
                            interval=50,
                            blit=True)

        if save_file is not None:
            Writer = writers['ffmpeg']
            writer = Writer(fps=10, metadata=dict(artist='Me'), bitrate=1800)
            ani.save(save_file, writer=writer)
        else:
            plt.show()

    def move(self, start, sequence):
        '''
        1 - up
        2 - down
        3 - left
        4 - right
        '''
        visitado = {tuple(start): 1}
        self.x, self.y = start
        pontos = 0
        x0, y0 = self.x, self.y
        vi = []
        vj = []

        for i in range(0, len(sequence) -1, 2):
            steps = sequence[i] * [sequence[i + 1]]
            if sequence[i + 1] not in [1, 2, 3, 4]:
                pontos -= self._introns
            else:
                for step in steps:

                    if step == 1:
                        self.move_up()
                    elif step == 2:
                        self.move_down()
                    elif step == 3:
                        self.move_left()
                    elif step == 4:
                        self.move_right()

                    imod = abs(self.x - x0)
                    ihat = (self.x - x0) / imod if imod != 0 else 0

                    jmod = abs(self.y - y0)
                    jhat = (self.y - y0) / jmod if jmod != 0 else 0

                    x0, y0 = self.x, self.y
                    vi.append(imod * ihat)
                    vj.append(jmod * jhat)

                    if (self.x, self.y) not in visitado:
                        d = abs(self.x - self._endx) + abs(self.y - self._endy)
                        pontos += self._moeda // (1 + d)
                        visitado[(self.x, self.y)] = 0
                    else:
                        if self.x != self._endx and self.y != self._endy:
                            visitado[(self.x, self.y)] += 1
                            pontos -= self._penalidade * visitado[(self.x, self.y)]

                    if self.x == self._endx and self.y == self._endy:
                        pontos += self._premio

                #xf = sum(vi)
                #yf = sum(vj)
                #d = int(abs(xf) + abs(yf))
                #d2 = abs(self.x - self._endx) + abs(self.y - self._endy)
                #pontos += d

        return pontos

    x = property(get_x, set_x)
    y = property(get_y, set_y)
