import numpy as np
from .rot_data import rot_data
from .body import Body


class Body4(Body):
    """
    Body 4-class for visual modeling of undirected behavior
    robot's

    Protected-methods:
            sound_data_init ( overload of a virtual method )

    Public-properties:
      position, delay, moved ( inherited from Robot.Body )
    """

    def __init__(self, coordinates, fig):
        """
        Designer of the oriented robot and its graphical image

        SYNTAX:
            r = Body 4( coordinates, hFig )
        - coordinates = [x, y] - Cartesian coordinates of the lower left corner of the cell
        - - hid = robot graphic window handle

        :param coordinates:
        :param fig:
        """

        super().__init__(coordinates, fig)

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
