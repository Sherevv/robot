import os
import os.path
import pickle
import numpy as np
import matplotlib
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
from .body import BodyUndirected
from .body import BodyOriented
from .border import Border
from .gridline import GridLine
from .marker import Marker
from .tools.controls import add_tool_to_navigation, default_tools, clear_toolbar
from .helpers import eprint
from .star_control import *
from .dialog import save_file, open_file, input_integer
from .exeptions import RobotTypeError

matplotlib.rcParams['toolbar'] = 'toolmanager'


class Field(object):
    def __init__(self, obj, body=None, size=None):
        """
        Creates a field and initiates the properties of the generated obj object

        SYNTAX:
           obj = field( obj, body, name )
             self.field( obj, body, name, fSize )
                                       ( fSize is not an empty array! )

        AT BASELINE:
        - obj - object of class Robot.Robot ( not yet formed
        finally !!! )
        - body - reference to the constructor of the robot body ( function_handle )
        - name-mat - file of the form *.map ( file,
               containing the initial configuration of the field with the robot, or
               where this configuration will be saved after editing)

          In this case, if there are 3 actual parameters (including self), it is opened for
          edit and reuse an existing file, and if
          there are 4 actual parameters, then a new file is created

        - [fSize = 2-vector double = number of rows and columns
        cellular field ]

        RESULT:
        - initialized the values of the properties of obj
        - if there are only 3 input parameters, then the connection is loaded from
        the variable 'r' of the corresponding mat file is displayed in a special graphic window;
        you can edit this configuration and save it to a file if you want

        - if there are all 4 input parameters, the configuration is re-created

        When you save the file with the configuration, the standard dialog will be opened for
        file selection.

        When you open a window with a checkered field of the specified size, the initial
        the position of the robot is the lower left corner. With the mouse, the robot can be dragged
        to any other cell, the initial location of the marred cells and
        the alignment of partitions between kletkami also carried out with the mouse.
        """

        self.borderWidth = 4
        self.borderColor = 'b'
        self.size = [5, 3]
        self.obj = obj
        self.hFrame = False
        self.is_texts = False
        self.hTexts = None
        self.hVerBord = None
        self.hHorBord = None
        self.hMark = None
        self.tMap = []
        self.hRobot = None
        self.body = body

        if size is not None:
            self.size = size

        # create Figure
        self.hFig = plt.figure()
        plt.gca().set_aspect('equal')  # save field scale
        self.hAxes = self.hFig.add_subplot(111)
        self.gridLines = []

        # setup Toolbar
        clear_toolbar(self.hFig.canvas.manager.toolmanager)
        for tool in default_tools:
            add_tool_to_navigation(tool, self.hFig)

        self.hAxes.robotdata = {'r': obj, 'f': self}
        self.hFig.canvas.callbacks.connect('pick_event', self.button_down_to_grid)
        self.hFig.canvas.callbacks.connect('button_press_event', self.button_down_to_cage)
        self.hFig.canvas.callbacks.connect('button_press_event', self.button_down_to_text)
        self.hFig.canvas.mpl_connect('key_press_event', self.window_key_press)
        self.draw()

    def draw(self):
        """ Create and draw field """
        self.hTexts = np.empty(self.size, dtype=object)
        self.hVerBord = np.empty(self.size, dtype=object)
        self.hHorBord = np.empty(self.size, dtype=object)
        self.hMark = np.empty(self.size, dtype=object)
        self.tMap = np.random.randint(-10, 10, size=self.size)

        # scale the axis area to fill the whole figure
        self.hAxes.set_position([0, 0, 1, 1])

        # get rid of axes and everything (the figure background will show through)
        self.hAxes.set_axis_off()

        # scale the plot area conveniently (the board is in 0,0..18,18)
        self.hAxes.set_xlim(-0.1, self.size[0] + 0.1)
        self.hAxes.set_ylim(-0.1, self.size[1] + 0.1)
        self.hRobot = self.body([0, 0], self.hFig)

        tool = self.hFig.canvas.manager.toolmanager.get_tool('FrameTool')
        if tool.toggled is False:
            tool.trigger(self, None)

        self.obj.hRobot = self.hRobot
        self.grid_create()

    def restore(self):
        """ Create field from saved data """

        with open(os.path.join(self.obj.fPath, self.obj.fName), 'rb') as f:
            r = pickle.load(f)

        self.size = r.get('size')

        if r.get('delay'):
            if self.obj.delay != 0:
                self.set_delay(r.get('delay'))
            else:
                self.obj.delay_def = r.get('delay')

        if r.get('effects') is not None:
            self.obj.isEffectOn = r.get('effects')

        self.grid_delete()
        self.markers_delete()
        self.borders_delete()
        self.frame_delete()

        tool = self.hFig.canvas.manager.toolmanager.get_tool('FrameTool')
        if tool.toggled is True:
            tool.trigger(self, None)

        self.hAxes.set_xlim(-0.1, self.size[0] + 0.1)
        self.hAxes.set_ylim(-0.1, self.size[1] + 0.1)
        self.grid_create()

        if r.get('isFrame') is True:
            tool.trigger(self, None)

        self.obj.isServiceable = True

        if r.get('robot_type') == 'Robot':
            if not isinstance(self.obj.hRobot, BodyUndirected):
                self.obj.hRobot.delete()
                self.obj.hRobot = BodyUndirected([0, 0], self.hFig)
        elif r.get('robot_type') in ['RobotOrt', 'RobotRot']:
            if not isinstance(self.obj.hRobot, BodyOriented):
                self.obj.hRobot.delete()
                self.obj.hRobot = BodyOriented([0, 0], self.hFig)
        else:
            raise RobotTypeError

        # restore robot object on the field
        self.obj.hRobot.shift(r.get('hRobot_position', (0, 0)), 'punct')

        # restore initial borders
        self.hVerBord = r.get('hVerBord')
        self.hHorBord = r.get('hHorBord')
        self.borders_restore()

        # restore initial markers
        self.obj.outMarkPos = np.empty((0, 2), int)
        self.hMark = r.get('hMark')
        self.markers_restore()

        self.tMap = r.get('tMap')

        del_star_to_end(self.hFig)

    def save(self, dialog=True):
        """
        In the CURRENT folder saves the current situation in a Mat file with the name of the person.name's
        (or in another file selected in the dialog) in the variable p, if
        only the file extension does not match .Map (capital letters)

        If you select a different file, the selected file name is saved
        in the obj object, and in the name field ( p = frames )
        """
        r = {
            'hVerBord': self.copy_for_restore(self.hVerBord),
            'hHorBord': self.copy_for_restore(self.hHorBord),
            'hMark': self.copy_for_restore(self.hMark),
            'tMap': self.tMap,
            'hRobot_position': self.hRobot.position,
            'robot_type': self.obj.robotType,
            'isFrame': True if self.hFrame else False,
            'size': self.size,
            'delay': self.obj.delay_def,
            'effects': self.obj.isEffectOn
        }

        if dialog:

            filepath = save_file(self.obj.fName)

            if not filepath:
                return False

            self.obj.fPath = os.path.dirname(filepath)
            self.obj.fName = os.path.basename(filepath)
        else:
            filepath = os.path.join(self.obj.fPath, self.obj.fName)

        with open(filepath, 'wb') as f:
            pickle.dump(r, f)

        self.hFig.canvas.set_window_title(self.obj.robotType + ' - ' + filepath)
        del_star_to_end(self.hFig)

        return True

    def load(self):
        """ Load field state from a map file """

        filepath = open_file(self.obj.fName, self.obj.fPath)

        if not filepath:
            return False

        self.obj.fPath = os.path.dirname(filepath)
        self.obj.fName = os.path.basename(filepath)

        self.hFig.canvas.set_window_title(self.obj.robotType + ' - ' + filepath)

        self.restore()

        del_star_to_end(self.hFig)

        return True

    def grid_create(self):
        """Create lines for grid"""

        n = self.size[0]
        m = self.size[1]
        # draw the grid
        for x in range(n + 1):
            line = GridLine([x, x], [0, m], 'ver', self.hFig, self.hAxes)
            self.gridLines.append(line)

        for y in range(m + 1):
            line = GridLine([0, n], [y, y], 'hor', self.hFig, self.hAxes)
            self.gridLines.append(line)

    def borders_restore(self):
        """ Restore borders """

        for ix in range(self.hHorBord.shape[0]):
            for iy in range(self.hHorBord.shape[1]):
                if self.hHorBord[ix][iy]:
                    xdata = [ix, ix + 1]
                    ydata = [iy, iy]
                    self.hHorBord[ix][iy] = Border(xdata, ydata, self.hFig, self.hAxes)

        for ix in range(self.hVerBord.shape[0]):
            for iy in range(self.hVerBord.shape[1]):
                if self.hVerBord[ix][iy]:
                    xdata = [ix, ix]
                    ydata = [iy, iy + 1]
                    self.hVerBord[ix][iy] = Border(xdata, ydata, self.hFig, self.hAxes)

    def copy_for_restore(self, arr):
        """ Create an array with boolean values """
        dest = np.empty(arr.shape, dtype=object)
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                if arr[i][j]:
                    dest[i][j] = True
                else:
                    dest[i][j] = False
        return dest

    def markers_restore(self):
        """ Restore markers on the field """

        for i in range(self.hMark.shape[0]):
            for j in range(self.hMark.shape[1]):
                if self.hMark[i][j]:
                    self.hMark[i][j] = Marker(i, j, self.hAxes)

    def grid_delete(self):
        """ Remove all grid lines from the field """

        for i in range(len(self.gridLines)):
            self.gridLines[i].delete()
        self.gridLines = []

    def borders_delete(self):
        """ Remove all borders from the field """

        for iy in range(self.hHorBord.shape[0]):
            for ix in range(self.hHorBord.shape[1]):
                if self.hHorBord[iy][ix]:
                    self.hHorBord[iy][ix].delete()
                    self.hHorBord[iy][ix] = False

        for iy in range(self.hVerBord.shape[0]):
            for ix in range(self.hVerBord.shape[1]):
                if self.hVerBord[iy][ix]:
                    self.hVerBord[iy][ix].delete()
                    self.hVerBord[iy][ix] = False
        self.hFig.canvas.draw()
        add_star_to_end(self.hFig)

    def markers_delete(self):
        """ Remove all markers from the field """

        for i in range(self.hMark.shape[0]):
            for j in range(self.hMark.shape[1]):
                if self.hMark[i][j]:
                    self.hMark[i][j].delete()
                    self.hMark[i][j] = False
        self.hFig.canvas.draw()
        add_star_to_end(self.hFig)

    def frame_create(self):
        """ Show field frame """
        if not self.hFrame:
            self.hFrame = mlines.Line2D(xdata=[0, 0, self.size[0], self.size[0], 0],
                                        ydata=[0, self.size[1], self.size[1], 0, 0],
                                        linewidth=self.borderWidth + 1,
                                        color='b', zorder=10)

            self.hAxes.add_line(self.hFrame)
        self.hFig.canvas.draw()

    def frame_delete(self):
        """ Hide field frame """
        if self.hFrame:
            self.hAxes.lines.remove(self.hFrame)
            self.hFrame = False
        self.hFig.canvas.draw()

    def window_key_press(self, eventdata=None):
        """
        Provides
        - ability to change the value of the delay
        when you press CTRL + plus or CTRL + minus
        - ability to move the robot to position (0, 0)
        when you press CTRL + R

        :param eventdata  - structure with the following fields (see matplotlib 'key_press_event')
            key: name of the key that was pressed, in lower case
        """

        if eventdata.key == 'ctrl++':
            self.set_delay(self.hRobot.delay * 2)
            print('Set delay time:', str(self.hRobot.delay), 'sec.')
        if eventdata.key == 'ctrl+-':
            self.set_delay(self.hRobot.delay / 2)
            print('Set delay time:', str(self.hRobot.delay), 'sec.')
        if eventdata.key == 'ctrl+r':
            self.obj.hRobot.shift([0, 0], 'punct')
            print('Robot moved to left bottom corner')

    def window_button_down(self, h=None, d=None, ):
        """
        Prevents the possibility of editing the environment when
        the robot is outside the field or markers have been set
        off the pitch
        """
        # TODO: make work

        if self.outside == 'none' and (self.is_out == 1 or not self.outMarkPos):
            eprint(
                'You cannot edit the field environment when the robot is outside '
                'the visible part of the field or markers have been set behind it. '
                'To be able to edit the situation, you need to restore the result '
                'of the last save by pressing CTRL+R')
            return
        pass

    def window_button_motion(self):
        """
        'Captures' robot and drags it with the left mouse button pressed on the tip of the cursor
        """

        self.obj.isServiceable = True
        add_star_to_end(self.hFig)

    def button_down_to_grid(self, event):
        """
        Set the partition between two adjacent cells when clicking the grid line
        ( the appropriate Robot class method is used to remove the partition.Border )
        - - or = 'hor' | 'ver'
        Records the fact of changing the situation (adds * to the end of the name
        window title)
        """

        try:
            a = event.artist.robotdata
        except AttributeError:
            return

        x, y = (event.mouseevent.xdata, event.mouseevent.ydata)

        ort = event.artist.robotdata  # ort
        if ort == 'ver':
            y = np.floor(y)
            x = round(x)

            i = int(x)  # the line index of the matrix hVerBord
            j = int(y)  # the column index of the matrix hVerBord

            if i < 1 or i >= self.size[0]:
                return

            xdata = [x, x]
            ydata = [y, y + 1]

            if not self.hVerBord[i][j]:
                self.hVerBord[i][j] = Border(xdata, ydata, self.hFig, self.hAxes)
            else:
                self.hVerBord[i][j].delete()
                self.hVerBord[i][j] = False

        elif ort == 'hor':
            y = round(y)
            x = np.floor(x)

            i = int(x)  # the line index of the matrix hHorBor
            j = int(y)  # the column index of the matrix hHorBor

            if j < 1 or j >= self.size[1]:
                return

            xdata = [x, x + 1]
            ydata = [y, y]
            if not self.hHorBord[i][j]:
                self.hHorBord[i][j] = Border(xdata, ydata, self.hFig, self.hAxes)
            else:
                self.hHorBord[i][j].delete()
                self.hHorBord[i][j] = False

        else:
            raise ValueError()

        self.hFig.canvas.draw()
        add_star_to_end(self.hFig)
        return True

    def button_down_to_cage(self, event=None):
        """
        Set the marker when clicking the mouse on the field
        Records the fact of changing the situation (adds * to the end of the name
        window title)
        """

        try:
            a = event.artist.robotdata
            return
        except AttributeError:
            pass

        if self.is_texts:
            return

        x, y = (event.xdata, event.ydata)

        if not x or not y:
            return

        xf = np.floor(x)
        yf = np.floor(y)
        xd = abs(x - xf)
        yd = abs(y - yf)

        if (0.8 < xd or xd < 0.2) or (0.2 > yd or yd > 0.8):
            return

        # xf, yf - lower left corner of the cage
        i = int(xf)
        j = int(yf)

        if self.hRobot.position[0] == i and self.hRobot.position[1] == j:
            return

        if not self.hMark[i][j]:
            self.hMark[i][j] = Marker(xf, yf, self.hAxes)
        else:
            self.hMark[i][j].delete()
            self.hMark[i][j] = False

        self.hFig.canvas.draw()

        add_star_to_end(self.hFig)
        return True

    def button_down_to_text(self, event=None):
        """
        Open dialog for asking temperature value by clicking the mouse on the field
        """

        try:
            a = event.artist.robotdata
            return
        except AttributeError:
            pass

        if not self.is_texts:
            return

        x, y = (event.xdata, event.ydata)

        if not x or not y:
            return

        xf = np.floor(x)
        yf = np.floor(y)
        xd = abs(x - xf)
        yd = abs(y - yf)

        if (0.8 < xd or xd < 0.2) or (0.2 > yd or yd > 0.8):
            return

        i = int(xf)
        j = int(yf)

        if self.hRobot.position[0] == i and self.hRobot.position[1] == j:
            return

        self.text_edit(i, j)

        self.hFig.canvas.draw()

    def tmpr_text_trigger(self):
        """ Create/remove text with temperature in caves from values in self.tMap """

        if not self.is_texts:
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    t = self.tMap[i][j]
                    self.hTexts[i][j] = self.hAxes.text(i + 0.4, j + 0.35, str(t),
                                                        color='b',
                                                        bbox={'fill': True,
                                                              'edgecolor': 'k',
                                                              'facecolor': 'w',
                                                              'linewidth': 1,
                                                              'boxstyle': 'round'},
                                                        zorder=100)
            self.is_texts = True

        else:
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    if self.hTexts[i][j]:
                        self.hTexts[i][j].remove()
            self.is_texts = False

    def text_edit(self, i, j):
        """
        Allows you to edit the cell temperature
        i,j - indices of the cells

        RECORDS the fact of change (possible) of a situation (adds * to the end of a name
        window title)
        """

        add_star_to_end(self.hFig)

        self.hTexts[i][j].set_color('r')

        t = input_integer(self.tMap[i][j])

        if not t and t != 0:
            self.hTexts[i][j].set_color('b')
            return

        self.hTexts[i][j].set_text(t)
        self.hTexts[i][j].set_color('b')
        self.tMap[i][j] = t

    def set_delay(self, delay):
        """
        Set delay for operations
        :param delay:
        """
        self.hRobot.delay = delay
        self.obj.delay = delay
        self.obj.delay_def = delay

    def add_grid_column(self):
        """ Add one column to the field """

        tool = self.hFig.canvas.manager.toolmanager.get_tool('FrameTool')
        if tool.toggled is True:
            self._trigger_tool('FrameTool')
        plt.cla()
        self.size[0] += 1
        self.draw()

    def remove_grid_column(self):
        """ Remove one column from the field """

        tool = self._get_tool('FrameTool')
        if tool.toggled is True:
            self._trigger_tool('FrameTool')

        self.size[0] -= 1
        plt.cla()
        self.draw()

    def add_grid_row(self):
        """ Add one row to the field """

        tool = self._get_tool('FrameTool')
        if tool.toggled is True:
            self._trigger_tool('FrameTool')

        plt.cla()
        self.size[1] += 1
        self.draw()

    def remove_grid_row(self):
        """ Remove one row from the field """

        tool = self._get_tool('FrameTool')
        if tool.toggled is True:
            self._trigger_tool('FrameTool')

        self.size[1] -= 1
        plt.cla()
        self.draw()

    def _trigger_tool(self, name):
        """ Trigger tool by name """
        self.hFig.canvas.manager.toolmanager.trigger_tool(name)

    def _get_tool(self, name):
        """ Get tool by name """
        return self.hFig.canvas.manager.toolmanager.get_tool(name)
