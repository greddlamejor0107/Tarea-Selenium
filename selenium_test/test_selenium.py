from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time, os

def screenshot(driver, step):
    path = f"screenshots/{step}.png"
    driver.save_screenshot(path)
    return path

steps_results = []

def log_step(driver, step, success, description):
    img = screenshot(driver, step)
    steps_results.append((step, success, description, img))

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

try:
    driver.get("http://127.0.0.1:5000/")
    time.sleep(1)
    log_step(driver, "inicio", True, "Página de inicio cargada")

    # Registro
    driver.find_element(By.LINK_TEXT, "Registrarse").click()
    time.sleep(1)
    driver.find_element(By.NAME, "usuario").send_keys("prueba1")
    driver.find_element(By.NAME, "contraseña").send_keys("1234")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    log_step(driver, "registro", True, "Registro completado")

    # Login
    driver.find_element(By.NAME, "usuario").send_keys("prueba1")
    driver.find_element(By.NAME, "contraseña").send_keys("1234")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    log_step(driver, "login", True, "Inicio de sesión exitoso")

    # Agregar productos
    links = driver.find_elements(By.PARTIAL_LINK_TEXT, "Agregar al carrito")
    if links:
        links[0].click()
        time.sleep(1)
        log_step(driver, "agregar_carrito", True, "Producto agregado al carrito")
    
    # Eliminar producto
    driver.find_element(By.LINK_TEXT, "Eliminar").click()
    time.sleep(1)
    log_step(driver, "eliminar_carrito", True, "Producto eliminado del carrito")

except Exception as e:
    log_step(driver, "error", False, str(e))

finally:
    driver.quit()

# Crear reporte HTML
with open("reporte.html", "w", encoding="utf-8") as f:
    f.write("<html><head><title>Reporte Selenium</title></head><body><h1>Resultados de Prueba</h1><ul>")
    for step, success, desc, img in steps_results:
        color = "green" if success else "red"
        f.write(f"<li><b>{step}</b>: <span style='color:{color}'>{desc}</span><br><img src='{img}' width='300'></li><br>")
    f.write("</ul></body></html>")
