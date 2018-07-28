import matplotlib.pyplot as plt
from .robot_engine import RobotEngine
from .robot_engine.exeptions import (WindowClosedError,
                                     NotSaveError,
                                     SideRotValueError)
from .robot_engine.helpers import mapfile_check
from .robot_engine import star_control
from .robot_engine.encode_side import encode_side
from .robot_engine.decode_side import decode_side


class RobotBase:

    def __init__(self, mapfile=None):
        """
        Robot - The constructor of a class

        SYNTAX:
           r = Robot()
           r = Robot( mapfile )
        WHERE:
        - mapfile = Name of a mat-file with initial conditions
        - r = The reference to the created object

        -------------------------------------------------------------
        All methods of a class Robot:
         step, is_bord, mark, is_mark, get_tmpr

        :param mapfile: Name of a mat-file with initial conditions


        In the 1st case, the standard dialog box opens for
        in case of failure, the file selection dialog opens for
        definition of field options

        In the 2nd case:
        - mapfile - the name of the file where the field situation is stored

        RESULT:
        - r = reference (handle ) to the created Robot class object

        -------------------------------------------------------------
        Robot command interface ( class methods ):
            step, is_bord, mark, is_mark, get_tmpr

        --------------------------------------------------------------
        Change ( install or edit ) the initial situation
        on the field, you can use the mouse:
         - click on a cell to set a marker
         - click on the marker to delete the marker
         - click on the dotted grid line of the checkered field sets
         partition
         - clicking on the partition removes the partition
         - click on the robot and move the mouse when the key is left
         moves the robot after the cursor to the desired cell
         (a" faulty "robot can also be "repaired" this way )
        After any number of such actions, the robot is immediately ready for the command
        management

        -------------------------------------------------------------
        If r.outside = 'none' , it is considered that the field is bounded by a frame
            r.outside = 'ismark', it is considered that the outside of the frame completely installed markers
            r.outside = 'nomark', it is considered that outside the scope of the original markers no

        At r.outside is not equal to 'none' is considered that all partitions closely adjacent to the field frame
        ( which in this case is not considered as a fence ),
        thought continued to infinity in the invisible part of the field in the appropriate directions
        ( the invisible part of the field is always invisible )

        -------------------------------------------------------------
        Save the result of MANUAL editing of the situation on the field
        you can use CTRL+S
        ( the window with the robot should be current! )

        You can restore the last saved situation on the field using
        keyboard shortcuts CTRL+R ( the window with the robot must be current! )

        You can view the cell temperature values by using the key combination
        CRTL+T ( the window with the robot must be current! )
        Pressing this key combination again removes the temperature values from the
        cells'.
        Visualized temperature values can be edited ( editing results
        operativnoi saved only in memory, to save on disk
        requires CTRL+S )

        It is possible to dynamically change the delay time of robot commands using
        Ctrl+plus or CTRL+minus, respectively
        ( the window with the robot should be current! )

        hRobotEngine-reference to the object of the RobotEngine class (robot on a cellular field)
        """
        if not mapfile:
            mapfile = ''
        else:  # checks mapfile
            mapfile_check(mapfile)

        self.mapfile = mapfile

        self.hRobotEngine = None

        self.init_data()

        if self.hRobotEngine:
            self.hRobotEngine.hField.hFig.robotdata = self

    def init_data(self):
        """
        Initialize data
        :return:
        """
        # self.hRobotEngine = RobotEngine(self.mapfile, 'Robot')
        pass

    def step(self, side):
        """
        Move the Robot on one step to the set side

        SYNTAX:
                   r.step( side )

        WHERE:
         - side = 'n' | 's' | 'o' | 'w'
         - r = The handle to object of class Robot
        """

        self.robot_check()
        self.hRobotEngine.step(side)

    def mark(self):
        """
        Put a marker in a current cage

        SYNTAX:
                r.mark()

        WHERE:
         - r = The handle to object of class Robot
        """

        self.robot_check()
        self.hRobotEngine.mark()

    def is_mark(self):
        """
        Returns result of stock-taking of a marker in a current cage

        SYNTAX:
                    ansv = r.is_mark()

        WHERE:
         - r = The handle to object of class Robot
         - ansv = True | False

        :return boolean
        """

        self.robot_check()
        return self.hRobotEngine.is_mark()

    def get_tmpr(self):
        """
        Returns value of temperature in a current cage

        SYNTAX:
                val = r.get_tmpr()

        WHERE:
         - r = The handle to object of class Robot

        :return temperature ( double )
        """

        self.robot_check()
        return self.hRobotEngine.get_tmpr()

    def robot_check(self):
        """
        Make checks for correct robot work
        """
        if not plt.fignum_exists(self.hRobotEngine.hField.hFig.number):
            raise WindowClosedError

        if star_control.is_star_to_end(self.hRobotEngine.hField.hFig):
            raise NotSaveError


class Robot(RobotBase):
    """
    Robot on a cellular field

    Directions of movement and obstacle checks are set ABSOLUTE values: North, South, West, East
    """

    def init_data(self):
        """
        Initialize data
        :return:
        """
        self.hRobotEngine = RobotEngine(self.mapfile, 'Robot')

    def step(self, side):
        """step - Moves the Robot on one step to the set side
        
        SYNTAX:
                   r.step( side )
        
        WHERE:
         - side = 'n' | 's' | 'o' | 'w'
         - r = The handle to object of class Robot
        """

        self.robot_check()
        self.hRobotEngine.step(side)

    def is_bord(self, side=None):
        """
        is_bord - Returns result of stock-taking of a border in the set side
            
            SYNTAX:
                      ansv = r.is_bord( side )
            
            WHERE:
             - side = 'n' | 's' | 'o' | 'w' 
             - r = The handle to object of class Robot
             - ansv = 1 ( true ) | 0 ( false ) 
        :param side: 
        :return: 
        """

        self.robot_check()
        return self.hRobotEngine.is_bord(side)


