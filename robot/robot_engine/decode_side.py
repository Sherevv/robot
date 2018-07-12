from .exeptions import SideValueError


def decode_side(side):
    """
    Return side letter by index
    :param side:  0  |  1  |  2  |  3
    :return:     'n' | 'o' | 's' | 'w'
    """

    if side and isinstance(side, str):
        side = side.lower()
    else:
        raise SideValueError

    side_list = ['n', 'o', 's', 'w']
    try:
        return side_list[side]
    except IndexError:
        raise SideValueError
