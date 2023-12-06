from ScraperClass import Scraper
import pandas as pd

# Uso de la clase
url = 'https://www.bbc.com/mundo/topics/c082p5d151nt'
scraper = Scraper(url)
news_links = scraper.run(18)


df = pd.read_csv("datos_noticias.csv", sep=",")
print(df)