class RobotRelBase(RobotBase):
    """
    """

    def forward(self):
        """
        forward-command to move the robot forward to the next cell

        SYNTAX:
                  R.forward( )

        GIVEN:
        - - r = reference to an object of class Rob_roy:
                    robot in some cell of the field, right at the course of the robot
          partition no

        RESULT:
        - The robot in the next cell in the direction of side (if
          only on the way of the robot there is no partition, otherwise
          there is a "breakdown" of the robot )
        """

        self.robot_check()

        side = self.hRobotEngine.get_side_()

        self.hRobotEngine.step(side)

    def get_side(self):
        """
        get_side - command to communicate the current direction of the robot

        SYNTAX:
            side = r.get_side()

        GIVEN:
            - r = reference to an object of class Rob_roy:
            a robot in a cage

        RESULT:
            - side = ' n '(North) | ' s '(South) | ' o '(East) | ' w ' (West))
            - current direction of the robot
        """

        self.robot_check()
        return self.hRobotEngine.get_side()


class RobotOrt(RobotRelBase):
    """
    The RobotOrt class, each object of this class is
        a reference (handle ) to an object representing an EXECUTOR of a " oriented robot on a cellular field"

    Command interface ( class methods ):
        forward, right, left, is_born, mark, is_mark, get_side, get_tmpr

    The direction of travel, turns and check for obstacles are set
    ON:
      step forward; turn left; turn right;
      check if there is an obstacle right on the course

        See also a SIMILAR Robotron class
    """

    def init_data(self):
        """
        Initialize data
        :return:
        """
        self.hRobotEngine = RobotEngine(self.mapfile, 'RobotOrt')

    def left(self):
        """
        left - command to turn the robot to the left

        SYNTAX:
            r.left( )

        GIVEN:
            - r = reference to an object of class Rob_rel:
            the robot is in some cell of the field

        RESULT:
            - - Works deployed to the left at 90 degrees
        """

        self.robot_check()
        self.hRobotEngine.rot('Left')

    def right(self):
        """
        right - command to deploy the robot to the right

        SYNTAX:
                  r.right( )

        GIVEN:
        - r = reference to an object of class Rob_rel:
                    the robot is in some cell of the field

        RESULT:
        - - robot deployed to the right at 90 degrees
        """

        self.robot_check()
        self.hRobotEngine.rot('Right')

    def is_bord(self):
        """
        is_born-command to check presence of partition in front of robot

        SYNTAX:
                 ansv = r.is_bord( )

        GIVEN:
        - r = reference to an object of class Rob_rel:
                    the robot is in some cell of the field

        RESULT:
        - - ansv = 1 (True) if there is a partition in the side direction
               = 0 (False) - otherwise
        :return:
        """

        self.robot_check()

        side = self.hRobotEngine.get_side_()

        return self.hRobotEngine.is_bord(side)


class RobotRot(RobotRelBase):
    """
    The Robot class, each object of this class is
    a reference (handle ) to an object that represents
            CONTRACTOR " oriented robot on a cellular field"

    Command interface ( class methods ):
        forward, rat, is_born, mark, is_mark, get_side, get_tmp

    The direction of travel, turns and check for obstacles are set
    ON:
      step forward; turn left; turn right;
      check if there is an obstacle right on the course, left, right

    ************************************************************************
    It DIFFERS from the RobotOrt class in that instead of two methods, left and
        right in the Robotron class, there is only one method, rot, but with a parameter,
    which can have 3 values: 'left', 'right', 'back '(or'l',
    'r','b')
        and also because the is_born method has a parameter that can
    accept also 3 values: 'forward', 'left', 'right'

    """

    def init_data(self):
        """
        Initialize data
        """
        self.hRobotEngine = RobotEngine(self.mapfile, 'RobotRot')

    def rot(self, side=None):
        """
        rot - command to turn the robot left, right or back

        SYNTAX:
            r.rot( side )

        GIVEN:
            - - r = reference to an object of class Rob_roy:
            the robot is in some cell of the field
            - side = 'l' ('left') | ' r ' ('right') | ' b ' ('back')
        RESULT:
            - - Works deployed to the left at 90 degrees
        :param side:
        """

        self.robot_check()
        self.hRobotEngine.rot(side)

    def is_bord(self, side=None):
        """
        is_bored - command to check partitions in a given direction

        SYNTAX:
                                  ansv = r.is_board( side )

        GIVEN:
        - - r = reference to an object of class Rob_roy:
                    the robot is in some cell of the field
        - side = 'forward' ('f') | 'left' ('l') | 'right' ('r'))

        RESULT:
        - - ansv = 1 (true) if there is a partition in the side direction
               = 0 (false) - otherwise
        """

        self.robot_check()

        abs_side = self.hRobotEngine.get_side_()

        abs_side = encode_side(abs_side)

        if side:
            side = str.upper(side)
        else:
            raise SideRotValueError

        if side in ('LEFT', 'L'):
            abs_side = (abs_side - 1) % 4
        elif side in ('RIGHT', 'R'):
            abs_side = (abs_side + 1) % 4
        elif side in ('FORWARD', 'F'):
            # direction remains the same
            pass
        else:
            raise SideRotValueError

        abs_side = decode_side(abs_side)

        return self.hRobotEngine.is_bord(abs_side)
