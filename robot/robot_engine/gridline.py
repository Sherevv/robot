import matplotlib.lines as mlines


class GridLine:
    """
    GridLine - line of the field's grid
    """

    def __init__(self, xdata, ydata, ort, fig, axes):
        """
        :param xdata, ydata: - line points
        :param ort: - line orientation = 'ver' | 'hor'
        :param fig: - matplotlib figure
        :param axes: - matplotlib axes
        """
        self.hLine = mlines.Line2D(xdata, ydata,
                                   color='b',
                                   linestyle=':',
                                   linewidth=0.5,
                                   pickradius=0.1,
                                   picker=5,
                                   zorder=1)
        self.hFig = fig
        self.hAxes = axes
        self.hLine.robotdata = ort
        self.hAxes.add_line(self.hLine)

    def delete(self):
        """
        Removes the grid
        """
        if self.hLine in self.hAxes.lines:
            self.hAxes.lines.remove(self.hLine)
        self.hFig.canvas.draw()
