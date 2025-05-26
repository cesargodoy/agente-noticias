import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Encabezados para evitar bloqueo
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "es-CL,es;q=0.9",
    "Referer": "https://www.google.com/"
}

# Scraper para DF.cl únicamente
def scrape_df():
    url = "https://www.df.cl/"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = []

    # Selector para titulares destacados
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

# Función central (solo noticias desde DF.cl)
def obtener_todas_las_noticias():
    return scrape_df()
