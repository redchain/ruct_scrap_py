import pandas as pd
import time
from selenium import webdriver
from src.ruct_client import RuctClient


class RuctScraper:
    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.df = pd.read_excel(excel_path)

        self.driver = webdriver.Chrome()
        self.client = RuctClient(self.driver)

    def procesar(self):
        filas_salida = []

        for i, row in self.df.iterrows():
            codigo = row["Código RUCT"]
            print(f"Procesando {codigo}...")

            variantes = self.client.obtener_variantes(codigo)

            for variante, url in variantes:
                self.driver.get(url)
                time.sleep(1)

                centros = self.client.extraer_centros()

                for centro in centros:
                    universidad, cod_centro, nombre = [c.strip() for c in centro.split("|")]

                    filas_salida.append({
                        "Código RUCT": codigo,
                        "Variante": variante,
                        "Universidad": universidad,
                        "Código Centro": cod_centro,
                        "Nombre Centro": nombre
                    })

        df_final = pd.DataFrame(filas_salida)
        
        df_final.to_excel("data/salida_centros.xlsx", index=False)
        

        self.driver.quit()
        print("Proceso completado. scaper.py")

