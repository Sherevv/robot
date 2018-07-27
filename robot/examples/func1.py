def walk_to_bord(r, side):
    """
    The robot goes until it meets the wall in the specified direction

    :param r:    robot object
    :param side: move side
    """
    while not r.is_bord(side):
        r.step(side)
