import sys
import os
from .exeptions import MapfileExtensionError


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def mapfile_check(mapfile):
    """
    Checks map file parameter, raise errors
    """
    if not isinstance(mapfile, str) or len(mapfile) < 5:
        raise ValueError('The parameter should be a string')

    __, ext = os.path.splitext(mapfile)
    if ext != '.map':
        raise MapfileExtensionError

    if not os.path.isfile(mapfile):
        raise FileNotFoundError('The file ' + mapfile + ' is non found')
