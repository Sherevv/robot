import os
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from .body import BodyUndirected
from .body import BodyOriented
from .marker import Marker
from .helpers import decode_side
from .star_control import is_star_to_end, add_star_to_end
from ..exceptions import *
from .field import Field

matplotlib.rcParams['toolbar'] = 'toolmanager'


class RobotEngine:
    """
    Robot Class

    Each object of this class has a separate graphic window with
    checkered field and robot on it

    Properties:
    hFig, hAxes, field_size, hRobot, hMark, outMarkPos tMap, hVerBord, hHorBord,
    isServiceable, f

    Methods. :.. + event handlers that provide capabilities:
    - You can save the current situation on the field using the keyboard shortcut
    CTRL+S (the window with the robot must be current! )

    - Restore the last saved situation on the field using
    keyboard shortcuts CTRL+R ( the window with the robot must be current! )

    - View the temperature values of the cells using albinali keys
    CRTL+T ( the window with the robot must be current! )
    Pressing this key combination again removes the temperature values from the
    cells'.
    - Visualized temperature values can be edited (editing results
    stored only in RAM, to save the result of RUNE
    edit on the drive you want CTRL+S)

    - Dynamically change the delay time of the robot commands with the help of
    Ctrl+plus or CTRL+minus, respectively
    ( the window with the robot should be current! )

    -------------------------------------------------------------------------
    Date: 03.09.2015
    -----------------------------------------------------------------------
    %properties( Access = public )
    hFig, the handle of the graphics window
    hAxes descriptor of coordinate axes
    field_size number of rows and columns of field cells
    hRobot reference to an object of class Robot or RobOrt (!!! in particular, he has the ability to delay )

    hMark cell matrix containing [] or references to objects of class Marker
    ( the absence of a marker in the cell means or an empty value
    the corresponding array element or value of an already DELETED Robot class object.Marker )

    outMarkPos [] | double matrix, in the rows containing the position of the robot corresponding to cells with markers,
    to be installed outside of the visible part of the field (Aktualno unless the property outside == 'nomark')
    outside = 'none';
    print
    outside
    = 'none' (the field is limited by the frame) | 'ismark' (outside the frame entirely token) |
    'nomark' (there are no markers outside the original frame)

    tMap is a matrix of temperatures of the cells of the field

    hVerBord matrix cell that contains [] or links of vertical partitions ( objects of class Border )
    hHorBord matrix cell that contains [] or links of horizontal partitions ( objects of class Border )
    every cell in associiruetsya or partition from above (horizontal partition)
    peregorodka or bottom ( vertical partition ) or partition
    no ( no means peregorodki or empty value
    an array element or value of an already DELETED Robot class object.Bord )

    isServiceable = True = True / False-flag that determines the ability to control the robot
    (the robot can be " broken after an accident" )

    fName the name of the mat file in which the object will be stored (class Rob_???) under the name r
    when executing the corresponding method by pressing CTRL + S

    end % properties( Access = public )

    properties( Access = private )

    diameter = 40
    r = Robot.Options.diameter
    - cell size in pixels for figure objects, for example, = 40
    ( !!! at the same time, the size of the cage for axes objects for convenience
    it is taken to be 1, but it is not connected with the diameter value,
    which determines the actual size of the cell on the screen ),

    hTexts

    """

    def __init__(self, mapfile=None, robot_type=None, delay: int = None, **params):
        """
        Robot class constructor
        Creates (or creates, if in the dialogue there is a failure) box with a robot
        The robot type is determined by the value of the body parameter

        SYNTAX:
            obj = Robot( [] )
            obj = Robot( map file )

        GIVEN:
            - mapfile - [] | the name of the file ( mat-file, although the extension name is
            to be another ) in which the previously stored certain situation on the field

        RESULT:
            - possible (map file = [] ) user dialog

            - obj = reference (handle ) to the created object of the Robot class.Robot
            It is possible that the obj object is deleted (deleted obj), which means that the field was not created,
            for any reason
        """

        is_delay = False
        if isinstance(delay, (int, float)) and delay > 0:
            self.delay_def = delay
            is_delay = True
        else:
            self.delay_def = 0.5

        self.delay = self.delay_def

        self.isEffectOn = True

        self.isServiceable = True
        self.diameter = 40
        self.robotType = robot_type
        self.outMarkPos = np.empty((0, 2), int)
        self.outside = 'none'
        self.hRobot = None
        self.fPath = ''
        self.fName = ''

        if robot_type == 'Robot':
            body = BodyUndirected
        elif robot_type in ['RobotOrt', 'RobotRot']:
            body = BodyOriented
        else:
            raise RobotTypeValueError

        self.fhBody = body

        self.hField = Field(self, body=body, size=params.get('size', None))
        self.hRobot.delay = self.delay_def
        self.is_init_save = True

        if not mapfile:
            self.fName = 'untitled.map'
            if not self.hField.load(is_delay):  # User press "Cancel"
                if not self.hField.save():  # User press "Cancel"
                    add_star_to_end(self.hField.hFig)
                    self.is_init_save = False
        else:
            self.fPath = os.path.dirname(mapfile)
            self.fName = os.path.basename(mapfile)
            self.hField.restore(is_delay, **params)
            self.hField.hFig.canvas.set_window_title(self.robotType + ' - ' + mapfile)

        plt.show(block=False)

    def step(self, side=None):
        """
        Move the robot to the next cell in the given direction

        SYNTAX:
            r.step( side )

        GIVEN:
            - side = 'n' | 's' | ' o ' | ' w ' - given direction
            - r = reference to an object of class Rob_abs:
              robot in some cell of the field, from the side of the robot
              partition no
        """

        self.state_check()

        self._pause()

        if side and isinstance(side, str):
            side = side.lower()
        else:
            raise SideValueError

        if side == 'n':
            vect = [0, 1]  # при коррекции индексов, этот вектор нужно переворачивать
        elif side == 's':
            vect = [0, -1]

        elif side == 'o':
            vect = [1, 0]

        elif side == 'w':
            vect = [-1, 0]
        else:
            raise SideValueError

        if not self.is_bord_without_effects(side):
            self.hRobot.shift(vect, 'vector')
        else:
            self.hRobot.shift(np.array(vect) / 4, 'vector')
            self.isServiceable = False
            raise BrokenError

    def rot(self, side=None):
        """
        Rotates the robot in the specified direction with a delay

        SYNTAX:
            r.rot( side )
        GIVEN:
            - r = reference to an object of class Rob_abs:
              robot in some cell of the field, from the side of the robot
              partition no
            - side = 'Right' | 'Left' | ' Back '(register value not
            has)
        """

        self.state_check()

        if str.upper(side) not in ('RIGHT', 'R', 'LEFT', 'L', 'BACK', 'B'):
            raise SideValueError

        self._pause()
        self.hRobot.rot(side)

    def is_bord(self, side=None):
        """
        Command to check partitions in a given direction

        SYNTAX:
            res = r.is_board( side )

        GIVEN:
            - side = 'n' | 's' | ' o ' | ' w ' - given direction
            - r = reference to the Robot class object:
                        the robot is in some cell of the field
        """

        self.state_check()

        if not str.lower(side) in ['n', 's', 'o', 'w']:
            raise SideValueError

        if self.isEffectOn:
            if isinstance(self.hRobot, BodyOriented):
                self.hRobot.is_bord()
            elif isinstance(self.hRobot, BodyUndirected):
                self.hRobot.is_bord(side)
            else:
                raise RobotTypeError

        return self.is_bord_without_effects(side)

    def mark(self):
        """
        Command to put a marker in a cell with a robot

        SYNTAX:
            r.mark()

        GIVEN:
            - r = reference to the Robot class object:
                        the robot is in some cell of the field

        RESULT:
            - In a cage with a robot is a marker
            (re-marking does not change anything, you can not remove the already supplied marker )
        """

        self.state_check()

        pos = self.hRobot.position

        if self.is_out():
            # robot is outside the visible part of the field
            if not any(np.equal(self.outMarkPos, pos).all(1)):
                self.outMarkPos = np.append(self.outMarkPos, [pos], axis=0)
        else:
            # robot is in the visible part of the field
            if not self.hField.hMark[pos[0]][pos[1]]:
                self.hField.hMark[pos[0]][pos[1]] = Marker(pos[0], pos[1], self.hField.hAxes)

            if self.isEffectOn:
                self.hRobot.mark()

            self.hField.hFig.canvas.draw()

    def is_mark(self):
        """
        Verify the presence of the marker field of the cell

        SYNTAX:
                   res = r.is_mark()

        GIVEN:
            - r = reference to the Robot class object:
            a robot in a cage

        :return True - if cage is mark
        """

        self.state_check()

        pos = self.hRobot.position
        if self.is_out():  # robot is outside the visible part of the field
            return any(np.equal(self.outMarkPos, pos).all(1))
        else:  # robot is in the visible part of the field

            if self.isEffectOn:
                self.hRobot.is_mark()

            return True if self.hField.hMark[pos[0]][pos[1]] else False

    def get_tmpr(self):
        """
        Command to measure and report the "temperature" of the current cell

        SYNTAX:
            val = r.get_tmpr()

        GIVEN:
            - r = reference to the Robot class object:
                        a robot in a cage

        RESULT:
            - val = integer (double) = "temperature" of the robot cell

        ( when you create a new object of class Robot, "temperature"
        the field is generated randomly, but when you load a previously created one
        object from file-it's the same )
        """

        self.state_check()

        position = self.hRobot.position

        for i in range(len(position)):
            if position[i] < 0:
                position[i] = 0
            elif position[i] >= self.hField.size[i]:
                position[i] = self.hField.size[i] - 1

        if self.isEffectOn:
            self.hRobot.meas()

        return self.hField.tMap[position[0], position[1]]

    def get_side(self):
        """
        Command to communicate the current direction of the robot

        SYNTAX:
            side = r.get_side()

        WHERE:
            - r = reference to the Robot class object:
            robot in a cage
        """

        self.state_check()

        if self.isEffectOn:
            self.hRobot.get_side()

        return decode_side(self.hRobot.side)

    def get_side_(self):
        """
        Returns the current direction of the robot without visualizations

        SYNTAX:
            side = r.get_side_()

        GIVEN:
            - r = reference to an object of class Robot:
            robot in some cell

        RESULT:
            - side = ' n '(North) | ' o '(East) | ' s '(South) | ' w ' (West)
            - current direction of the robot
        """
        return decode_side(self.hRobot.side)

    def is_out(self):
        """
        Check robot is out of the field
        :return: True - if robot is out
        """
        pos = self.hRobot.position
        return pos[0] < 0 or pos[0] >= self.hField.size[0] or pos[1] < 0 or pos[1] >= self.hField.size[1]

    def is_bord_without_effects(self, side=None):
        """
        Checks for the presence of a border in the specified direction
        without special effects ( blinking of the legs, delays )

        :param side = ' n '(North) | ' o '(East) | ' s '(South) | ' w ' (West)
        """

        x, y = self.hRobot.position  # x - row index, y - col index

        side = side.upper()
        if side == 'N':
            # robot is out of the field
            if x < 0 or x >= self.hField.size[0]:
                return False

            if y < -1 or y > self.hField.size[1] - 1:
                return False
            elif y == -1 or y == self.hField.size[1] - 1:  # y = -1 - robot outside near frame
                return True if self.hField.hFrame else False  # Frame is a border

            return True if self.hField.hHorBord[x][y + 1] else False

        elif side == 'S':
            # robot is out of the field
            if x < 0 or x >= self.hField.size[0]:
                return False

            if y < 0 or y > self.hField.size[1]:
                return False
            elif y == 0 or y == self.hField.size[1]:
                return True if self.hField.hFrame else False

            return True if self.hField.hHorBord[x][y] else False

        elif side == 'O':
            # robot is out of the field
            if y < 0 or y >= self.hField.size[1]:
                return False

            if x < -1 or x > self.hField.size[0] - 1:
                return False
            elif x == -1 or x == self.hField.size[0] - 1:
                return True if self.hField.hFrame else False  # Frame is a border

            return True if self.hField.hVerBord[x + 1][y] else False

        elif side == 'W':
            # robot is out of the field
            if y < 0 or y >= self.hField.size[1]:
                return False

            if x < 0 or x > self.hField.size[0]:
                return False
            elif x == 0 or x == self.hField.size[0]:
                return True if self.hField.hFrame else False

            return True if self.hField.hVerBord[x][y] else False

    def _pause(self):
        """ Add delay"""
        if self.hRobot.delay != 0:
            time.sleep(self.hRobot.delay)

    def state_check(self):
        """
        Checks robot and field state, raise errors
        """
        if is_star_to_end(self.hField.hFig):
            raise NotSaveError

        if not self.isServiceable:
            raise ServiceError

    def delay_off(self):
        """ Disable delay """
        self.delay = 0
        self.hRobot.delay = 0
        self.isEffectOn = False

    def delay_on(self):
        """ Enable delay """
        self.delay = self.delay_def
        self.hRobot.delay = self.delay_def
        self.isEffectOn = True
