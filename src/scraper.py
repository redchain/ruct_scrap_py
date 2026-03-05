import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.ruct_client import RuctClient


class RuctScraper:
    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.df = pd.read_excel(excel_path)

        # Chrome optimizado
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)
        self.client = RuctClient(self.driver)

    def procesar(self):
        filas_salida = []

        for _, row in self.df.iterrows():
            codigo = row["Código RUCT"]

            variantes = self.client.obtener_variantes(codigo)

            for variante, url in variantes:
                self.driver.get(url)

                centros = self.client.extraer_centros()

                for centro in centros:
                    partes = [c.strip() for c in centro.split("|")]

                    if len(partes) < 3:
                        continue

                    universidad = partes[0]
                    cod_centro = partes[1]
                    nombre = " | ".join(partes[2:])

                    filas_salida.append({
                        "Código RUCT": codigo,
                        "Variante": variante,
                        "Universidad": universidad,
                        "Código Centro": cod_centro,
                        "Nombre Centro": nombre
                    })

        df_final = pd.DataFrame(filas_salida)

        output_path = "data/salida_centros.xlsx"
        df_final.to_excel(output_path, index=False)

        self.driver.quit()
        print(f"Excel generado en: {os.path.abspath(output_path)}")
