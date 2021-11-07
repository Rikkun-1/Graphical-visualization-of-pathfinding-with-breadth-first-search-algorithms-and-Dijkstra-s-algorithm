"""
Непосредственно начальник клеток. Это структура заведует всеми клетками внутри себя.
После создания объекта этого класса он наполняется клетками заданного размера.
CellGrid сам подготавливает нужный размер шрифта для всех клеток внутри себя.
По обрабатывает клики, вычисляя положение клетки под курсором.
Отрисовает только те клетки, которые видны в данный момент.
"""

from math import ceil, floor
import pygame

import color
from cell import Cell

class CellGrid():

    def __init__(self, pos, size, rows, columns, cell_size = 100):
        self.x = pos[0]
        self.y = pos[1]
        self.width     = size[0]
        self.height    = size[1]
        self.__cell_size = cell_size

        self.__rows       = rows
        self.__columns    = columns
        self.__cursor     = [0, 0]
        # Курсор это условно начало отсчета для отрисовки
        # Когда вы тянете влево курсор тоже двигается в лево,
        # утягивая за собой всю сетку и вам кажется, будто вы прокручиваете справа налево.

        self.__line_scale = round(cell_size / 30)
        if self.__line_scale % 2 == 1: self.__line_scale += 1
        if self.__line_scale == 0: self.__line_scale = 1

        self.__gap = round(cell_size / 30)
        if self.__gap == 0: self__gap = 1

        self.__text_scale = round(self.__cell_size / 2.5)

        self.__main_font       = None
        self.__additional_font = None
        self.prepareFonts()

        self.cells_to_update = []
        # нажатые клетки, которые нужно время от времени проверять, что они ве еще нажаты(что анимация нажатия еще не прошла)

        self.cells = [0]*rows
        for i in range(0, rows):
            self.cells[i] = [0]*columns

        for i in range(0, rows):
            for j in range(0, columns):
                newCell = Cell()
                self.cells[i][j] = newCell

        end_row    = self.height // (self.__cell_size + self.__gap)
        end_column = self.width  // (self.__cell_size + self.__gap)
        for i in range(0, rows):
            for j in range(0, columns):
                self.cells[i][j].renderText(self.__main_font, self.__additional_font)

    def get_map(self):
        # Возвращает двумерный массив - карту с препятствиями и стоимостями прохождения для алгоритмов
        map = [0]*self.__rows
        for i in range(0, self.__rows):
            map[i] = [0]*self.__columns

        for i in range(0, self.__rows):
            for j in range(0, self.__columns):
                color_pack = self.cells[i][j].color_pack
                if color_pack == color.BLACK_PACK   : map[i][j] = 0
                if color_pack == color.GREY_PACK    : map[i][j] = 1
                if color_pack == color.SKY_PACK     : map[i][j] = 2
                if color_pack == color.BLUE_PACK    : map[i][j] = 3
                if color_pack == color.COBALT_PACK  : map[i][j] = 4
                if color_pack == color.PURPLE_PACK  : map[i][j] = 5
                if color_pack == color.VIOLET_PACK  : map[i][j] = 6
                if color_pack == color.JAM_PACK     : map[i][j] = 7
                if color_pack == color.MAGENTA_PACK : map[i][j] = 8
                if color_pack == color.RED_PACK     : map[i][j] = 9
                if color_pack == color.GREEN_PACK   : map[i][j] = 10
                if color_pack == color.CELERY_PACK  : map[i][j] = 14
                if color_pack == color.YELLOW_PACK  : map[i][j] = 18
                if color_pack == color.RUST_PACK    : map[i][j] = 22
                if color_pack == color.ORANGE_PACK  : map[i][j] = 25
        return map


    @property
    def cell_size(self):
        return self.__cell_size


    @property
    def cursor(self):
        return self.__cursor


    @cursor.setter
    def cursor(self, newCursor):
        # Здесь задается новый курсор. Данные приходят из main.py от обработчиков событий
        # Здесь же проверяется и то, чтобы новый свайп не выходил за пределы карты.
        # Но он не идеален. Попробуйте потыкаться в край сетки. Не вышло?
        # Попробуйте прижаться к стене, когда вы приближеннык клеткам, а затем отдалиться.
        # Вы увидите черный край, так как обработку этого Я не успел придумать.
        self.__cursor = newCursor

        if self.__cursor[0] > 0: self.__cursor[0] = 0
        if self.__cursor[1] > 0: self.__cursor[1] = 0

        a = (self.__cell_size + self.__gap) * (self.__columns) - self.width
        if self.__cursor[0] < -a:
             self.__cursor[0] = -a

        b = (self.__cell_size + self.__gap) * (self.__rows) - self.height
        if self.__cursor[1] < -b:
             self.__cursor[1] = -b


    def get_cell_pos_in_map(self, i, j):
        x = (self.__cell_size+self.__gap) * j + self.y + self.__cell_size//2
        y = (self.__cell_size+self.__gap) * i + self.x + self.__cell_size//2
        return [x, y]


    def update(self):
        cells = self.cells_to_update
        for i in cells:
            if i.update() == True:
                self.cells_to_update.remove(i)


    def click_by_id(self, i, j):
        self.cells[i][j].onClick()
        if not self.cells[i][j] in self.cells_to_update:
            self.cells_to_update.append(self.cells[i][j])


    def click(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                pos = [pos[0] - self.x, pos[1] - self.y]
                j = (-self.__cursor[0] + pos[0])//(self.__cell_size+self.__gap)
                i = (-self.__cursor[1] + pos[1])//(self.__cell_size+self.__gap)
                if 0 <= i < self.__rows:
                    if 0 <= j < self.__columns:
                        self.cells[i][j].onClick()
                        if not self.cells[i][j] in self.cells_to_update:
                            self.cells_to_update.append(self.cells[i][j])
                        return [i, j]
        return False


    def collision(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


    def scale(self, size, pos_x = 0, pos_y = 0):
        # О это веселая штучка. Отвечает за приближение
        # Я долго придумывал формулу, чтобы научить его приближать туда, куда смотрит курсор
        # и отдалять оттуда, куда опять таки смотрит курсор

        if size * self.__columns > self.width and size * self.__rows > self.height and size >= 16 and size < 200:
            x = self.__cursor[0]
            y = self.__cursor[1]
            old_size = self.__cell_size
            size_dif = size - old_size

            old_gap = self.__gap
            self.__gap = round(size / 30 + 1)
            if self.__gap == 0: self.__gap = 1
            gap_dif = self.__gap - old_gap

            x1 = floor(x + (size_dif+gap_dif)*((x-pos_x)/(old_size+old_gap)))
            y1 = floor(y + (size_dif+gap_dif)*((y-pos_y)/(old_size+old_gap)))
            self.cursor = [x1, y1]

            self.__cell_size = size

            self.__line_scale = round(size / 30)
            if self.__line_scale % 2 == 1: self.__line_scale += 1
            if self.__line_scale == 0: self.__line_scale = 1

            self.prepareFonts()


    def prepareFonts(self):
        # Готовит для всех клеток единый тип и размер шрифта
        self.__text_scale = round(self.__cell_size / 2.8)
        self.__main_font       = pygame.font.SysFont("arial", round(self.__text_scale))
        self.__additional_font = pygame.font.SysFont("arial", round(self.__text_scale/1.25))


    def draw(self, screen, pressed_mask = None,
             top_text_mask = None, center_text_mask = None, bottom_text_mask = None):

        pygame.draw.rect(screen, color.FULL_BLACK, [self.x, self.y, self.width, self.height])

        start_row    = -self.__cursor[1] // (self.__cell_size + self.__gap)
        start_column = -self.__cursor[0] // (self.__cell_size + self.__gap)
        end_column   = start_column + (self.width  + self.__cell_size*2+self.__gap) // (self.__cell_size + self.__gap)
        end_row      =    start_row + (self.height + self.__cell_size*2+self.__gap) // (self.__cell_size + self.__gap)

        if end_column >= self.__columns:
            end_column = self.__columns

        if end_row >= self.__rows:
            end_row = self.__rows

        a = self.__cell_size+self.__gap
        b = self.__cursor[1] + self.x
        c = self.__cursor[0] + self.y

        for i in range(start_row, end_row):
            y = a * i + b
            for j in range(start_column, end_column):
                x = a * j + c

                if pressed_mask:
                    if pressed_mask[i][j] != 0:
                        self.cells[i][j].isPressed = True
                        self.cells[i][j].isClosed  = True
                        if pressed_mask[i][j] == -1:
                              self.cells[i][j].isPath = True
                    else:
                        self.cells[i][j].isPressed = False
                        self.cells[i][j].isClosed  = False
                else:
                    self.cells[i][j].isClosed  = False
                    self.cells[i][j].isPath    = False

                if self.__cell_size > 35 and self.cells[i][j].color_pack != color.BLACK_PACK:
                    if center_text_mask and center_text_mask[i][j] not in [0, 1_000_000]:
                        self.cells[i][j].text[1] = str(center_text_mask[i][j])
                    else: self.cells[i][j].text[1] = ""
                else: self.cells[i][j].text[1] = ""

                self.cells[i][j].renderText(self.__main_font, self.__additional_font)
                self.cells[i][j].draw(screen, [x, y], self.__cell_size, self.__line_scale, self.__text_scale)

        pygame.draw.rect(screen, (255, 255, 255), [self.x, self.y, self.width, self.height], 1)
