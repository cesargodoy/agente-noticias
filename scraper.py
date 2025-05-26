import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Encabezados para simular un navegador real (evita bloqueos en Render)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "es-CL,es;q=0.9",
    "Referer": "https://www.google.com/"
}

# 📰 Scraper para Emol
def scrape_emol():
    url = "https://www.emol.com/"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = []

    # Selector actualizado para titulares principales de Emol
    for bloque in soup.select(".cont_headline h3 a")[:5]:
        titulo = bloque.get_text(strip=True)
        bajada = ""  # Emol no tiene bajada directa visible
        noticias.append({
            "medio": "emol",
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "titular": titulo,
            "bajada": bajada
        })

    return noticias

# 💼 Scraper para DF.cl
def scrape_df():
    url = "https://www.df.cl/"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = []

    # Selector para noticias destacadas en DF
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

# 🧩 Función central que combina noticias de ambos medios
def obtener_todas_las_noticias():
    return scrape_emol() + scrape_df()
