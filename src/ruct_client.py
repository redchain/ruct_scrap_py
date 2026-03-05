import re
import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RuctClient:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.educacion.gob.es/ruct/consultaestudios?actual=estudios"
        self.wait = WebDriverWait(self.driver, 10)

    def obtener_variantes(self, codigo_ruct):
        self.driver.get(self.url)

        input_codigo = self.wait.until(
            EC.presence_of_element_located((By.ID, "codigoEstudio"))
        )
        input_codigo.clear()
        input_codigo.send_keys(str(codigo_ruct))

        boton = self.driver.find_element(By.NAME, "action:listaestudios")
        boton.click()

        filas = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table#estudio tbody tr"))
        )

        variantes = []
        for fila in filas:
            enlace = fila.find_element(By.CSS_SELECTOR, "a[href*='CodigoEstudio']")
            url = enlace.get_attribute("href")
            variante = url.split("codigoCiclo=")[1].split("&")[0]
            variantes.append((variante, url))

        return variantes

    def limpiar(self, raw):
        if raw is None:
            return ""
        sin_tags = re.sub(r"<.*?>", "", raw)
        return html.unescape(sin_tags).strip()

    def extraer_centros(self):
        tabla = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table#centro"))
        )

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

            centros.append(f"{universidad} | {codigo} | {nombre}")

        return centros
