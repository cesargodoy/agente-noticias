import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "es-CL,es;q=0.9",
    "Referer": "https://www.google.com/"
}

def scrape_df_sitemap(limit=5):
    sitemap_url = "https://www.df.cl/noticias/site/list/port/sitemap_df.xml"
    response = requests.get(sitemap_url, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ Error al obtener el sitemap: {response.status_code}")
        return []

    noticias = []
    root = ET.fromstring(response.content)
    urls = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url")

    for i, url_tag in enumerate(urls[:limit]):
        loc = url_tag.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
        fecha = url_tag.find("{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod").text
        print(f"🔗 Scrapeando noticia {i+1}: {loc}")

        try:
            noticia = scrape_noticia(loc, fecha)
            noticias.append(noticia)
        except Exception as e:
            print(f"⚠️ Error al procesar noticia: {e}")

    return noticias

def scrape_noticia(url, fecha_iso):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    titular = soup.find("h1").get_text(strip=True) if soup.find("h1") else "Sin título"
    
    # Intentamos obtener bajada desde <meta name="description"> o <h2>
    meta_desc = soup.find("meta", attrs={"name": "description"})
    bajada = meta_desc["content"].strip() if meta_desc else ""

    if not bajada:
        h2 = soup.find("h2")
        bajada = h2.get_text(strip=True) if h2 else ""

    fecha = fecha_iso.split("T")[0]  # solo dejamos la parte de la fecha

    return {
        "medio": "df",
        "fecha": fecha,
        "titular": titular,
        "bajada": bajada,
        "url": url
    }

def obtener_todas_las_noticias():
    return scrape_df_sitemap(limit=5)
