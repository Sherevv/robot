import numpy as np
from ..robot import Robot
from ..robot_engine.helpers import decode_side


class BugException(Exception):
    message = __doc__

    def __init__(self, message=None, *args):
        if message:
            self.message = message
        super(BugException, self).__init__(self.message, *args)


class NoWayToExitError(BugException):
    """There is no way to exit"""
    message = __doc__


class NoFrameError(BugException):
    """There is no frame border"""
    message = __doc__


class Bug:
    """
    Bug in a maze

    Idea from http://buglab.ru
    """

    def __init__(self, map_file=None, delay=0.0001):
        """
        Create field for bug (robot)
        :param map_file: map-file path string
        """
        self.r = Robot(map_file)
        self.r.hRobotEngine.hField.set_delay(delay)
        self.field_size = self.r.hRobotEngine.hField.size

        self.hVerBord = self.r.hRobotEngine.hField.hVerBord
        self.hHorBord = self.r.hRobotEngine.hField.hHorBord
        self.statusBar = self.r.hRobotEngine.hField.hFig.canvas.manager.statusbar

    def go(self):
        """
        The bug always starts its movement from the upper left corner,
        and the exit is always in the lower right corner.
        The bug is not moving optimally, and in the following manner:
        he goes to the place where there was not or was there frequently.
        I.e. passing each cell of the labyrinth, the bug remembers:
        how many times it was in this cell and when thinking about the direction
        of its movement at some particular moment, it looks:
        how many times it was in the cell below, how many on the right,
        how many on the left and how many on top and moving there, where he was less than once.
        If there are several such directions and one of them coincides with the current direction of movement,
        it does not change direction, otherwise it moves according to the following priorities:
        down, right, up, left. I. e. if the minimum number of visits immediately to the right and left
        (and it moved up or down), the bug goes to the right, because the "right" priority is higher.
        It should be noted that moving according to this algorithm,
        the bug will always reach the output in the case, when there is a way out.

        :return: n - count of steps
        """

        self._check_field()

        self.r.hRobotEngine.hRobot.shift((0, self.field_size[1] - 1), 'punct')

        kx, ky, kx2, ky2, down, right, up, left, cur = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        n = 0
        field = np.zeros(np.flipud(self.field_size))
        side = 2
        big = 1e+9
        while True:
            if kx == self.field_size[0] - 1 and ky == self.field_size[1] - 1:  # exit found
                return n
            else:
                kx2 = kx
                ky2 = ky
                n += 1

                if not self.r.is_bord('s'):
                    down = field[ky + 1][kx]
                else:
                    down = big

                if not self.r.is_bord('o'):
                    right = field[ky][kx + 1]
                else:
                    right = big

                if not self.r.is_bord('n'):
                    up = field[ky - 1][kx]
                else:
                    up = big

                if not self.r.is_bord('w'):
                    left = field[ky][kx - 1]
                else:
                    left = big

                if side == 2:
                    cur = down
                if side == 1:
                    cur = right
                if side == 0:
                    cur = up
                if side == 3:
                    cur = left
                if cur <= down and cur <= right and cur <= up and cur <= left:
                    if side == 2:
                        ky2 += 1
                    if side == 1:
                        kx2 += 1
                    if side == 0:
                        ky2 -= 1
                    if side == 3:
                        kx2 -= 1
                elif down <= right and down <= up and down <= left:
                    ky2 += 1
                    side = 2
                elif right <= down and right <= up and right <= left:
                    kx2 += 1
                    side = 1
                elif up <= right and up <= down and up <= left:
                    ky2 -= 1
                    side = 0
                elif left <= right and left <= down and left <= up:
                    kx2 -= 1
                    side = 3

                field[ky][kx] += 1
                kx = kx2
                ky = ky2

            self.r.step(decode_side(side))
            self.statusBar.set_message('Steps count: ' + str(n))
            print(n)

    def _check_field(self):
        """
        Check if field is correct
        :return boolean
        """

        if not self.r.hRobotEngine.hField.hFrame:
            raise NoFrameError

        if not self._is_exit_exists():
            raise NoWayToExitError

    def _is_exit_exists(self):
        """
        Check if way to exit is exist in a maze
        :return boolean
        """

        field = np.zeros(self.field_size)
        field[0][self.field_size[1] - 1] = 1
        while True:
            ok = False
            for i in range(self.field_size[0]):
                for j in range(self.field_size[1] - 1, -1, -1):
                    if (not field[i][j]) and (
                            (i > 0 and field[i - 1][j] == 1 and not self.hVerBord[i][j])
                            or (i + 1 < self.field_size[0] and field[i + 1][j] == 1 and not self.hVerBord[i + 1][j])
                            or (j > 0 and field[i][j - 1] == 1 and not self.hHorBord[i][j])
                            or (j + 1 < self.field_size[1] and field[i][j + 1] == 1 and not self.hHorBord[i][j + 1])):

                        ok = True
                        field[i][j] = 1
                        if (i == self.field_size[0] - 1) and (j == 0):
                            return True
            if not ok:
                break

        return False
