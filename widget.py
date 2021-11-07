"""
Здесь находятся все возможные кнопки, которые размещены на панели меню.
"""

import color
import pygame
import time

pygame.font.init()

class Widget:

        def __init__(self, id = 0, weight = 1, color_pack = color.GREY_PACK, text = "",
            clickable = True, switch = False, radio = False, text_pos_modifier = [1, 1]):
            # weight отвечает за то, сколько места в группе (group.py) занимает эта клетка по отношению к другим
            # text_pos_modifier требуется для выведения особых ascii символов, которые съезжат при попытке вывести их
            # просто так

            self.id     = id
            self.x      = 0
            self.y      = 0
            self.width  = 0
            self.height = 0
            self.weight = weight
            self.text_pos_modifier = text_pos_modifier

            if radio: switch = False
            self.clickable = clickable  # Ее можно нажать?
            self.switch    = switch     # Это переключатель?
            self.radio     = radio      # Это радио кнопка? (это как переключатель,
                                        # но единовременно может быть активна только одна из групппы)

            self.color_pack = list(color_pack)
            self.text       = text
            self.__text     = None # Отрендеренный текст, готовый к расположению на поверхности

            self.isPressed = False
            self.time_when_pressed = 0


        def update(self):
            current_time = time.time()
            if current_time - self.time_when_pressed > 0.2 and not self.switch and not self.radio:
                self.onReleased()
                return True
            return False


        def onReleased(self):
            if self.isPressed:
                self.isPressed = False


        def click(self, pos):
            if self.clickable:
                if self.x < pos[0] < self.x + self.width:
                    if self.y < pos[1] < self.y + self.height:
                        self.onClick()
                        return True
            return False


        def onClick(self):
            old_time = self.time_when_pressed
            self.time_when_pressed = time.time()

            if self.isPressed == False and not self.switch:
                self.isPressed = True

            if self.switch and self.time_when_pressed - old_time > 0.15 and not self.radio:
                self.isPressed = not self.isPressed


        def draw(self, screen, pos, size, font, text_scale, text_y_offset):

            width  = size[0]
            height = size[1]

            x  = pos[0];     x1 = x + width
            y  = pos[1];     y1 = y + height

            self.x = x ;     self.width  = width
            self.y = y ;     self.height = height

            l_sc = 1
            a = 1

            pygame.draw.rect(screen, self.color_pack[0],   [x, y, size[0], size[1]])
            if self.isPressed:
                pygame.draw.line(screen, self.color_pack[2], [x+a-1 , y     ],   [x+a-1 , y1    ], l_sc)   # left line
                pygame.draw.line(screen, self.color_pack[2], [x+a   , y1-a+1],   [x1-a  , y1-a+1], l_sc)   # bottom line
                pygame.draw.line(screen, self.color_pack[1], [x     , y+a-1 ],   [x1-1  , y+a-1 ], l_sc)   # top line
                pygame.draw.line(screen, self.color_pack[1], [x1-a  , y     ],   [x1-a  , y1    ], l_sc)   # right line
            else:
                pygame.draw.line(screen, self.color_pack[1], [x+a-1 , y     ],   [x+a-1 , y1    ], l_sc)   # left line
                pygame.draw.line(screen, self.color_pack[1], [x+a   , y1-a+1],   [x1-a  , y1-a+1], l_sc)   # bottom line
                pygame.draw.line(screen, self.color_pack[2], [x     , y+a-1 ],   [x1-1  , y+a-1 ], l_sc)   # top line
                pygame.draw.line(screen, self.color_pack[2], [x1-a  , y     ],   [x1-a  , y1    ], l_sc)   # right line

            offset = 1 if self.isPressed else 0
            if self.text:
                x_mod = self.text_pos_modifier[0]
                y_mod = self.text_pos_modifier[1]
                text = font.render(self.text, 1, color.FONT_ORANGE) # 2-й аргумент это сглаживание 1 - есть, 0 - нет
                b = text.get_height()
                screen.blit(text, (x+size[0]/2-len(self.text)*text_scale/5*x_mod-offset, y+b/2*y_mod+offset+text_y_offset))
