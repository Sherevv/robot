class RobotException(Exception):
    message = __doc__

    def __init__(self, message=None, *args):
        if message:
            self.message = message
        super(RobotException, self).__init__(self.message, *args)


class ServiceError(RobotException):
    """The robot is not serviceable"""
    message = __doc__


class BrokenError(RobotException):
    """Fatal error: the Robot has driven into a partition (border)"""
    message = __doc__


class NotSaveError(RobotException):
    """Conditions in the field are NOT SAVE after editing"""
    message = __doc__


class SideValueError(RobotException):
    """Not admissible value of SIDE parameter, admissible values: 'n' | 's' | 'o' | 'w'"""
    message = __doc__


class SideOrdValueError(RobotException):
    """Not admissible value of SIDE parameter, admissible values: 'Left' | 'Right' | 'Back' (case no matter)"""
    message = __doc__


class SideRotValueError(RobotException):
    """Not admissible value of SIDE parameter, admissible values: 'forward' ('f') |'left' ('l') | 'right' ('r')"""
    message = __doc__


class RobotTypeValueError(RobotException):
    """Wrong value for robot_type parameter"""
    message = __doc__


class RobotTypeError(RobotException):
    """Wrong robot type"""
    message = __doc__


class WindowClosedError(RobotException):
    """The window with the robot has been closed"""
    message = __doc__


class MapfileExtensionError(RobotException):
    """The map file name should have extension .map"""
    message = __doc__


class EditFieldOutError(RobotException):
    """
    You cannot edit the field environment when the robot is outside
    the visible part of the field or markers have been set behind it.
    To be able to edit the situation, you need to restore the result
    of the last save by pressing CTRL+R
    """
    message = __doc__


class FieldSizeTypeError(RobotException):
    """ Field size values must be integer """
    message = __doc__


class FieldSizeValueError(RobotException):
    """ Field size values must be positive """
    message = __doc__


class IsFrameValueError(RobotException):
    """ Field is_frame value must be bool """
    message = __doc__
