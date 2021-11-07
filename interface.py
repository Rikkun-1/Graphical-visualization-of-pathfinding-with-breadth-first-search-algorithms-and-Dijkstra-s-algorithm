"""
    Здесь присходит инициализация интерфейса, а также хранится парочка функций, для работы с сеткой
"""

import pygame

from group import Group
from widget import Widget
from color import *

def selection_on_grid(grid, start_cell_pos, end_cell_pos, fill, color_pack = None):
    """
    # Лучше бы это перенести в cellGrid.py
    # Отвечает за закрашивание прямоугольных секторов на сетке.
    # grid - объект класса CellGrid
    # start_cell_pos, end_cell_pos - противоположные углоы прямоугольника в формате [i, j] [строка, столбец]
    # fill - bool - заполнять ли прямоугольник.
    """
    if end_cell_pos != False:
        if start_cell_pos[0] > end_cell_pos[0]:
            start_cell_pos[0], end_cell_pos[0] = end_cell_pos[0], start_cell_pos[0]

        if start_cell_pos[1] > end_cell_pos[1]:
            start_cell_pos[1], end_cell_pos[1] = end_cell_pos[1], start_cell_pos[1]

        if not fill:
                for j in range(start_cell_pos[1], end_cell_pos[1]+1): #top
                    grid.click_by_id(start_cell_pos[0], j)
                    if color_pack: grid.cells[start_cell_pos[0]][j].color_pack = color_pack

                for j in range(start_cell_pos[1], end_cell_pos[1]+1): #down
                    grid.click_by_id(end_cell_pos[0], j)
                    if color_pack: grid.cells[end_cell_pos[0]][j].color_pack = color_pack

                for i in range(start_cell_pos[0], end_cell_pos[0]): #left
                    grid.click_by_id(i, start_cell_pos[1])
                    if color_pack: grid.cells[i][start_cell_pos[1]].color_pack = color_pack

                for i in range(start_cell_pos[0], end_cell_pos[0]): #right
                    grid.click_by_id(i, end_cell_pos[1])
                    if color_pack: grid.cells[i][end_cell_pos[1]].color_pack = color_pack
        else:
            for i in range(start_cell_pos[0], end_cell_pos[0]+1):
                for j in range(start_cell_pos[1], end_cell_pos[1]+1):
                    grid.click_by_id(i, j)
                    if color_pack: grid.cells[i][j].color_pack = color_pack


