from selenium.webdriver.common.by import By

def refrescar(driver, rows, cols):
    squares = driver.find_elements(By.CLASS_NAME, "square")

    tablero = [["" for _ in range(cols)] for _ in range(rows)]

    for square in squares:
        id_casilla = square.get_attribute("id")
        classes = square.get_attribute("class")

        if id_casilla and "_" in id_casilla:
            fila_str, columna_str = id_casilla.split("_")

            if fila_str.isdigit() and columna_str.isdigit():
                fila = int(fila_str) - 1
                columna = int(columna_str) - 1

                if 0 <= fila < rows and 0 <= columna < cols:
                    estado = classes.replace("square ", "")
                    tablero[fila][columna] = estado
    return tablero