import time
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from source.robot.robot.robot_engine.helpers import encode_side


def rot_data(x_data=None, y_data=None, phi=None, point=None):
    """
    Perform transformation of arrays of coordinates of graphical object points
    when turning at a given angle around a given point

    SYNTAX:
        [x_data, y_data] = rot_data( x_data, y_data, phi, point )

    AT BASELINE:
        - x_data, y_data-double vectors that determine the coordinates of the points of the graphic object
        - phi-rotation angle
        - point = 2-vector double-contains the coordinates of the point-center of rotation

    RESULT:
        - x_data, y_data - double of the vector defining the coordinates of the points
          the graphical object after the rotation
    """

    complex_point = complex(point[0], point[1])
    complex_data = (x_data + 1j * y_data) - complex_point
    complex_data = np.array(complex_data) * np.exp(1j * phi) + complex_point
    x_data = np.real(complex_data)
    y_data = np.imag(complex_data)

    return x_data, y_data


class BodyBase:
    """
    Body-base class for visual modeling of non-oriented behavior
    robot's

    Public method:
        shift, mark, is_mark, is_bord, meas
    Protected-methods:
        sond_data_init ( virtual method )

    Properties:
        position, delay, moved
    """

    def __init__(self, coordinates, hFig):
        """
        Designer of the oriented robot and its graphical image

        SYNTAX:
            r = Body( coordinates )
            - coordinates = [x, y] - Cartesian coordinates of the lower left corner of the cell
            - - hid = handle of the graphics window work

        :param coordinates: initial robot position on the field
        :param hFig: reference to plot Figure
        """

        self.delay = 0
        # self.moved = 'off'  # flag that determines the ability to move the robot with the mouse

        self.hL = [0, 0, 0, 0]  # = 4-vector of the descriptors of the feet of the robot:

        # TODO: check this
        # 1st foot - FRONT or NORTH
        # 2st foot - RIGHT or EAST
        # 3rd foot - REAR or SOUTH
        # 4th foot - LEFT or EAST

        self.xData_0_L = np.zeros(4)
        self.yData_0_L = np.zeros(4)

        self.R = 0.35  # the radius of the robot corpus
        # the base size of the tabs ( e.g. the side of a square if the square foot )
        self.L = 0.15

        self.hFig = hFig

        # indices of the field cell containing the robot ( the lower left cell is indexed: [0,0] )
        self.position = np.array(coordinates)

        x = coordinates[0]
        y = coordinates[1]

        self.x_0 = x + 0.5
        self.y_0 = y + 0.5
        # x_0, y_0 - the coordinates of the robot center

        self.hCorp = mpatches.Circle((self.x_0, self.y_0), self.R,
                                     facecolor='y',
                                     edgecolor='k',
                                     linewidth=1,
                                     clip_on=False,
                                     zorder=15)

        self.hAxes = plt.gca()
        self.hAxes.add_patch(self.hCorp)

        self.sond_data_init()

        for i in range(4):
            self.hL[i] = mpatches.Rectangle(
                (self.xData_0_L[i] + self.x_0,
                 self.yData_0_L[i] + self.y_0),
                width=self.L,
                height=self.L,
                facecolor='k',
                edgecolor='k',
                zorder=16)
            self.hAxes.add_patch(self.hL[i])

        self.dr = Draggable(self.hCorp, self.hL, self.hFig, self)

    def delete(self):
        """ Delete robot """
        self.hAxes.patches.remove(self.hCorp)
        for i in range(4):
            self.hAxes.patches.remove(self.hL[i])

    def shift(self, coord=None, mode=None):
        """
        without delay shifts the image of the robot on the vector of coord or coord point
        - depending on the mode parameter value

        - coord = 2-vector double = coordinates of the displacement vector | coordinates of the center of the body
        - mode = ' vector '(for software movement) / 'punct' (for manual movement)
        Records the fact of changing the situation (adds * to the end of the name
        window title)

        :param coord:
        :param mode:
        """

        if mode == 'vector':

            dx = coord[0]
            dy = coord[1]

            self.hCorp.center = (
                self.hCorp.center[0] + dx,
                self.hCorp.center[1] + dy)

            for i in range(0, 4):
                self.hL[i].xy = (
                    self.hL[i].xy[0] + dx,
                    self.hL[i].xy[1] + dy)

            self.position = self.position + np.array(coord)

        elif mode == 'punct':

            x = coord[0]
            y = coord[1]

            self.hCorp.center = (
                self.x_0 + x,
                self.y_0 + y)

            for i in range(0, 4):
                self.hL[i].xy = (
                    self.x_0 + self.xData_0_L[i] + x,
                    self.y_0 + self.yData_0_L[i] + y)

            self.position = np.int8(np.array(coord) + 0.5)
        else:
            raise ValueError()

        self.hFig.canvas.draw()

    def meas(self):
        """
        Visualizes the fact of measurement with the set time delay
        """
        self.update_edgecolor('b')

    def mark(self):
        """
        Visualizes the marking fact with the set time delay
        If there was a situation editing, then opens a dialog
        to save the result of editing and removes * at the end
        window name
        """
        # Robot.Control.SaveDialog( self.hFig )
        self.update_edgecolor('m')

    def is_mark(self):
        """
        Visualizes the fact of the check with the set time delay
        """

        self.update_facecolor('m')

    def is_bord(self, side=None):
        """
        Visualizes the fact of the check with the set time delay
        :param side:
        """

        self.update_facecolor_p(self.hL[encode_side(side)], 'g')

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

    def update_facecolor(self, uclr):
        self.update_facecolor_p(self.hCorp, uclr)

    def update_edgecolor(self, uclr):
        clr = self.hCorp.get_edgecolor()
        self.hCorp.set_edgecolor(uclr)
        self.hFig.canvas.draw()
        time.sleep(self.delay)
        self.hCorp.set_edgecolor(clr)
        self.hFig.canvas.draw()

    def update_facecolor_p(self, patch, uclr):
        clr = patch.get_facecolor()
        patch.set_facecolor(uclr)
        self.hFig.canvas.draw()
        time.sleep(self.delay)
        patch.set_facecolor(clr)
        self.hFig.canvas.draw()

    def update_color(self, param, uclr):
        clr = self.hCorp.get(param)
        self.hCorp.set(param, uclr)
        self.hFig.canvas.draw()
        time.sleep(self.delay)
        self.hCorp.set(param, clr)
        self.hFig.canvas.draw()


