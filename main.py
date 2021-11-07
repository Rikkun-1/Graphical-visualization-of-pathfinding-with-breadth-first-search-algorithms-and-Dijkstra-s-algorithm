import time
import os
import multiprocessing
from copy import deepcopy

def main():
    """
    Ну эт обработка интерфейса. Мне страшно это объяснять. Давайте вы сами просто поймете :3
    """
    import pygame

    import color
    import algoritms
    from cellGrid import CellGrid
    from interface import Interface, selection_on_grid, grid_scaling
    from group import Group
    from widget import Widget

    pygame.init()

    size = [1280, 720]
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE, depth = 16)
    pygame.display.set_caption("Гоша")

    clock = pygame.time.Clock()

    grid = CellGrid([10, 10], [round(size[0] * 0.75 + 10), 700], 60, 100, 50)
    grid.scale(50)

    Interface.init()
    Interface.recalculate(size)
    
    start_cell_pos = [0, 0]
    end_cell_pos = [0, 0]
    update_grid = True
    inter = False       # Переменная становится true в момент нажатия в пределах grid и остается таковой до тех пор,
                        # пока мышка не будет отпущена. Отвечает за возможность перемотки даже если мышь уже за пределами поля
    current_frame = 0
    frames = []
    # массив подготовленных кадров от algoritms.py
    # По мере выполнения алгоритма сюда будут подбрасываться кадры из queue
    queue = multiprocessing.Queue() # синхронизированная очередь для связи с потоком просчета алгоритма

    pressed_mask     = []
    # Маска нажатых кнопок. 0 - не нажата 1 нажата, -1 - она мало того что нажата, так еще и часть маршрута (Grid покрасит ее в зеленый :3)
    top_text_mask    = [] #
    center_text_mask = [] # Маски текста для клеток
    bottom_text_mask = [] #
    # Маски нужны для более эффективной работы с клетками.
    # Без них потребовалось бы присвоить новое значение каждой клетке. А так
    # Сетка поменяет значение только тех клеток, которые сейчас отображаются
    # Можно сделать лучше. Это можно сделать полем класса GridCell, тогда
    # это будет более цельным и логичным.
    # У меня же это так ибо проект очень быстро рос и его архитектура менялась очень стремительно.
    # А потому во всем коде встречаются как неплохие решения, так и хлам.
    # Времени реализовать все хорошо не хватало, а потому код похож на бред шизофреника
    # Решения разной степени бреда вместе выполняют одно задание
    # Старый код не переписывался, просто возле него писался более продуманный и привязывался к старому
    # Это и есть опыт : |   p.s. нет, это костыли :p

    algoritm_is_started = []
    brush_color = color.GREY_PACK

    start_pos = []
    end_pos   = []
    current_algorithm = None
    # ссылка на функцию с выбранным алгоритом. Она скармливается параллельному потоку
    # При запуске алгоритма
    last_play = 0
    # время последнего нажатия на клавишу проигрывания. Позволяет не пускать слюни, нажимая на проигрыватель
    # А на приятной скорости катиться по кадрам
    done = False
    while not done:
        clock.tick(60)
        screen.fill(color.VERY_GREY)

        mouse = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()
        rel = pygame.mouse.get_rel()
        grid_collision = grid.collision(pos)
        focused = pygame.mouse.get_focused()
        pressed_buttons = Interface.get_pressed()

        if not queue.empty():
            frames.append(queue.get())

        if update_grid:
            grid.update()
        grid.draw(screen, pressed_mask, top_text_mask, center_text_mask, bottom_text_mask)

        pygame.draw.rect(screen, color.VERY_GREY,  [0, 0, size[0], 10]) # top
        pygame.draw.rect(screen, color.VERY_GREY,  [0, size[1]-10, size[0], size[1]]) # bottom
        pygame.draw.rect(screen, color.VERY_GREY,  [0, 0, 10, size[1]]) # left
        pygame.draw.rect(screen, color.VERY_GREY,  [round((size[0]-20)*0.75+25), 0, size[0], size[1]]) #right

        Interface.update()
        Interface.draw(screen)

        current_time = time.time()
        play_delay = current_time - last_play  # delays between player button presses

        for button in pressed_buttons:
            if button.id == "Wave":
                current_algorithm = algoritms.BFS
            if button.id == "Dijkstra":
                current_algorithm = algoritms.dijkstra

            if (play_delay > 0.35) or \
               ("X2" in button.id and play_delay > 0.10) or \
               ("X3" in button.id and play_delay > 0.005):

                if "PlayFrameR" in button.id and not algoritm_is_started and start_pos and end_pos and current_algorithm:
                    process = multiprocessing.Process(target=current_algorithm, args=(queue, grid.get_map(), start_pos, end_pos))
                    process.start()
                    algoritm_is_started = True

                if "PlayFrameL" in button.id and current_frame - 1 >= 0:
                    last_play = current_time
                    current_frame -= 1

                    pressed_mask     = deepcopy(frames[current_frame][0])
                    center_text_mask = deepcopy(frames[current_frame][1])

                if "PlayFrameR" in button.id and current_frame + 2 < len(frames):
                    last_play = current_time
                    current_frame += 1

                    if frames[current_frame] == "endOfAlgorithm":
                        path = frames[current_frame + 1]
                        pressed_mask     = deepcopy(frames[current_frame-1][0])
                        center_text_mask = deepcopy(frames[current_frame-1][1])
                        for k in path:
                            i, j = k
                            pressed_mask[i][j] = -1
                    else:
                        pressed_mask     = list(frames[current_frame][0])
                        center_text_mask = list(frames[current_frame][1])

            if button.id == "FrameField" and algoritm_is_started:
                process.terminate()
                algoritm_is_started = False
                current_frame       = 0
                pressed_mask        = []
                top_text_mask       = []
                center_text_mask    = []
                bottom_text_mask    = []
                frames              = []
                for row in grid.cells:
                    for cell in row:
                        cell.isPressed = False

            if "Weight" in button.id:
                brush_color = button.color_pack

            if button.id == "StartPath":
                brush_color = "A"
            if button.id == "EndPath":
                brush_color = "B"

            FrameField = Interface.get_widget_by_id("FrameField")
            FrameField.text = str(current_frame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_1: brush_color = "A"
                if event.key == pygame.K_2: brush_color = "B"

            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                if width < 720:
                    width = 720
                if height < 405:
                    height = 405
                if width / height > 2.53:
                    height = round(width / 2.53)

                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                grid.width  = round(width*0.75)
                grid.height = round(height-20)
                size = [width, height]
                Interface.recalculate(size)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL or event.key == pygame.K_r:
                    start_cell_pos = [0, 0]

            if event.type == pygame.MOUSEBUTTONUP:
                update_grid = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and start_cell_pos != [0, 0]:
                    end_cell_pos = grid.click(event.pos)
                    fill = keys[pygame.K_LCTRL]
                    selection_on_grid(grid, start_cell_pos, end_cell_pos, fill, brush_color)
                    start_cell_pos = [0, 0]
                    end_cell_pos = [0, 0]
                    update_grid = False

                if (event.button == 4 or event.button == 5) and grid_collision and focused:
                    grid_scaling(grid, event.button, event.pos)

        if mouse[0] and not keys[pygame.K_LSHIFT]:
            Interface.click(pos)

            id = grid.click(pos)
            if id and not algoritm_is_started:
                i, j = id
                if brush_color == "A":
                    if start_pos:
                        m, k = start_pos
                        grid.cells[m][k].isStart = False
                    start_pos = [i, j]
                    grid.cells[i][j].isStart = True
                elif brush_color == "B":
                    if end_pos:
                        m, k = end_pos
                        grid.cells[m][k].isEnd = False
                    grid.cells[i][j].isEnd = True
                    end_pos = [i, j]
                else: grid.cells[i][j].color_pack = brush_color

                if (keys[pygame.K_LCTRL] or keys[pygame.K_r]) and start_cell_pos == [0, 0]:
                    start_cell_pos = id

        #print(clock.get_fps())
        if grid_collision or inter:
            if mouse[0] and keys[pygame.K_LSHIFT] or mouse[2]:
                grid.cursor = [grid.cursor[0] + rel[0]//3, grid.cursor[1] + rel[1]//3]
            inter = mouse[0] or mouse[2]

        pygame.display.update()
    pygame.quit()
    if algoritm_is_started:
        process.terminate()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
