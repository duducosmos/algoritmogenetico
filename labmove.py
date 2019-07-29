from numpy import array, uint8, where, max, random, count_nonzero
from numpy import sqrt, abs, log, exp, floor
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers


class LabMove:

    def __init__(self, R, premio=100, penalidade=10, moeda=1):
        self.R = R
        self._penalidade = penalidade
        self._premio = premio
        self._moeda = moeda
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
        im = plt.imshow(img2, animated=True, interpolation='none', aspect='auto')

        self.x, self.y = start
        self._stop = False


        def updatefig(frame):
            img2 = self.R.copy()
            img2[img2 == 0] = 255
            img2[img2 == -1] = 0
            img2[self._endx, self._endy] = 150
            step = sequence[frame]

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
            return im,

        ani = FuncAnimation(fig,
                            updatefig,
                            frames=len(sequence) - 1,
                            interval=50,
                            blit=True)

        if save_file is not None:
            Writer = writers['ffmpeg']
            writer = Writer(fps=29, metadata=dict(artist='Me'), bitrate=1800)
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
        self.x, self.y = start
        pontos = 0
        chegou = False
        position = [[self.x, self.y]]
        repeticao = {(self.x, self.y): 1}
        ns = 0

        for step in sequence:
            if step == 1:
                self.move_up()
            elif step == 2:
                self.move_down()
            elif step == 3:
                self.move_left()
            elif step == 4:
                self.move_right()

            if (self.x, self.y) not in repeticao:
                repeticao[(self.x, self.y)] = 0
            else:
                repeticao[(self.x, self.y)] += 1


            position.append([self.x, self.y])
            ns += 1
            if ns >= self.size_lab * 10:
                break

            if self.x == self._endx and self.y == self._endy:
                pontos += self._premio
                chegou = True
                print("ch")
                break

        np = len(position)
        dx = sum([position[i + 1][0] - position[i][0] for i in range(0, np - 1)])
        dy = sum([position[i + 1][1] - position[i][1] for i in range(0, np - 1)])
        ds = sqrt(dx ** 2.0 + dy ** 2.0)
        steps = sum([repeticao[keys] for keys in repeticao])

        df = 1 + sqrt((self.x - self._endx) ** 2.0 + (self.y + self._endy) ** 2.0)
        pontos += 1 / df - steps + ds
    
        if chegou is True:
            pontos = (pontos + 10 / steps) ** 2.0


        return pontos

    x = property(get_x, set_x)
    y = property(get_y, set_y)
