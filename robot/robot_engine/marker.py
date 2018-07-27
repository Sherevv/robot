import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from .star_control import add_star_to_end


class Marker:
    """
    Class Marker - cell marker

    Methods: constructor, delete
    Has the patch property of the corresponding graphic object
    """

    def __init__(self, xf, yf, axes):
        """
        :param xf, yf: - coordinates of the lower left corner of the cell
        :param axes: - matplotlib axes
        """

        self.hAxes = axes
        # x0, y0 - the coordinates of the center of the cell
        x0 = xf + 0.5
        y0 = yf + 0.5

        self.hPatch = mpatches.Circle((x0, y0), .15,
                                      facecolor='m',
                                      edgecolor='m',
                                      linewidth=0.5,
                                      clip_on=False,
                                      zorder=10,
                                      picker=5)

        self.hAxes.add_patch(self.hPatch)

    def delete(self):
        """
        Remove marker
        Records the change of the scene (adds * to the end of the window title)
        """

        self.hAxes.patches.remove(self.hPatch)
        add_star_to_end(plt.gcf())
