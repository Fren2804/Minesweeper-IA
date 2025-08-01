import config
import pyautogui
import random
from PIL import ImageGrab

def init_table():
    table = [["-" for _ in range(config.cols)] for _ in range(config.rows)]
    return table

def obtain_table(table):
    screenshot_right = config.screenshot_left + (24 * config.cols)
    screenshot_bottom = (config.screenshot_top + 50) + (24 * config.rows)
    screenshot = ImageGrab.grab(bbox=(config.screenshot_left, config.screenshot_top, screenshot_right, screenshot_bottom))
    #screenshot.show()
    pixels = screenshot.load()
    color_flag_rel_x = config.x_flag - config.screenshot_left
    color_flag_rel_y = config.y_flag - config.screenshot_top
    color_number_rel_x = config.x_numbers - config.screenshot_left
    color_number_rel_y = config.y_numbers - config.screenshot_top
    if pixels[config.x_death, config.y_death] == (0, 0, 0):
        return 1
    if pixels[config.x_victory, config.y_victory] == (0, 0, 0):
        return 2
    for i in range(config.rows):
        for j in range(config.cols):
            color_corner = pixels[config.x_step * j + 1, 50 + config.y_step * i]
            if color_corner == config.color_corner:
                color_flag = pixels[color_flag_rel_x + config.x_step * j, color_flag_rel_y + config.y_step * i]
                if color_flag == config.color_flag:
                    table[i][j] = "X"
                else:
                    table[i][j] = "-"
            else:
                color_number = pixels[color_number_rel_x + config.x_step * j, color_number_rel_y + config.y_step * i]
                for number in config.colors:
                    if color_number == number:
                        table[i][j] = config.colors.get(color_number)
                        break
                    else:
                        table[i][j] = "?"
    return 0

def print_table(table):
    cols_len = len(table[0])
    rows_len = len(table)

    for i in range(cols_len + 2):
        print("#", end="")
    print()
    for i in range(rows_len):
        print("#",  end="")
        for j in range(cols_len):
            print(table[i][j], end="")
        print("#")
    for i in range(cols_len + 2):
        print("#", end="")
    print()

def click_random():
    i = random.randint(0, config.rows - 1) #config.row
    j = random.randint(0, config.cols - 1) #config.col
    x = config.x_0 + config.x_step * j
    y = config.y_0 + config.y_step * i
    pyautogui.click(x, y)

def click_random_fav():
    i = config.rows / 2
    j = config.cols / 2
    x = config.x_0 + config.x_step * j
    y = config.y_0 + config.y_step * i
    pyautogui.click(x, y)

def resize_table(table, x0, y0, x1, y1):
    nueva_tabla = [fila[y0:y1 + 1] for fila in table[x0:x1 + 1]]
    return nueva_tabla

def level():
    if config.level == 1:
        config.rows = 9
        config.cols = 9
        config.x_victory = 362 - config.screenshot_left
        config.x_death = 356 - config.screenshot_left
        config.click_x_smile = 362
    elif config.level == 2:
        config.rows = 16
        config.cols = 16
        config.x_victory = 446 - config.screenshot_left
        config.x_death = 440 - config.screenshot_left
        config.click_x_smile = 446
    elif config.level == 3:
        config.rows = 16
        config.cols = 30
        config.x_victory = 614 - config.screenshot_left
        config.x_death = 608 - config.screenshot_left
        config.click_x_smile = 614

def win():
    if config.level == 1:
        pyautogui.PAUSE = 0.5
        pyautogui.click(1030, 250)
        pyautogui.click(1030, 250)
        pyautogui.PAUSE = 0.3
        pyautogui.click(270, 110)
        pyautogui.click(300, 280)
        pyautogui.click(300, 360)
        pyautogui.PAUSE = 0.01
        config.level = 2
        level()
    elif config.level == 2:
        pyautogui.PAUSE = 0.5
        pyautogui.click(1030, 250)
        pyautogui.click(1030, 250)
        pyautogui.PAUSE = 0.3
        pyautogui.click(270, 110)
        pyautogui.click(300, 300)
        pyautogui.click(300, 360)
        pyautogui.PAUSE = 0.01
        config.level = 3
        level()
    elif config.level == 3:
        pyautogui.PAUSE = 0.5
        pyautogui.click(1030, 250)
        pyautogui.click(1030, 250)

def lose():
    pyautogui.PAUSE = 0.3
    pyautogui.click(270, 110)
    pyautogui.click(300, 260)
    pyautogui.click(300, 360)
    pyautogui.PAUSE = 0.01





