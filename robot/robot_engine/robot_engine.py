import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from .body.body4 import Body4
from .body.body1 import Body1
from .marker import Marker
from .decode_side import decode_side
from .star_control import is_star_to_end
from .exeptions import *
from .field import Field
matplotlib.rcParams['toolbar'] = 'toolmanager'


class RobotEngine:
    """
    Robot Class

    Each object of this class has a separate graphic window with
    checkered field and robot on it

    Properties:
    hFig, hAxes, field_size, hRobot, hMark, outMarkPos tMap, hVerBord, hhorborford,
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

    def __init__(self, mapfile=None, robot_type=None):
        """ Robot-class constructor
        Creates (or creates, if in the dialogue there is a failure) box with a robot
        The robot type is determined by the value of the body parameter

        SYNTAX:
        obj = Robot( body, [] )
        obj = Robot( body, map file )

        GIVEN:
        - - body = @Robot.Boy 4 (corresponds to Rob_abs) | @Robot.Body 1 (corresponds to Rob_rel)

        - mapfile - [] | the name of the file ( mat-file, although the extension name is
        to be another ) in which the previously stored certain situation on the field

        RESULT:
        - - possible (map file = [] ) user dialog

        - obj = reference (handle ) to the created object of the Robot class.Robot
        It is possible that the obj object is deleted (deleted obj), which means that the field was not created,
        for any reason

        - self.outside = 'none' | 'ismark' | 'nomark'
        """

        self.delay_def = 0.5
        self.delay = self.delay_def  # Значение delay может быть изменено с помощью соответствующего инструмента
        self.isEffectOn = True

        self.isServiceable = True
        self.diameter = 40
        self.robotType = robot_type
        self.outMarkPos = []
        self.outside = 'none'
        self.hRobot = None

        if robot_type == 'Robot':
            body = Body4
        elif robot_type in ['Robot_ort', 'Robot_rot']:
            body = None  # Body1
        else:
            raise RobotTypeValueError

        self.fhBody = body

        self.hField = Field(self)
        self.hRobot.delay = self.delay_def

        if not mapfile:
            self.fName = 'untitled.map'
        else:  # входной параметр mapfile - не пустой
            self.fName = mapfile
            self.hField.restore()
            # __, ext = os.path.splitext(mapfile)
            # self.fName = [name, ext]
            # требуется выбрать файл
            # filepath = get_file()
            # print(a)

            # if filepath and os.path.isfile(filepath):  # - файл выбран
            #     if os.path.splitext(filepath)[1] != '.map':
            #         return
        # self.Field.create(self)  # self.field_create( self.hField.size )
        # self.hField = Field(self)
        plt.show(block=False)

    def step(self, side=None):
        """step - команда переместить робота в соседнюю клетку в заданном направлении

        СИНТАКСИС:
                 coderror =  r.step( side )

        ДАНО:
        - side = 'n' | 's' | 'o' | 'w' - заданное направление
        - r = ссылка на объект класса Rob_abs:
          робот в некоторой клетке поля, со стороны side от робота
          перегородки нет
          """

        self.state_check()

        self._pause()

        if side in ('n', 'N'):
            vect = [0, 1]  # при коррекции индексов, этот вектор нужно переворачивать
        elif side in ('s', 'S'):
            vect = [0, -1]

        elif side in ('o', 'O'):
            vect = [1, 0]

        elif side in ('w', 'W'):
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
                  coderror = rot( obj, side )
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
                                  ansv = r.is_board( side )

        GIVEN:
        - side = 'n' | 's' | ' o ' | ' w ' - given direction
        - r = reference to the Robot class object:
                    the robot is in some cell of the field
        """

        self.state_check()

        if not str.lower(side) in ['n', 's', 'o', 'w']:
            raise SideValueError

        if self.isEffectOn:
            if isinstance(self.hRobot, Body1):
                self.hRobot.is_bord()
            elif isinstance(self.hRobot, Body4):
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
            # TODO добавление только новых меток
            # if pos not in self.outMarkPos.any():
            self.outMarkPos.append(pos)
            print("out")

            self._pause()

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
                   [ansv, coderror] = R.is_mark()

        GIVEN:
        - r = reference to the Robot class object:
        a robot in a cage
        """

        self.state_check()

        pos = self.hRobot.position
        if self.is_out():  # robot is outside the visible part of the field

            if self.outside == 'nomark':
                ansv = False
                for i in range(len(self.outMarkPos)):
                    # TODO: check this
                    if pos == self.outMarkPos[i, :]:  # isequal( pos, self.outMarkPos(i,:) ) == 1
                        ansv = True
                        break

            # elif self.outside == 'ismark':
            # ansv = True

            self._pause()
        else:  # robot is in the visible part of the field
            if self.hField.hMark[pos[0]][pos[1]]:
                ansv = True
            else:
                ansv = False

            if self.isEffectOn:
                self.hRobot.is_mark()

        return ansv

    def get_tmpr(self):
        """
        Command to measure and report the "temperature" of the current cell

        SYNTAX:
                   [val, coderror] = R.get_tmpr()

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
        Returns the current direction of the robot without
        # visualizations
        #
        # SYNTAX:
        # side = r.get_side_()
        #
        # GIVEN:
        # - r = reference to an object of class Robot:
        # # robot in some cell
        #
        # RESULT:
        # - side = ' n '(North) | ' o '(East) | ' s '(South) | ' w ' (West)
        # - current direction of the robot
        """
        side = decode_side(self.hRobot.side)

        return side

    def is_out(self):
        """
        Check robot is out of the field
        :return: True - robot is out
        """
        pos = self.hRobot.position
        return pos[0] < 0 or pos[0] >= self.hField.size[0] or pos[1] < 0 or pos[1] >= self.hField.size[1]

    def is_bord_without_effects(self, side=None):
        """
        Checks for the presence of a border in the specified direction
        without special effects ( blinking of the legs, delays )
        """

        x, y = self.hRobot.position  # x - row index, y - col index

        side = side.upper()
        if side == 'N':

            if y >= self.hField.size[1] - 1:
                return True if self.hField.hFrame else False  # Frame is a border
            elif y < 0:
                return False

            # robot is out of the field
            if x >= self.hField.size[0]:
                x = self.hField.size[0] - 1
            elif x < 0:
                x = 0

            return True if self.hField.hHorBord[x][y + 1] else False

        elif side == 'S':
            if y <= 0:
                return True if self.hField.hFrame else False
            elif y >= self.hField.size[1] - 1:
                return False

            # robot is out of the field
            if x >= self.hField.size[0]:
                x = self.hField.size[0] - 1
            elif x < 0:
                x = 0

            return True if self.hField.hHorBord[x][y] else False

        elif side == 'O':
            if x >= self.hField.size[0] - 1:
                return True if self.hField.hFrame else False
            elif x < 0:
                return False

            # robot is out of the field
            if y >= self.hField.size[1]:
                y = self.hField.size[1] - 1
            elif y < 0:
                y = 0

            return True if self.hField.hVerBord[x + 1][y] else False

        elif side == 'W':

            if x <= 0:
                return True if self.hField.hFrame else False
            elif x >= self.hField.size[0] - 1:
                return False

            # robot is out of the field
            if y >= self.hField.size[1]:
                y = self.hField.size[1] - 1
            elif y < 0:
                y = 0

            return True if self.hField.hVerBord[x][y] else False

    def _pause(self):
        if self.hRobot.delay != 0:
            time.sleep(self.hRobot.delay)

    def state_check(self):
        if is_star_to_end(self.hField.hFig):
            raise NotSaveError

        if not self.isServiceable:
            raise ServiceError

    def delay_off(self):
        self.delay = 0
        self.hRobot.delay = 0

    def delay_on(self):
        self.delay = self.delay_def
        self.hRobot.delay = self.delay_def
