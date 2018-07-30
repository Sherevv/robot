import sys
import os
from ..exceptions import MapfileExtensionError, SideValueError


def eprint(*args, **kwargs):
    """
    Print error in console
    """
    print(*args, file=sys.stderr, **kwargs)


def mapfile_check(mapfile):
    """
    Checks map file parameter, raise errors
    :param mapfile: file path string
    """
    if not isinstance(mapfile, str) or len(mapfile) < 5:
        raise ValueError('The parameter should be a string')

    __, ext = os.path.splitext(mapfile)
    if ext != '.map':
        raise MapfileExtensionError

    if not os.path.isfile(mapfile):
        raise FileNotFoundError('The file ' + mapfile + ' is non found')


def decode_side(side):
    """
    Return side letter by index
    :param side:  0  |  1  |  2  |  3
    :return:     'n' | 'o' | 's' | 'w'
    """

    side_list = ['n', 'o', 's', 'w']
    try:
        return side_list[side]
    except IndexError:
        raise SideValueError


def encode_side(side):
    """
    Return side index by letter
    :param side:  'n' | 'o' | 's' | 'w'
    :return:       0  |  1  |  2  |  3
    """

    if side and isinstance(side, str):
        side = str.lower(side)
    else:
        raise SideValueError

    side_list = ['n', 'o', 's', 'w']
    try:
        return side_list.index(side)
    except IndexError:
        raise SideValueError
