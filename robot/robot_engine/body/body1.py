import time
import numpy as np
from .body import Body
from .rot_data import rot_data


class Body1(Body):
    """
    # Body1 - класс для визуального моделирования поведения ориентированного
    # робота ( < handle )
    #
    # Методы:
    # shift, rot, mark, is_mark, is_bord, meas
    """

    def __init__(self, coordinates=None, hFig=None, side=None):
        """Конструктор ориентированного робота и его графического образа

        СИНТАКСИС:
              r = Body1( coordinates, hFig, side )
        - coordinates = [x, y]  - декартовы координаты левого нижнего угла ячейки
        - hFig = дескриптор графического окна робота
        - side = 0 | 1 | 2 | 3

              r = Body1( R, hFig )
        - R = объект класса Robot.Body1 | объект класса Robot.Body4
        """

        self.side = 0  # = 0 | 1 | 2 | 3

        # if nargin == 2:
        #
        #     if strcmp(mclass(coordinates), 'Robot.Body1') == 1:
        #         side = coordinates.side
        #     elif strcmp(mclass(coordinates), 'Robot.Body4') == 1:
        #         side = 0  # - ориентация на Север
        #     else:
        #         # error
        #         mstring(
        #             'Входной параметр должен быть объектом класса Robot.Body1 или Robot.Body4')
        #
        #     coordinates = np.flipud(coordinates.position) - 1
        #
        # if ischar(side):
        #     # error
        #     'Значение side должно быть  0 | 1 | 2 | 3'

        super().__init__(coordinates, hFig)
        self.side = 0
        # = 0 | 1 | 2 | 3

        if side == 1:
            self.rot('RIGHT')
        elif side == 2:
            self.rot('BACK')
        elif side == 3:
            self.rot('LEFT')

        self.hL[0].set_facecolor('g')

        # set(self.hL(3), 'ButtonDownFcn',
        #     lambda h, d: self.rot_('BACK', hFig))
        # set(self.hL(2), 'ButtonDownFcn',
        #     lambda h, d: self.rot_('RIGHT', hFig))
        # set(self.hL(4), 'ButtonDownFcn',
        #     lambda h, d: self.rot_('LEFT', hFig))

    def shift(self, coord=None, mode=None):
        """без задержки сдвигает изображение робота с сохранением ориентации на вектор
        coord или в точку coord с фиксацией ориентации на Север
        - в зависимости от значения параметра mode

        - coord = 2-вектор double = координаты вектора перемещения | координаты центра корпуса
        - mode = 'vector' (для программного перемещения) | 'punct'(для ручного перемещения)
        Фиксирует факт изменения обстановки (добавляет * в конец имени
        заголовка окна)
        """

        super().shift(coord, mode)

        if mode == 'punct':
            self.side = 0

    def rot(self, side=None):
        """Выполняет поворот  на 90 или 180 градусов влево или вправо - в
        зависимости от значения side вокруг центра робота
        - side = 'Left' | 'Right' | 'Back' ( значение регистра не важно )
        Если имело место редактирования обстановки, то открывает диалог
        для сохранения результата редактирования и удаляет * в конце
        имени окна
        """

        #             Robot.Control.SaveDialog( self.hFig )

        side = str.upper(side)
        if side in ('LEFT', 'L'):
            phi = np.pi / 2
            self.side = np.mod(self.side - 1, 4)
        elif side in ('RIGHT', 'R'):
            phi = -np.pi / 2
            self.side = np.mod(self.side + 1, 4)
        elif side in ('BACK', 'B'):
            phi = np.pi
            self.side = np.mod(self.side + 2, 4)

        else:
            # error
            print('НЕ предусмотренное значение параметра')
        # switch upper( side )

        point = self.position + 0.5
        # координаты центра робота

        for i in range(4):
            xData, yData  = self.hL[i].xy
            xData, yData = rot_data(xData + self.L/2, yData + self.L/2, phi, point)
            self.hL[i].xy = (xData - self.L/2, yData - self.L/2)

    def is_bord(self):
        """Визуализирует факт проверки
        с установленной временной задержкой
        """
        self.update_facecolor_hl('g', [1])

    def get_side(self):
        """Визуализирует факт возвращения направления
        с установленной временной задержкой
        """
        self.update_facecolor_hl('r', [1, 3])

    def update_facecolor_hl(self, uclr, hli):
        clr = self.hL[1].get_facecolor()
        for idx in hli:
            self.hL[idx].set_facecolor(uclr)
        self.hFig.canvas.draw()
        time.sleep(self.delay)
        for idx in hli:
            self.hL[idx].set_facecolor(clr)
        self.hFig.canvas.draw()

    def sond_data_init(self):
        """создает массивы данных для лапок робота, центр которого
        находится в начале координат ( в точке (0,0) )
        """

        self.xData_0_L[0] = 0
        self.yData_0_L[0] = self.R

        for i in range(1, 5):
            if i != 4:
                self.xData_0_L[i], self.yData_0_L[i] = rot_data(
                    self.xData_0_L[i - 1], self.yData_0_L[i - 1], -np.pi / 2, [0, 0])
            self.xData_0_L[i - 1] -= self.L / 2
            self.yData_0_L[i - 1] -= self.L / 2

        # self.xData_0_L = [0,0,0,0]
        # self.yData_0_L = [0,0,0,0]
        #
        # L = self.L
        # pi = np.pi
        # t = np.array([-pi/4, -pi/2 , -3*pi/4], dtype=float)  # [ -np.pi, / 4  :  -np.pi / 2  :  -3 * np.pi / 4 ]
        # segmXData = L * np.sqrt(2) * np.cos(t)
        # segmYData = L * np.sqrt(2) * np.sin(t)
        # xData_0 = np.array([0,  L/2,  -L/2], dtype=float)    # np.array([0, [segmXData]], dtype=float)
        # yData_0 =  np.array([ L/2 + self.R, -L/2 + self.R, -L/2 + self.R], dtype=float) # ;np.array([L / 2, segmYData], dtype=float)
        # self.xData_0_L[0] = xData_0
        # self.yData_0_L[0] = yData_0 #+ self.R
        #
        # self.xData_0_L[2] = xData_0
        # self.yData_0_L[2] = yData_0 #- 0.75 * self.R
        #
        # xData_0 = [-L / 2, L / 2, L / 2, - L / 2]
        # yData_0 = [L / 2, - 0.5 * L, - 1.5 * L, - L / 2]
        # self.xData_0_L[1] = xData_0 #+ self.R
        # self.yData_0_L[1] = yData_0
        #
        # #             xData_0 = [-L/1.5 L/1.5  L/1.5 -L/1.5];
        # #             yData_0 = [ L/2 L/2 -L/2 -L/2];
        # #             self.xData_0_L{3} = xData_0;
        # #             self.yData_0_L{3} = yData_0 - self.R;
        #
        # xData_0 = np.array([-L / 2, L / 2, L / 2 - L / 2], dtype=float)
        # yData_0 = np.array([-0.5 * L, L / 2 - L / 2 - 1.5 * L], dtype=float)
        # self.xData_0_L[3] = xData_0 #- self.R
        # self.yData_0_L[3] = yData_0

    def rot_(self, side=None, hFig=None):
        """Выполняет поворот  на 90 или 180 градусов влево или вправо - в
        зависимости от значения side вокруг центра робота
        - side = 'Left' | 'Right' | 'Back' ( значение регистра не важно )
        ФИКСИРУЕТ факт изменения обстановки (добавляет * в конец имени
        заголовка окна)
        - hFig - дескриптор графического окна робота
        """

        self.rot(side)

        # обстановка изменена
        # Robot.Control.AddStarToEnd(hFig)
