def encode_side(side):
    """
    Return side index by letter
    :param side:  'n' | 'o' | 's' | 'w'
    :return:       0  |  1  |  2  |  3
    """

    if side and isinstance(side, str):
        side = side.lower()

    side_list = ['n', 'o', 's', 'w']
    try:
        return side_list.index(side)
    except IndexError:
        raise ValueError("Wrong side index")
