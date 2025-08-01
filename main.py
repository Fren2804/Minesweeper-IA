import pyautogui
import config

import functions
import ia


def play():
    functions.click_random_fav()
    while True:
        config.clicked = 0
        table = functions.init_table()
        status = functions.obtain_table(table)
        if status == 1:
            pyautogui.click(config.click_x_smile, config.click_y_smile)
            return 0
        if status == 2:
            functions.win()
            return 1
        status = ia.analize_mines(table)
        if status == 1:
            functions.win()
            return 1
        ia.click_squares(table)
        if config.clicked == 0:
            table = functions.init_table()
            functions.obtain_table(table)
            ia.obtain_cells_analize(table)

#pyautogui.PAUSE = 0.2
pyautogui.PAUSE = 0.01


level1 = 0
level2 = 0
level3 = 0



while True:
    config.level = 1
    functions.level()
    level1 = play()
    if level1 == 1:
        level2 = play()
        if level2 == 1:
            level3 = play()
            if level3 == 1:
                break
            else:
                functions.lose()
                # break
        else:
            functions.lose()
            # break
    else:
        functions.lose()
        # break




