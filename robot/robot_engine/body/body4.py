import numpy as np
from .rot_data import rot_data
from .body import Body


class Body4(Body):
    """
    # Body4 - класс для визуального моделирования поведения не ориентированного
    # робота ( < Robot.Body ( < handle ) )
    #
    # Protected - методы:
    #   sond_data_init ( перегрузка виртуального метода )
    #
    # Public - свойства:
    #   position, delay, moved ( наследуются от Robot.Body )
    """

    def __init__(self, coordinates, hfig):
        """
        # Конструктор ориентированного робота и его графического образа
        #
        # СИНТАКСИС:
        #       r = Body4( coordinates, hFig )
        # - coordinates = [x, y]  - декартовы координаты левого нижнего угла ячейки
        # - hFig = дескриптор графического окна робота
        #
        #       r = Body4( R, hFig )
        # - R = объект класса Robot.Body1 | объект класса Robot.Body4

        # if isequal(mclass(coordinates), 'Robot.Body1') or isequal(mclass(coordinates), 'Robot.Body4'):
        # if isinstance(coordinates, Body1) or isinstance(coordinates, Body4):
        #     coordinates = np.flipud(coordinates.position) - 1
        # elif not isreal(coordinates) and numel(coordinates) == 2:
        #
        #     # error
        #     print('Входной параметр должен быть объектом класса Robot.Body1
        # или Robot.Body4 или 2-вектором real doouble')
        :param coordinates:
        :param hfig:
        """

        super().__init__(coordinates, hfig)

    def sond_data_init(self):
        """
        # создает массивы данных для лапок робота, центр которого
        # находится в начале координат ( в точке (0,0) )
        """

        self.xData_0_L[0] = 0
        self.yData_0_L[0] = self.R

        for i in range(1, 5):
            if i != 4:
                self.xData_0_L[i], self.yData_0_L[i] = rot_data(
                    self.xData_0_L[i - 1], self.yData_0_L[i - 1], -np.pi / 2, [0, 0])
            self.xData_0_L[i - 1] -= self.L / 2
            self.yData_0_L[i - 1] -= self.L / 2
