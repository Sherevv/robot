import matplotlib.lines as mlines
from .star_control import add_star_to_end


class Border:
    """
    The Border class is an element of partitions

    Methods: constructor, destructor - delete
    Has the hLine property-the descriptor of the corresponding graphic object
    """

    def __init__(self, xdata, ydata, fig, axes):
        """
        :param xdata, ydata: - line points
        :param fig: - matplotlib figure
        :param axes: - matplotlib axes
        """
        self.hLine = mlines.Line2D(xdata, ydata,
                                   linewidth=4,
                                   color='b',
                                   picker=5,
                                   zorder=10)
        self.hFig = fig
        self.hAxes = axes
        self.hAxes.add_line(self.hLine)

    def delete(self):
        """
        Removes the border
        Records the change of scene (adds * to the end of the window title)
        """

        self.hAxes.lines.remove(self.hLine)
        add_star_to_end(self.hFig)
