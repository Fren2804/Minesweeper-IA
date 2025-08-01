import pyautogui

import config
import functions
import odds

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
                    x = config.x_0 + config.x_step * nc
                    y = config.y_0 + config.y_step * nr
                    pyautogui.rightClick(x, y)


def analize_around_square(table, mines_around, row, col):
    mines = int(mines_around)
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
                    mine_to_flag = 1
                if table[nr][nc] == "X":
                    mines -= 1
    if int(mines) == 0 and mine_to_flag:
        mark_mines(table, row, col)

def analize_mines(table):
    # print(f"{len(table)} {len(table[0])}")
    for row in range(config.rows):
        for col in range(config.cols):
            if table[row][col] == "-":
                continue
            elif table[row][col] == "0":
                continue
            elif table[row][col] == "X":
                continue
            elif table[row][col] == "?":
                return 1
            else:
                mines_around = table[row][col]
                analize_around_square(table, mines_around, row, col)
    return 0







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
                    x = config.x_0 + config.x_step * nc
                    y = config.y_0 + config.y_step * nr
                    pyautogui.click(x, y)
                    config.clicked = True
                    config.clicked = 1

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
    # if int(mines) < 0:
    #     print("You are fucked")
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
                return 1
            else:
                mines_around = table[row][col]
                analize_around_square_click(table, mines_around, row, col)
    return 0




#Dir 1 hacia arriba, 2 hacia izquierda, 3 hacia abajo, 4 hacia derecha

def analize_around_square_outline(table, row, col):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr = row + dr
            nc = col + dc
            if 0 <= nr < config.rows and 0 <= nc < config.cols:
                if table[nr][nc] != "-" and table[nr][nc] != "X":
                    return True
    return False

def check_ways(table, row, col, ways):
    row_max = config.rows - 1
    col_max = config.cols - 1
    if row != 0:
        if table[row - 1][col] == "-":
            if analize_around_square_outline(table, row - 1, col):
                ways[0] += 1
                ways[1] = True
    if col != 0:
        if table[row][col - 1] == "-":
            if analize_around_square_outline(table, row, col - 1):
                ways[0] += 1
                ways[2] = True
    if row != row_max:
        if table[row + 1][col] == "-":
            if analize_around_square_outline(table, row + 1, col):
                ways[0] += 1
                ways[3] = True
    if col != col_max:
        if table[row][col + 1] == "-":
            if analize_around_square_outline(table, row, col + 1):
                ways[0] += 1
                ways[4] = True
    return ways


#Dir 1 arriba->abajo, 2 izquierda->derecha, 3 abajo->arriba, 4 derecha->izquierda
def outline(table, row, col, outline_cells, dir):
    row_max = config.rows - 1
    col_max = config.cols - 1
    # 1 arriba way?, 2 izquierda way?, 3 abajo way?, 4 derecha way?
    ways = [
        0,
        False,
        False,
        False,
        False,
    ]
    ways = check_ways(table, row, col, ways)
    if ways[1] and row > 0:
        new_row = row - 1
        if not (new_row, col) in outline_cells and dir != 1:
            outline_cells.add((new_row, col))
            outline_cells = outline(table, new_row, col, outline_cells, 3)
    if ways[2] and col > 0:
        new_col = col - 1
        if not (row, new_col) in outline_cells and dir != 2:
            outline_cells.add((row, new_col))
            outline_cells = outline(table, row, new_col, outline_cells, 4)
    if ways[3] and row < row_max:
        new_row = row + 1
        if not (new_row, col) in outline_cells and dir != 3:
            outline_cells.add((new_row, col))
            outline_cells = outline(table, new_row, col, outline_cells, 1)
    if ways[4] and col < col_max:
        new_col = col + 1
        if not (row, new_col) in outline_cells and dir != 4:
            outline_cells.add((row, new_col))
            outline_cells = outline(table, row, new_col, outline_cells, 2)
    return outline_cells


def analize_odds(table, outline_cells):
    cells_status = {coord: {"check": False, "value": 0, "save": 0, "mines": 0, "idk": 0} for coord in sorted(outline_cells)}
    for (x, y), cells in cells_status.items():
        if not cells["check"]:
            cells["check"] = True
            aux_table = [fila[:] for fila in table]
            aux_table[x][y] = "X"
            # functions.print_table(aux_table)
            while True:
                config.marked_odds = 0
                odds.analize_mines(aux_table)
                if config.marked_odds == -1:
                    cells["value"] = -1
                    break
                config.clicked_odds = 0
                odds.click_squares(aux_table)
                if config.marked_odds == -1:
                    cells["value"] = -1
                    break
                if config.marked_odds == 0 and config.clicked_odds == 0:
                    break
            if cells["value"] != -1:
                cells_status = odds.check_results(aux_table, cells_status, x, y)
    # for (x, y), datos in cells_status.items():
    #     print(f"x = {x}, y = {y}, check = {datos['check']}, value = {datos['value']}, save = {datos['save']}, mines = {datos['mines']}, idk = {datos['idk']}")
    return cells_status

def click_odds(table, cells_status):
    for (x1, y1), cells in cells_status.items():
        if cells["value"] == -1:
            # print(x1, y1)
            x = config.x_0 + config.x_step * y1
            y = config.y_0 + config.y_step * x1
            pyautogui.click(x, y)
            return
    for (x1, y1), cells in cells_status.items():
        if cells["value"] == 1:
            x = config.x_0 + config.x_step * y1
            y = config.y_0 + config.y_step * x1
            pyautogui.rightClick(x, y)
            return
    mines = 0
    for (x1, y1), cells in cells_status.items():
        if cells["mines"] >= mines:
            mines = cells["mines"]
    for (x1, y1), cells in cells_status.items():
        if cells["mines"] == mines:
            x = config.x_0 + config.x_step * y1
            y = config.y_0 + config.y_step * x1
            pyautogui.click(x, y)
            return

def search_blank(table):
    for col in range(config.cols):
        for row in range(config.rows):
            if table[row][col] == "-":
                x = config.x_0 + config.x_step * col
                y = config.y_0 + config.y_step * row
                pyautogui.click(x, y)

def obtain_cells_analize(table):
    row0 = 0
    col0 = 0
    outline_cells = set()
    found_table = False
    for row in range(config.rows):
        found_blank = False
        found_no_blank = False
        for col in range(config.cols):
            if table[row][col] == "-":
                found_blank = True
            if table[row][col] != "-" and table[row][col] != "X":
                found_no_blank = True
            if table[row][col] == "X":
                found_blank = False
                found_no_blank = False
            if found_blank and found_no_blank:
                col0 = col
                row0 = row
                found_table = True
                break
        if found_table:
            if table[row0][col0] != "-":
                col0 -= 1
            break
    if table[row0][col0] != "-":
        for col in range(config.cols):
            found_blank = False
            found_no_blank = False
            for row in range(config.rows):
                if table[row][col] == "-":
                    found_blank = True
                if table[row][col] != "-" and table[row][col] != "X":
                    found_no_blank = True
                if table[row][col] == "X":
                    found_blank = False
                    found_no_blank = False
                if found_blank and found_no_blank:
                    row0 = row
                    col0 = col
                    found_table = True
                    break
            if found_table:
                if table[row0][col0] != "-":
                    row0 -= 1
                break
    if table[row0][col0] != "-":
        search_blank(table)
        return 0
    outline_cells.add((row0, col0))
    outline_cells = outline(table, row0, col0, outline_cells, 2)
    cells_status = analize_odds(table, outline_cells)
    click_odds(table, cells_status)
    return 0




