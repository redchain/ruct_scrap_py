import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import html

class RuctClient:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.educacion.gob.es/ruct/consultaestudios?actual=estudios"
        self.wait = WebDriverWait(self.driver, 10)

    def buscar_titulo(self, codigo_ruct):
        print(f"[RUCT] Buscando código {codigo_ruct}")
        self.driver.get(self.url)

        try:
            input_codigo = self.wait.until(
                EC.presence_of_element_located((By.ID, "codigoEstudio"))
            )
        except Exception as e:
            print(f"[RUCT] No se encontró el campo 'codigoEstudio': {e}")
            return False

        input_codigo.clear()
        input_codigo.send_keys(str(codigo_ruct))

        try:
            boton = self.driver.find_element(By.NAME, "action:listaestudios")
            boton.click()
        except Exception as e:
            print(f"[RUCT] No se pudo pulsar el botón Consultar: {e}")
            return False

        time.sleep(1)

        enlaces = self.driver.find_elements(
            By.CSS_SELECTOR,
            "table#estudio a[href*='CodigoEstudio']"
        )

        if not enlaces:
            print(f"[RUCT] No se encontró enlace para {codigo_ruct}")
            return False

        print(f"[RUCT] Entrando en ficha del título {codigo_ruct}")
        enlaces[0].click()
        time.sleep(1)
        return True

    def limpiar(self, raw):
        if raw is None:
            return ""
        sin_tags = re.sub(r"<.*?>", "", raw)
        return html.unescape(sin_tags).strip()

    def extraer_centros(self):
        print("[RUCT] Extrayendo centros...")

        try:
            tabla = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table#centro"))
            )
        except Exception as e:
            print(f"[RUCT] No se encontró la tabla de centros: {e}")
            return []

        filas = tabla.find_elements(By.CSS_SELECTOR, "tbody tr")
        

        centros = []

        for fila in filas:
            columnas = fila.find_elements(By.TAG_NAME, "td")

            uni_raw = columnas[0].get_attribute("innerHTML")
            cod_raw = columnas[1].get_attribute("innerHTML")
            cen_raw = columnas[2].get_attribute("innerHTML")

            universidad = self.limpiar(uni_raw)
            codigo = self.limpiar(cod_raw)
            nombre = self.limpiar(cen_raw)

            print("DEBUG:", universidad, "|", codigo, "|", nombre)

            centros.append(f"{universidad} | {codigo} | {nombre}")

        
        return centros
    
    def obtener_variantes(self, codigo_ruct):
        print(f"[RUCT] Buscando variantes para {codigo_ruct}")
        self.driver.get(self.url)

        input_codigo = self.wait.until(
            EC.presence_of_element_located((By.ID, "codigoEstudio"))
        )
        input_codigo.clear()
        input_codigo.send_keys(str(codigo_ruct))

        boton = self.driver.find_element(By.NAME, "action:listaestudios")
        boton.click()
        time.sleep(1)

        filas = self.driver.find_elements(By.CSS_SELECTOR, "table#estudio tbody tr")

        variantes = []
        for fila in filas:
            enlace = fila.find_element(By.CSS_SELECTOR, "a[href*='CodigoEstudio']")
            url = enlace.get_attribute("href")

            # Extraer la variante del href (ej: codigoCiclo=SCL)
            href = url
            variante = href.split("codigoCiclo=")[1].split("&")[0]

            variantes.append((variante, url))

        print(f"[RUCT] Variantes encontradas: {variantes}")
        return variantes

