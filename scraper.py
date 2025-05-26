import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

def scrape_df_rss():
    url = "https://www.df.cl/rss"
    response = requests.get(url)
    response.encoding = 'utf-8'

    noticias = []
    tree = ET.fromstring(response.text)

    for item in tree.findall(".//item")[:5]:  # Solo los primeros 5 titulares
        titulo = item.find("title").text if item.find("title") is not None else "Sin título"
        bajada = item.find("description").text if item.find("description") is not None else ""
        fecha = datetime.now().strftime("%Y-%m-%d")

        noticias.append({
            "medio": "df",
            "fecha": fecha,
            "titular": titulo.strip(),
            "bajada": BeautifulSoup(bajada, "html.parser").get_text().strip()
        })

    return noticias

def obtener_todas_las_noticias():
    return scrape_df_rss()
