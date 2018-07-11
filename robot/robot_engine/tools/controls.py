from matplotlib.backend_tools import ToolBase, ToolToggleBase
from matplotlib.backend_managers import ToolEvent
from ...robot import *

ICON_DIR = os.path.dirname(os.path.abspath(__file__))  # Current dir


class RobotTool(object):
    @property
    def r(self):
        return get_current_field()

    @property
    def f(self):
        gca = plt.gca()
        return gca.robotdata['f']


class ToolBaseCustom(ToolBase, RobotTool):
    pass


class ToolToggleBaseCustom(ToolToggleBase, RobotTool):
    pass


class WidthPlusTool(ToolBaseCustom):
    """Add one column to field"""
    # keyboard shortcut
    default_keymap = 'w'
    description = 'Add column'
    group = 'navigation'
    image = os.path.join(ICON_DIR, 'icons8-add-column-32.png')

    def trigger(self, *args, **kwargs):
        print('add column')

        plt.cla()
        self.f.size[0] += 1
        self.f.draw()


class WidthMinusTool(ToolBaseCustom):
    """Drop one column from field"""
    # keyboard shortcut
    default_keymap = 'e'
    description = 'Remove column'
    group = 'navigation'
    image = os.path.join(ICON_DIR, 'icons8-delete-column-32.png')

    def trigger(self, *args, **kwargs):
        print('drop column')

        if self.f.size[0] > 1:
            self.f.size[0] -= 1
            plt.cla()
            self.f.draw()
        else:
            print('cant drop')


class HeightPlusTool(ToolBaseCustom):
    """Add one row to field"""
    # keyboard shortcut
    default_keymap = 'h'
    description = 'Add row'
    group = 'navigation'
    image = os.path.join(ICON_DIR, 'icons8-add-row-32.png')

    def trigger(self, *args, **kwargs):
        print('add column')

        plt.cla()
        self.f.size[1] += 1
        self.f.draw()


class HeightMinusTool(ToolBaseCustom):
    """Drop one row from field"""
    # keyboard shortcut
    default_keymap = 'j'
    description = 'Remove row'
    group = 'navigation'
    image = os.path.join(ICON_DIR, 'icons8-delete-row-32.png')

    def trigger(self, *args, **kwargs):
        print('Drop row')

        if self.f.size[1] > 1:
            self.f.size[1] -= 1
            plt.cla()
            self.f.draw()
        else:
            print('cant drop')


class SaveTool(ToolBaseCustom):
    """Save field to file"""
    # keyboard shortcut
    default_keymap = 's'
    description = 'Save field'
    group = 'io'
    image = os.path.join(ICON_DIR, 'icons8-save-32.png')

    def trigger(self, *args, **kwargs):
        print('Save field')

        self.f.save()


class RestoreTool(ToolBaseCustom):
    """Restore field from file"""
    # keyboard shortcut
    default_keymap = 'r'
    description = 'Restore field'
    group = 'io'
    image = os.path.join(ICON_DIR, 'icons8-sync-32.png')

    def trigger(self, *args, **kwargs):
        print('Restore field')

        self.f.restore()


class LoadTool(ToolBaseCustom):
    """Load field from file"""
    # keyboard shortcut
    default_keymap = 'ctrl+l'
    description = 'Load field'
    group = 'io'
    image = os.path.join(ICON_DIR, 'icons8-open-32.png')

    def trigger(self, *args, **kwargs):
        print('Load field')

        self.f.load()


class DelayTool(ToolToggleBaseCustom):
    """Remove delay"""
    # keyboard shortcut
    default_keymap = 'd'
    description = 'Remove delay'
    group = 'zoompan'
    image = os.path.join(ICON_DIR, 'icons8-speedometer-32.png')

    def enable(self, *args):
        print('enable delay')

        self.r.delay_off()

    def disable(self, *args):
        print('disable delay')

        self.r.delay_on()


class ValuesTool(ToolToggleBaseCustom):
    """Show values on field"""
    # keyboard shortcut
    default_keymap = 't'
    description = 'Show values'
    group = 'zoompan'
    image = os.path.join(ICON_DIR, 'icons8-text-box-32.png')

    def enable(self, *args):
        print('enable show values')
        self.f.tmpr_text_trigger()

    def disable(self, *args):
        print('disable show values')
        self.f.tmpr_text_trigger()


class FrameTool(ToolToggleBaseCustom):
    """Drop one row from field"""
    # keyboard shortcut
    default_keymap = 'b'
    description = 'Toggle frame'
    group = 'zoompan'
    image = os.path.join(ICON_DIR, 'icons8-add-image-32.png')

    def enable(self, *args):
        print('enable frame')

        self.f.frame_create()

    def disable(self, *args):
        print('disable frame')

        self.f.frame_delete()


def clear_toolbar(toolbar):
    def_tools = ['home', 'back', 'forward',
                 'zoom', 'pan',
                 # 'subplots',
                 'save',
                 ]
    try:
        for tool in def_tools:
            if toolbar.get_tool(tool):
                toolbar.remove_tool(tool)

        tool = toolbar.get_tool('subplots')
        s = 'tool_removed_event'
        event = ToolEvent(s, toolbar, tool)
        toolbar._callbacks.process(s, event)

        toolbar._remove_keys('subplots')
        del toolbar._tools['subplots']
    except:
        pass


def add_tool_to_navigation(cls, fig):
    fig.canvas.manager.toolmanager.add_tool(cls.__name__, cls)
    fig.canvas.manager.toolbar.add_tool(cls.__name__, cls.group, 1)


default_tools = [WidthPlusTool, WidthMinusTool, HeightPlusTool, HeightMinusTool, FrameTool, ValuesTool, DelayTool,
                 RestoreTool, SaveTool, LoadTool]


def get_current_field():
    gca = plt.gca()
    return gca.robotdata['r']
