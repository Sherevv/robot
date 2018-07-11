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
