import pyautogui

import config

def mark_mines(table, row, col):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr = row + dr
            nc = col + dc
            if 0 <= nr < config.rows and 0 <= nc < config.cols:
                if table[nr][nc] == "-":
                    table[nr][nc] = "X"

def analize_around_square(table, mines_around, row, col):
    mines = int(mines_around)
    marked_mines_around = 0
    mine_to_flag = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr = row + dr
            nc = col + dc
            if 0 <= nr < config.rows and 0 <= nc < config.cols:
                if table[nr][nc] == "-":
                    mines -= 1
                    mine_to_flag += 1
                if table[nr][nc] == "X":
                    marked_mines_around += 1
                    mines -= 1
    if marked_mines_around > int(mines_around) or int(mines_around) > mine_to_flag + marked_mines_around:
        # print("You are fucked 1")
        # print(mines)
        # print()
        config.marked_odds = -1
    if int(mines) == 0 and mine_to_flag:
        mark_mines(table, row, col)
        if config.marked_odds != -1:
            config.marked_odds = 1

def analize_mines(table):
    for row in range(config.rows):
        for col in range(config.cols):
            if table[row][col] == "-":
                continue
            elif table[row][col] == "0":
                continue
            elif table[row][col] == "X":
                continue
            elif table[row][col] == "?":
                continue
            else:
                mines_around = table[row][col]
                analize_around_square(table, mines_around, row, col)


def click_no_mines(table, row, col):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr = row + dr
            nc = col + dc
            if 0 <= nr < config.rows and 0 <= nc < config.cols:
                if table[nr][nc] == "-":
                    table[nr][nc] = "?"
                    if config.clicked_odds != -1:
                        config.clicked_odds = 1

def analize_around_square_click(table, mines_around, row, col):
    mines = int(mines_around)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr = row + dr
            nc = col + dc
            if 0 <= nr < config.rows and 0 <= nc < config.cols:
                if table[nr][nc] == "X":
                    mines -= 1
    if int(mines) < 0:
        # print("You are fucked 2")
        config.clicked_odds = -1
    if int(mines) == 0:
        click_no_mines(table, row, col)

def click_squares(table):
    for row in range(config.rows):
        for col in range(config.cols):
            if table[row][col] == "-":
                continue
            elif table[row][col] == "0":
                continue
            elif table[row][col] == "X":
                continue
            elif table[row][col] == "?":
                continue
            else:
                mines_around = table[row][col]
                analize_around_square_click(table, mines_around, row, col)

def check_results(table, cells_status, x, y):
    mines = 0
    save = 0
    idk = 0
    for (x1, y1), cells in cells_status.items():
        if table[x1][y1] == "X":
            cells['check'] = True
            mines += 1
        if table[x1][y1] == "?":
            save += 1
        if table[x1][y1] == "-":
            idk += 1
    if idk == 0:
        cells_status[(x, y)]["value"] = 1
    cells_status[(x, y)]["mines"] = mines
    cells_status[(x, y)]["save"] = save
    cells_status[(x, y)]["idk"] = idk
    return cells_status
