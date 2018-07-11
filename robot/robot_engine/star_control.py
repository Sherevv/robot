def add_star_to_end(hFig):
    """Add '*' to the end of a window name"""

    if not is_star_to_end(hFig):
        name = hFig.canvas.get_window_title()
        hFig.canvas.set_window_title(name + '*')


def is_star_to_end(hFig):
    """Check if '*' at the end of a window name"""
    name = hFig.canvas.get_window_title()

    if name[-1] == '*':
        return True
    else:
        return False


def del_star_to_end(hFig):
    """Delete '*' from the end of a window name"""

    if is_star_to_end(hFig):
        name = hFig.canvas.get_window_title()
        hFig.canvas.set_window_title(name[0:-1])
