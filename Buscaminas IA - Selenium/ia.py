from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import config

def casillas_alrededor(row, col, rows, cols):
    vecinos = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                vecinos.append((nr, nc))
    return vecinos

def mark_mines(driver, row, col, rows, cols, tablero):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr = row + dr
            nc = col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if tablero[nr][nc] == "blank":
                    id_casilla = f"{nr+1}_{nc+1}"
                    casilla = driver.find_element(By.ID, id_casilla)
                    actions = ActionChains(driver)
                    actions.context_click(casilla).perform()
                    tablero[nr][nc] = "bombflagged"

def analize_around_square(driver, row, col, rows, cols, tablero, mines_around):
    mines = int(mines_around)
    mine_to_flag = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr = row + dr
            nc = col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if tablero[nr][nc] == "blank":
                    mines -= 1
                    mine_to_flag = 1
                if tablero[nr][nc] == "bombflagged":
                    mines -= 1
    if int(mines) == 0 and mine_to_flag:
        mark_mines(driver, row, col, rows, cols, tablero)

def analize_mines(driver, tablero, rows, cols):
    for row in range(rows):
        for col in range(cols):
            if tablero[row][col] == "blank":
                continue
            elif tablero[row][col] == "open0":
                continue
            elif tablero[row][col] == "bombflagged":
                continue
            else:
                mines_around = tablero[row][col][4:]
                if mines_around == "revealed" or mines_around == "death":
                    continue
                analize_around_square(driver, row, col, rows, cols, tablero, mines_around)

def click_no_mines(driver, row, col, rows, cols, tablero):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr = row + dr
            nc = col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if tablero[nr][nc] == "blank":
                    id_casilla = f"{nr+1}_{nc+1}"
                    casilla = driver.find_element(By.ID, id_casilla)
                    casilla.click()
                    config.clicked = True
                    nuevo_estado = driver.find_element(By.ID, id_casilla)
                    classes = nuevo_estado.get_attribute("class")
                    estado = classes.replace("square ", "")
                    tablero[nr][nc] = estado


def analize_around_square_click(driver, row, col, rows, cols, tablero, mines_around):
    mines = int(mines_around)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr = row + dr
            nc = col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if tablero[nr][nc] == "bombflagged":
                    mines -= 1
    if int(mines) < 0:
        print("You are fucked")
    if int(mines) == 0:
        click_no_mines(driver, row, col, rows, cols, tablero)


def click_squares(driver, tablero, rows, cols):
    for row in range(rows):
        for col in range(cols):
            if tablero[row][col] == "blank":
                continue
            elif tablero[row][col] == "open0":
                continue
            elif tablero[row][col] == "bombflagged":
                continue
            else:
                mines_around = tablero[row][col][4:]
                if mines_around == "revealed" or mines_around == "death":
                    continue
                analize_around_square_click(driver, row, col, rows, cols, tablero, mines_around)