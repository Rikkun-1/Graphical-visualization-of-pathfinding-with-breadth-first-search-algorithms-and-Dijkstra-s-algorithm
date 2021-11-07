import time
from copy import deepcopy
import pygame

import color

"""
    Класс клетка. Именно она рисуется в СellGrid
    Сама по себе бесполезна. На базе нее создается объект класса
"""

class Cell():

    def __init__(self, color_pack = color.GREY_PACK):

        self.color_pack = color_pack
        self.text = ["", "", ""]
        self.__top_text     = None #
        self.__center_text  = None # Отрендеренный текст, готовый к расположению на поверхности
        self.__bottom_text  = None #

        self.isPressed         = False
        self.time_when_pressed = 0

        self.isClosed  = False
        self.isPath    = False
        self.isStart   = False
        self.isEnd     = False


    def update(self):
        current_time = time.time()

        if current_time - self.time_when_pressed > 0.3:
            self.isPressed = False
            self.onReleased()
            return True
        return False


    def onReleased(self):
        pass


    def onClick(self):
        self.time_when_pressed = time.time()
        if self.isPressed == False:
            self.isPressed = True


    def renderText(self, main_font, additional_font):
        # Рендер текста. Можно делать проще, но так красивше :3
        # Клетка не сама рендерит себе текст. Эту функию вызывает вышестоящий CellGrid
        # Он вызовет рендер текста только для тех клеток, которые сейчас видны.
        # Он main_font и additional_font это объекты класса pygame.font.SysFont
        # Смотри cellGrid.py prepareFonts()
        if self.isPath:
            self.__top_text     = additional_font.render(self.text[0], 1, color.PATH_COLOR)
            self.__center_text  =       main_font.render(self.text[1], 1, color.PATH_COLOR)
            self.__bottom_text  = additional_font.render(self.text[2], 1, color.PATH_COLOR)
        elif self.isClosed:
            self.__top_text     = additional_font.render(self.text[0], 1, color.CLOSED_COLOR)
            self.__center_text  =       main_font.render(self.text[1], 1, color.CLOSED_COLOR) # 2-й аргумент это сглаживание 1 - есть, 0 - нет
            self.__bottom_text  = additional_font.render(self.text[2], 1, color.CLOSED_COLOR)
        else:
            self.__top_text     = additional_font.render(self.text[0], 1, color.FONT_ORANGE)
            self.__center_text  =       main_font.render(self.text[1], 1, color.FONT_ORANGE)
            self.__bottom_text  = additional_font.render(self.text[2], 1, color.FONT_ORANGE)


    def draw(self, screen, pos, size, lineScale, textScale):
        
        x  = pos[0];     x1 = x + size
        y  = pos[1];     y1 = y + size

        l_sc = lineScale
        a = l_sc//2

        pygame.draw.rect(screen, self.color_pack[0],   [x, y, size, size]) # Рисуем основу
        if self.isPressed: # Рисуем светлую и темную часть кнопки. Они меняются местами при нажатии
            pygame.draw.line(screen, self.color_pack[2], [x+a-1 , y    ],   [x+a-1 , y1   ], l_sc)   # left line
            pygame.draw.line(screen, self.color_pack[2], [x+a   , y1-a ],   [x1-a  , y1-a ], l_sc)   # bottom line
            pygame.draw.line(screen, self.color_pack[1], [x     , y+a-1],   [x1-1  , y+a-1], l_sc)   # top line
            pygame.draw.line(screen, self.color_pack[1], [x1-a  , y    ],   [x1-a  , y1   ], l_sc)   # right line
        else:
            pygame.draw.line(screen, self.color_pack[1], [x+a-1 , y    ],   [x+a-1 , y1   ], l_sc)   # left line
            pygame.draw.line(screen, self.color_pack[1], [x+a   , y1-a ],   [x1-a  , y1-a ], l_sc)   # bottom line
            pygame.draw.line(screen, self.color_pack[2], [x     , y+a-1],   [x1-1  , y+a-1], l_sc)   # top line
            pygame.draw.line(screen, self.color_pack[2], [x1-a  , y    ],   [x1-a  , y1   ], l_sc)   # right line

        if size > 35: # Размещение текста
            offset = 1 if self.isPressed else 0
            screen.blit(self.__top_text,    (x+size/2-len(self.text[0])*textScale/8.4-offset , y + offset))
            screen.blit(self.__center_text, (x+size/2-len(self.text[1])*textScale/5  -offset , y + size/3.3 + offset))
            screen.blit(self.__bottom_text, (x+size/2-len(self.text[2])*textScale/8.4-offset , y + size/1.6 + offset))

            gap = 6
            if self.isStart: # Рисуем символ старта
                pygame.draw.line(screen  , color.START_COLOR, [x+gap , y+size/4  ],  [x+gap  , y+size/1.25   ], 2)    # left
                pygame.draw.line(screen  , color.START_COLOR, [x1-gap-1, y+size/4],  [x1-gap-1  , y+size/1.25], 2)    # right
                pygame.draw.aaline(screen, color.START_COLOR, [x+gap , y+size/4  ],  [x1-gap-1, y+size/1.25  ], True) # up to down
                pygame.draw.aaline(screen, color.START_COLOR, [x+gap, y+size/1.25],  [x1-gap-1, y+size/4     ], True) # down to up
            if self.isEnd: # Рисуем символ конца
                pygame.draw.line(screen, color.END_COLOR,   [x+gap , y+size/4  ],  [x+gap  , y+size/1.25   ], 2) # left
                pygame.draw.line(screen, color.END_COLOR,   [x1-gap-1, y+size/4],  [x1-gap-1  , y+size/1.25], 2) # right
        elif self.isStart : pygame.draw.rect(screen, color.START_COLOR , [x+2, y+2, size-4, size-4], 2)
        elif self.isEnd   : pygame.draw.rect(screen, color.END_COLOR   , [x+2, y+2, size-4, size-4], 2)
        elif self.isPath  : pygame.draw.rect(screen, color.PATH_COLOR  , [x+2, y+2, size-4, size-4], 2)
        elif self.isClosed: pygame.draw.line(screen, color.CLOSED_COLOR, [x+size/3, y+size/2],   [x+size/1.5  , y+size/2], 1) # top line
