from numpy import array, uint8, where, max, random, count_nonzero, sqrt, abs
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



class LabMove:

    def __init__(self, R, premio=10, penalidade=10):
        self.R = R
        self._penalidade = penalidade
        self._premio = premio
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

    def plot(self, start, sequence):
        fig = plt.figure()
        img2 = self.R.copy()
        img2[self._endx, self._endy] = 200
        im = plt.imshow(img2, animated=True)

        self.x, self.y = start
        self._stop = False

        def updatefig(frame):
            img2 = self.R.copy()
            img2[img2 == 0] = 255
            img2[img2 == -1] = 0
            img2[self._endx, self._endy] = 50
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


            if self._stop == False:
                img2[self.x, self.y] = 100

            im.set_array(img2)
            return im,

        ani = FuncAnimation(fig,
                            updatefig,
                            frames=len(sequence),
                            interval=150,
                            blit=True)
        plt.show()

    def move(self, start, sequence):
        '''
        1 - up
        2 - down
        3 - left
        4 - right
        '''

        path = [tuple(start)]
        self.x, self.y = start
        penalidades = 0
        touched = False
        for step in sequence:
            if step == 1:
                self.move_up()
            elif step == 2:
                self.move_down()
            elif step == 3:
                self.move_left()
            elif step == 4:
                self.move_right()

            if (self.x, self.y) not in path:
                path.append((self.x, self.y))
            else:
                if self.x != self._endx and self.y != self._endy :
                    penalidades += self._penalidade

            d = sqrt((self._endx - self.x) ** 2.0 + (self._endy  - self.y) ** 2.0)

            if d == 0 and touched is False:
                penalidades -= self._premio
                touched = True

        d = abs(self._endx - self.x) + abs(self._endy  - self.y)
        penalidades += d

        return penalidades

    x = property(get_x, set_x)
    y = property(get_y, set_y)
