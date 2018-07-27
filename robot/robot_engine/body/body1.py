import time
import numpy as np
from .body import Body
from .rot_data import rot_data


class Body1(Body):
    """
    Body 1-class for visual modeling of oriented behavior robot

    Methods:
        shift, riot, mark, is_mark, is_bond, meas
    """

    def __init__(self, coordinates=None, fig=None, side=None):
        """
        Designer of the oriented robot and its graphical image

        SYNTAX:
                            r = Body 1( coordinates, hFig, side )
        - coordinates = [x, y] - Cartesian coordinates of the lower left corner of the cell
        - fig = descriptor of the robot's graphical window
        - side = 0 | 1 | 2 | 3

                            r = Body 1( R, hFig )
        - - R = Robot class object.Body 1 / Robot class object.Body 4
        """

        super().__init__(coordinates, fig)

        self.side = 0  # = 0 | 1 | 2 | 3

        if side == 1:
            self.rot('RIGHT')
        elif side == 2:
            self.rot('BACK')
        elif side == 3:
            self.rot('LEFT')

        self.hL[0].set_facecolor('g')

    def shift(self, coord=None, mode=None):
        """
        Without delay shift the image of the robot with preservation of orientation vector
        coord or to the coord point with North orientation
        - depending on the mode parameter value

        - coord = 2-vector double = coordinates of the displacement vector | coordinates of the center of the body
        - mode = ' vector '(for software movement) / 'punct' (for manual movement)
        Records the fact of changing the situation (adds * to the end of the name
        window title)
        """

        super().shift(coord, mode)

        if mode == 'punct':
            self.side = 0

    def rot(self, side=None):
        """
        Rotates 90 or 180 degrees left or right-in
        matter what side around the center of the robot
        - side = 'Left' | 'Right' / 'Back' (register value does not matter )
        If there was a situation editing, then opens a dialog
        to save the result of editing and removes * at the end
        window name
        """

        # Robot.Control.SaveDialog( self.hFig )

        side = str.upper(side)
        if side in ('LEFT', 'L'):
            phi = np.pi / 2
            self.side = np.mod(self.side - 1, 4)
        elif side in ('RIGHT', 'R'):
            phi = -np.pi / 2
            self.side = np.mod(self.side + 1, 4)
        elif side in ('BACK', 'B'):
            phi = np.pi
            self.side = np.mod(self.side + 2, 4)

        else:
            raise ValueError()

        point = self.position + 0.5  # the coordinates of the center of the robot

        for i in range(4):
            xData, yData = self.hL[i].xy
            xData, yData = rot_data(xData + self.L / 2, yData + self.L / 2, phi, point)
            self.hL[i].xy = (xData - self.L / 2, yData - self.L / 2)

    def is_bord(self):
        """
        Visualizes the fact of the check
        with a set time delay
        """
        self.update_facecolor_hl('g', [1])

    def get_side(self):
        """
        Visualizes the return of a direction
        with a set time delay
        """
        self.update_facecolor_hl('r', [1, 3])

    def update_facecolor_hl(self, uclr, hli):
        clr = self.hL[1].get_facecolor()
        for idx in hli:
            self.hL[idx].set_facecolor(uclr)
        self.hFig.canvas.draw()
        time.sleep(self.delay)
        for idx in hli:
            self.hL[idx].set_facecolor(clr)
        self.hFig.canvas.draw()

    def sond_data_init(self):
        """
        Create data sets for robot legs, the center of which
        is at the origin (at (0,0) )
        """

        self.xData_0_L[0] = 0
        self.yData_0_L[0] = self.R

        for i in range(1, 5):
            if i != 4:
                self.xData_0_L[i], self.yData_0_L[i] = rot_data(
                    self.xData_0_L[i - 1], self.yData_0_L[i - 1], -np.pi / 2, [0, 0])
            self.xData_0_L[i - 1] -= self.L / 2
            self.yData_0_L[i - 1] -= self.L / 2

    def rot_(self, side=None, fig=None):
        """
        Rotate 90 or 180 degrees left or right-in depending on the side value around the robot center
            - side = 'Left' | 'Right' / 'Back' (register value does not matter )
            RECORDS the fact of changing the situation (adds * to the end of the name
            window title)
            - fig - descriptor of the robot's graphic window
        """

        self.rot(side)

        # situation changed
        # Robot.Control.AddStarToEnd(fig)
