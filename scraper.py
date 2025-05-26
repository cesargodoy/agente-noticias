import requests
from datetime import datetime

def scrape_df_api():
    url = "https://www.df.cl/data/frontpage.json"
    response = requests.get(url)
    noticias = []

    if response.status_code == 200:
        data = response.json()
        fecha = datetime.now().strftime("%Y-%m-%d")

        for item in data[:5]:  # Solo las primeras 5 noticias
            titulo = item.get("title", "Sin título")
            bajada = item.get("excerpt", "")
            noticias.append({
                "medio": "df",
                "fecha": fecha,
                "titular": titulo.strip(),
                "bajada": bajada.strip()
            })

    return noticias

def obtener_todas_las_noticias():
    return scrape_df_api()
