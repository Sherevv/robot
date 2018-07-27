def add_star_to_end(fig):
    """
    Add '*' to the end of a window name

    :param fig: matplotlib figure
    """

    if not is_star_to_end(fig):
        name = fig.canvas.get_window_title()
        fig.canvas.set_window_title(name + '*')


def is_star_to_end(fig):
    """
    Check if '*' at the end of a window name

    :param fig: matplotlib figure
    """
    name = fig.canvas.get_window_title()

    if name[-1] == '*':
        return True
    else:
        return False


def del_star_to_end(fig):
    """
    Delete '*' from the end of a window name

    :param fig: matplotlib figure
    """

    if is_star_to_end(fig):
        name = fig.canvas.get_window_title()
        fig.canvas.set_window_title(name[0:-1])
