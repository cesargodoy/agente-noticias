import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_emol():
    url = "https://www.emol.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = []

    # Extrae las noticias principales
    for noticia in soup.select('.headline')[:5]:  # Ajusta el selector si cambia Emol
        titulo = noticia.get_text(strip=True)
        bajada_tag = noticia.find_next('p')
        bajada = bajada_tag.get_text(strip=True) if bajada_tag else ""
        noticias.append({
            "medio": "emol",
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "titular": titulo,
            "bajada": bajada
        })

    return noticias


def scrape_df():
    url = "https://www.df.cl/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = []

    for item in soup.select(".highlight__title")[:5]:  # Selector para titulares de portada
        titulo = item.get_text(strip=True)
        bajada_tag = item.find_next("p")
        bajada = bajada_tag.get_text(strip=True) if bajada_tag else ""
        noticias.append({
            "medio": "df",
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "titular": titulo,
            "bajada": bajada
        })

    return noticias


def obtener_todas_las_noticias():
    return scrape_emol() + scrape_df()