class Draggable:
    def __init__(self, corp, hands, figure, rob=None):
        self.hands_init = 0
        self.rect_init = 0
        if rob:
            self.rect_init = {'x': rob.x_0, 'y': rob.y_0}
            self.hands_init = {'x': rob.xData_0_L, 'y': rob.yData_0_L}
        self.rect = corp
        self.hands = hands
        self.press = None
        self.f = figure
        self.r = plt.gca().robotdata['r']
        self.rob = rob
        self.connect()

    def connect(self):
        """connect to all the events we need"""
        self.cidpress = self.f.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.f.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.f.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        """on button press we will see if the mouse is over us and store some data"""
        if event.inaxes != self.rect.axes: return

        contains, attrd = self.rect.contains(event)
        if not contains: return

        self.r.hField.window_button_motion()
        self.rect.set_facecolor('b')
        x0, y0 = self.rect.center
        hands_coord = []
        for hand in self.hands:
            hands_coord.append(hand.xy)
        self.press = x0, y0, event.xdata, event.ydata, hands_coord

    def on_motion(self, event):
        """on motion we will move the rect if the mouse is over us"""
        if self.press is None:
            return
        if event.inaxes != self.rect.axes:
            return
        x0, y0, xpress, ypress, hands_coord = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.rect.center = (x0 + dx, y0 + dy)
        for indx, hand in enumerate(self.hands):
            hand.xy = (hands_coord[indx][0] + dx, hands_coord[indx][1] + dy)

        self.rect.figure.canvas.draw()

    def on_release(self, event):
        """on release we reset the press data"""
        if self.press is None:
            return
        if event.inaxes != self.rect.axes:
            return
        x0, y0, xpress, ypress, hands_coord = self.press

        dx = np.floor(event.xdata - xpress + self.rect_init['x'])
        dy = np.floor(event.ydata - ypress + self.rect_init['y'])

        x0 = np.floor(x0) + self.rect_init['x']
        y0 = np.floor(y0) + self.rect_init['y']

        newx = x0 + dx
        newy = y0 + dy
        if newx < self.rect_init['x']:
            newx = self.rect_init['x']
        if newy < self.rect_init['y']:
            newy = self.rect_init['y']

        r = plt.gca().robotdata['r']
        if newx > r.hField.size[0]:
            newx = r.hField.size[0] - self.rect_init['x']
        if newy > r.hField.size[1]:
            newy = r.hField.size[1] - self.rect_init['y']

        self.rect.center = (newx, newy)
        for indx, hand in enumerate(self.hands):
            hand.xy = (self.hands_init['x'][indx] + newx, self.hands_init['y'][indx] + newy)

        self.rob.position = np.array([int(newx - self.rect_init['x']), int(newy - self.rect_init['y'])])
        self.rob.side = 0
        self.rect.set_facecolor('y')
        self.press = None
        self.rect.figure.canvas.draw()

    def disconnect(self):
        """disconnect all the stored connection ids"""
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)


class BodyOriented(BodyBase):
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

    def is_bord(self, side=None):
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


class BodyUndirected(BodyBase):
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