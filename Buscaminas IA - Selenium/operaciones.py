from selenium.webdriver.common.by import By
import time
import random
import keyboard
import threading

finish_event = threading.Event()

#Hilos

def close_driver():
    while True:
        if keyboard.is_pressed("q"):
            finish_event.set()
            break
        time.sleep(0.5)

def start_thread():
    thread_keyboard = threading.Thread(target=close_driver)
    thread_keyboard.start()
    return thread_keyboard



#Estados de la partida

def check_alive(driver):
    face = driver.find_elements(By.ID, "face")
    smile_value = face[0].get_attribute("class")
    if smile_value == "facesmile":
        return 1
    elif smile_value == "facewin":
        return 2
    else:
        return 0

def restart(driver):
    face = driver.find_elements(By.ID, "face")
    face[0].click()

def finish_win(driver):
    print("\nCongratulations! You have won!")
    time.sleep(10)
    driver.quit()

def finish(driver):
    print("\nForce exit.")
    driver.quit()



def random_click(driver, rows, cols):
    row = random.randint(0, rows - 1)
    col = random.randint(0, cols - 1)
    id_square = f"{row + 1}_{col + 1}"
    try:
        square = driver.find_element(By.ID, id_square)
        square.click()
    except Exception as e:
        print(f"No se pudo hacer clic en la casilla {id_square}: {e}")
