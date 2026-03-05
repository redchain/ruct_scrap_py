from src.scraper import RuctScraper

def main():
    input_excel = "data/libro.xlsx"

    scraper = RuctScraper(input_excel)
    scraper.procesar()

    print("Proceso completado.")

if __name__ == "__main__":
    main()
