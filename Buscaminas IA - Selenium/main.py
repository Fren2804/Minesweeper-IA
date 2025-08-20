from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import obtener_tablero
import operaciones
import ia
import config



# Dificultad 0 Beginner 1 Intermediate 2 Expert
dificultad = 1

service = Service("C:\\Users\\franc\\PyCharmMiscProject\\Buscaminas IA - Selenium\\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Configuración
if dificultad == 0:
    rows = 9
    cols = 9
    driver.get("https://minesweeperonline.com/#beginner")
elif dificultad == 1:
    rows = 16
    cols = 16
    driver.get("https://minesweeperonline.com/#intermediate")
else:
    rows = 16
    cols = 30
    driver.get("https://minesweeperonline.com/#expert")

#thread_keyboard = operaciones.start_thread()

time.sleep(4)
operaciones.random_click(driver, rows, cols)
#while not operaciones.finish_event.is_set():
while True:
    tablero = obtener_tablero.refrescar(driver, rows, cols)
    ia.analize_mines(driver, tablero, rows, cols)
    ia.click_squares(driver, tablero, rows, cols)
    match_status = operaciones.check_alive(driver)
    if not config.clicked:
        operaciones.random_click(driver, rows, cols)
    if match_status == 2:
        operaciones.finish_win(driver)
        #thread_keyboard.join()
        break
    elif match_status == 0:
        print("\nYou lose")
        operaciones.restart(driver)
    config.clicked = False
time.sleep(4)
operaciones.finish(driver)
#thread_keyboard.join()