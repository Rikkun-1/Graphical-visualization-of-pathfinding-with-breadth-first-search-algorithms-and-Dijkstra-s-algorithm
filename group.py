"""
Маленький командир, отвечающий за ровное и пропорциональное отображение
подчиненных виджетов(кнопок).
"""

import color
import pygame
import time

class Group:

    def __init__(self, pos = [0, 0], width = 0, line_weight = 0, gap = 2, square_buttons = False,
            text_scale_multiplier = 1, text_y_offset = 0):


        self.x      = pos[0]
        self.y      = pos[1]
        self.width  = width
        self.gap    = gap
        self.line_weight           = line_weight
        self.square_buttons        = square_buttons
        self.text_scale_multiplier = text_scale_multiplier
        self.text_y_offset         = text_y_offset

        self.widgets = []
        self.widgets_to_update = []


    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]


    def append(self, item):
        self.widgets.append(item)


    def update(self):
        widgets = self.widgets_to_update
        for i in widgets:
            if i.update() == True:
                self.widgets_to_update.remove(i)


    def click(self, pos):
        if self.x < pos[0] < self.x + self.width:
            for widget in self.widgets:
                if widget != "\n":
                    if widget.click(pos):
                        if not widget in self.widgets_to_update:
                            self.widgets_to_update.append(widget)
                        if widget.radio == True:
                            for i in self.widgets:
                                if i != "\n" and i.radio == True and i != widget:
                                    i.onReleased()


    def draw(self, screen):
        gap = self.gap

        i = j = 0
        button_width  = round((self.width-3*gap)/self.line_weight)
        button_height = button_width if self.square_buttons else round(button_width*0.64)
        if button_height < 22: button_height = 22

        text_scale  = round(button_height / 2.3 * self.text_scale_multiplier)
        font        = pygame.font.SysFont("arial", text_scale)

        for widget in self.widgets:
            if widget == "\n":
                i = 0
                j += 1
                continue

            weight = widget.weight
            if weight != 0:
                x = self.x + i * (button_width+gap)
                y = self.y + j * (button_height+gap)
                width = button_width * weight + ((weight-1)*gap)
                widget.draw(screen, [x, y], [width, button_height], font, text_scale, self.text_y_offset)
                i += weight
