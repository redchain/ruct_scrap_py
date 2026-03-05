from src.scraper import RuctScraper

def main():
    input_excel = "data/codigos.xlsx"

    scraper = RuctScraper(input_excel)
    scraper.procesar()


if __name__ == "__main__":
    main()
