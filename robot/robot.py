import os
import matplotlib.pyplot as plt
from .robot_engine import RobotEngine
from .robot_engine.exeptions import RobotException, WindowClosedError, MapfileExtensionError, NotSaveError
from .robot_engine.helpers import eprint, mapfile_check
from .robot_engine import star_control


class Robot:
    """
    Robot on a cellular field

    Directions of movement and obstacle checks are set ABSOLUTE values: North, South, West, East
    """

    def __init__(self, mapfile=None):
        """
        Robot - The constructor of a class

        SYNTAX:
           r = Robot()
           r = Robot( mapfile )
        WHERE:
        - mapfile = Name of a mat-file with initial conditions
        - r = The reference to the created object

        -------------------------------------------------------------
        All methods of a class Robot:
         step, is_bord, mark, is_mark, get_tmpr

        :param mapfile: Name of a mat-file with initial conditions

        #
        # Robot - конструктор класса
        #
        # СИНТАКСИС:
        #       r = Robot()
        #       r = Robot( mapfile )
        #
        # В 1-ом случае открвается стандартное диалоговое окно для
        # выбора файла, в случае отказа, открывается диалог для
        # определения параметров поля
        #
        # Во 2-м случае:
        # - mapfile - имя файла, в котором сохранена обстановка на поле
        #
        # РЕЗУЛЬТАТ:
        # - r = ссылка ( handle ) на созданный объект класса Robot
        #
        # -------------------------------------------------------------
        # Kомандный интерфейс робота ( методы класса ):
        #     step, is_bord, mark, is_mark, get_tmpr
        #
        # --------------------------------------------------------------
        # Изменить ( установить или отредактировать ) начальную обстановку
        # на поле можно с помощью мыши:
        #  -клик по клетке устанавливает маркер
        #  -клик по маркеру удаляет маркер
        #  -клик по пунктирной линии сетки клетчатого поля устанавливает
        #  перегородку
        #  -клик по перегородке удаляет перегородку
        #  -клик по роботу и перемещение мыши при неотпущенной клавише
        #  перемещает робота вслед за курсором в нужную клетку
        #  ( "неисправного" робота также можно "починить" таким способом )
        # После любого числа таких действий робот сразу готов к командному
        # управлению
        #
        # -------------------------------------------------------------
        # Если r.outside = 'none', то считается, что поле ограничено рамкой
        #     r.outside = 'ismark', то считается, что за пределами рамки сплошь установлены маркеры
        #     r.outside = 'nomark', то считается, что за пределами рамки исходно маркеров нет
        #
        # При r.outside не равном 'none' считается, что все перегородки, вплотную примыкающие к рамке поля
        # ( которая в данном случае не рассматривается как ограждение ),
        # мыслятся продолженными до бесконечности в невидимую часть поля в соответствующих направлениях
        # ( невидимая часть поля всегда остается невидимой )
        #
        # -------------------------------------------------------------
        # Сохранить результат РУЧНОГО редактирования обстановки на поле
        # можно с помощью комбинации клавиш CTRL+S
        # ( при этом окно с роботом должно быть текущим! )
        #
        # Восстановить последнюю сохраненную обстановку на поле можно с помощью
        # комбинации клавиш CTRL+R ( при этом окно с роботом должно быть текущим! )
        #
        # Просмотреть значения температур клеток можно с помощью коьбинации клавиш
        # CRTL+T ( при этом окно с роботом должно быть текущим! )
        # Повторное нажатие этой комбинации клавиш убирает значения температур из
        # клеток.
        # Визуализированные значения температур можно редактировать ( результаты редактирования
        # сохраняются только в опреративной памяти, для сохранения на диске
        # требуется CTRL+S )
        #
        # Динамически менять время задержки выполнения команд робота мможно с помощью
        # комбинации клавиш CTRL+"плюс" или CTRL+"минус", соответственно
        # ( при этом окно с роботом должно быть текущим! )

        # hRobotEngine - ссылка на объект класса RobotEngine (робот на клетчатом поле)
        """
        if not mapfile:
            mapfile = ''
        else:  # checks mapfile
            try:
                mapfile_check(mapfile)
            except (ValueError, MapfileExtensionError, FileNotFoundError) as e:
                eprint(e)
                return

        self.hRobotEngine = RobotEngine(mapfile, 'Robot')

        if self.hRobotEngine:
            self.hRobotEngine.hField.hFig.robotdata = self

    def step(self, side):
        """step - Moves the Robot on one step to the set side
        
        SYNTAX:
                   r.step( side )
        
        WHERE:
         - side = 'n' | 's' | 'o' | 'w'
         - r = The handle to object of class Robot
        """

        try:
            self.robot_check()
            self.hRobotEngine.step(side)
        except RobotException as e:
            eprint(e)

    def is_bord(self, side=None):
        """
        is_bord - Returns result of stock-taking of a border in the set side
            
            SYNTAX:
                      ansv = r.is_bord( side )
            
            WHERE:
             - side = 'n' | 's' | 'o' | 'w' 
             - r = The handle to object of class Robot
             - ansv = 1 ( true ) | 0 ( false ) 
        :param side: 
        :return: 
        """

        try:
            self.robot_check()
            return self.hRobotEngine.is_bord(side)
        except RobotException as e:
            eprint(e)

    def mark(self):
        """
        Puts a marker in a current cage
            
        SYNTAX:
                r.mark()

        WHERE:
         - r = The handle to object of class Robot
        """

        try:
            self.robot_check()
            self.hRobotEngine.mark()
        except RobotException as e:
            eprint(e)

    def is_mark(self):
        """
        Returns result of stock-taking of a marker in a current cage
            
        SYNTAX:
                    ansv = r.is_mark()

        WHERE:
         - r = The handle to object of class Robot
         - ansv = True | False

        :return boolean
        """

        try:
            self.robot_check()
            return self.hRobotEngine.is_mark()
        except RobotException as e:
            eprint(e)

    def get_tmpr(self):
        """
        Returns value of temperature in a current cage

        SYNTAX:
                val = r.get_tmpr()

        WHERE:
         - r = The handle to object of class Robot

        :return temperature ( double )
        """

        try:
            self.robot_check()
            return self.hRobotEngine.get_tmpr()
        except RobotException as e:
            eprint(e)

    def robot_check(self):
        """
        Make checks for correct robot work
        """
        if not plt.fignum_exists(self.hRobotEngine.hField.hFig.number):
            raise WindowClosedError

        if star_control.is_star_to_end(self.hRobotEngine.hField.hFig):
            raise NotSaveError
