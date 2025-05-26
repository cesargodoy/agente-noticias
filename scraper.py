import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Scraper para Emol
def scrape_emol():
    url = "https://www.emol.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = []

    # Emol: Selector de titulares principales
    for bloque in soup.select(".titulares .headline")[:5]:
        titulo = bloque.get_text(strip=True)
        bajada_tag = bloque.find_next("p")
        bajada = bajada_tag.get_text(strip=True) if bajada_tag else ""
        noticias.append({
            "medio": "emol",
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "titular": titulo,
            "bajada": bajada
        })

    return noticias

# Scraper para Diario Financiero (DF.cl)
def scrape_df():
    url = "https://www.df.cl/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = []

    # DF.cl: artículos destacados con clase 'highlight__news'
    for item in soup.select("article.highlight__news")[:5]:
        titulo_tag = item.select_one(".highlight__title")
        bajada_tag = item.select_one(".highlight__excerpt")

        titulo = titulo_tag.get_text(strip=True) if titulo_tag else "Sin título"
        bajada = bajada_tag.get_text(strip=True) if bajada_tag else ""

        noticias.append({
            "medio": "df",
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "titular": titulo,
            "bajada": bajada
        })

    return noticias

# Función central que devuelve todas las noticias unificadas
def obtener_todas_las_noticias():
    noticias_emol = scrape_emol()
    noticias_df = scrape_df()
    return noticias_emol + noticias_df