def grid_scaling(grid, button, pos):
    if button == 4:
        grid.scale(grid.cell_size+grid.cell_size//10, pos[0], pos[1])
    if button == 5:
        grid.scale(grid.cell_size-grid.cell_size//10, pos[0], pos[1])

class Interface:
    groups = []

    def init():
        algo_group = Group(line_weight = 4, text_scale_multiplier = 1.15, text_y_offset = -5)
        algo_group.append(Widget(                 weight = 4, text = "Алгоритм", clickable = False))
        algo_group.append("\n")
        algo_group.append(Widget(id = "Wave"    , weight = 2, text = "Волновой", radio = True))
        algo_group.append(Widget(id = "Dijkstra", weight = 2, text = "Дейкстра", radio = True))

        pallete_group = Group(line_weight = 4, gap = 2, square_buttons = True)
        pallete_group.append(Widget(id = "StartPath" , weight = 1, color_pack = list(GREY_PACK)    , text = "A"))
        pallete_group.append(Widget(id = "EndPath"   , weight = 1, color_pack = list(GREY_PACK)    , text = "B"))
        pallete_group.append(Widget(id = "Weight 1"  , weight = 1, color_pack = list(GREY_PACK)    , text = "1"))
        pallete_group.append(Widget(id = "Weight inf", weight = 1, color_pack = list(BLACK_PACK)   , text = "" ))
        pallete_group.append("\n")
        pallete_group.append(Widget(id = "Weight 2"  , weight = 1, color_pack = list(SKY_PACK)     , text = "2"))
        pallete_group.append(Widget(id = "Weight 3"  , weight = 1, color_pack = list(BLUE_PACK)    , text = "3"))
        pallete_group.append(Widget(id = "Weight 4"  , weight = 1, color_pack = list(COBALT_PACK)  , text = "4"))
        pallete_group.append(Widget(id = "Weight 5"  , weight = 1, color_pack = list(PURPLE_PACK)  , text = "5"))
        pallete_group.append("\n")
        pallete_group.append(Widget(id = "Weight 6"  , weight = 1, color_pack = list(VIOLET_PACK)  , text = "6"))
        pallete_group.append(Widget(id = "Weight 7"  , weight = 1, color_pack = list(JAM_PACK)     , text = "7"))
        pallete_group.append(Widget(id = "Weight 8"  , weight = 1, color_pack = list(MAGENTA_PACK) , text = "8"))
        pallete_group.append(Widget(id = "Weight 9"  , weight = 1, color_pack = list(RED_PACK)     , text = "9" ))
        pallete_group.append("\n")
        pallete_group.append(Widget(id = "Weight 10" , weight = 1, color_pack = list(GREEN_PACK)   , text = "10"))
        pallete_group.append(Widget(id = "Weight 14" , weight = 1, color_pack = list(CELERY_PACK)  , text = "14"))
        pallete_group.append(Widget(id = "Weight 18" , weight = 1, color_pack = list(YELLOW_PACK)  , text = "18"))
        pallete_group.append("\n")
        pallete_group.append(Widget(id = "Weight 22" , weight = 1, color_pack = list(RUST_PACK)    , text = "22"))
        pallete_group.append(Widget(id = "Weight 25" , weight = 1, color_pack = list(ORANGE_PACK)  , text = "25"))

        stepper_group = Group(line_weight = 4)
        stepper_group.append(Widget(id = "PlayFrameLX1", weight = 1, text = "<"))
        stepper_group.append(Widget(id = "FrameField"  , weight = 2, text = "0"))
        stepper_group.append(Widget(id = "PlayFrameRX1", weight = 1, text = ">"))
        stepper_group.append("\n")
        stepper_group.append(Widget(id = "PlayFrameLX2" , weight = 1, text = "<<"))
        stepper_group.append(Widget(id = "PlayFrameLX3" , weight = 1, text = "<<<"))
        stepper_group.append(Widget(id = "PlayFrameRX3" , weight = 1, text = ">>>"))
        stepper_group.append(Widget(id = "PlayFrameRX2" , weight = 1, text = ">>"))

        Interface.groups = [algo_group, pallete_group, stepper_group]

    def recalculate(window_size):
        """
        Перерасчет положения и размеров групп при изменении размера окна. Позволяет интерфейсу масштабироваться.
        Изменение параметров групп заставит их пересчитать свои widgets
        """
        groups = Interface.groups
        algo_group    = groups[0]
        pallete_group = groups[1]
        stepper_group = groups[2]

        window_gap    = 10
        menu_x        = (window_size[0]-window_gap*2)*0.75+window_gap
        menu_y        = window_gap
        menu_width    = (window_size[0] - window_gap*2) * 0.25
        menu_height   = (window_size[1] - window_gap*2)
        menu_gap      = menu_width * 0.11
        group_width   = menu_width - menu_gap * 2

        group_x         = menu_x + menu_gap * 1.25
        algo_group_y    = menu_y + menu_gap * 0.5
        pallete_group_y = menu_y + menu_gap + menu_height * 0.10
        stepper_group_y = menu_y + menu_gap + menu_height * 0.75

        algo_group   .set_pos([group_x, algo_group_y   ])
        pallete_group.set_pos([group_x, pallete_group_y])
        stepper_group.set_pos([group_x, stepper_group_y])

        algo_group.width     = group_width
        pallete_group.width  = group_width
        stepper_group.width  = group_width

        Interface.groups = [algo_group, pallete_group, stepper_group]


    def draw(screen):
        for group in Interface.groups:
            group.draw(screen)


    def update():
        for group in Interface.groups:
            group.update()


    def click(pos):
        for group in Interface.groups:
            if group.click(pos):
                 # click() возвращает true, если Ты попал на какуето кнопку.
                 # Если мы уже попали, то рассматривать другие кнопки не нужно и break
                break


    def get_pressed():
        pressed_widgets = []
        for group in Interface.groups:
            for widget in group.widgets:
                if widget != "\n" and widget.isPressed == True:
                    pressed_widgets.append(widget)
        return pressed_widgets


    def get_widget_by_id(id): # Возвращает ссылку на widget объект
        for group in Interface.groups:
            for widget in group.widgets:
                if widget != "\n" and widget.id == id:
                    return widget
        return False
