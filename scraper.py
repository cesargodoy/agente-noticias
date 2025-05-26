import requests
from datetime import datetime

def scrape_df_api():
    url = "https://www.df.cl/data/frontpage.json"
    response = requests.get(url)
    noticias = []

    if response.status_code == 200:
        try:
            data = response.json()
            print(f"🔍 JSON cargado correctamente. Total items en data: {len(data)}")  # log de verificación

            fecha = datetime.now().strftime("%Y-%m-%d")

            for i, item in enumerate(data[:5]):  # puedes quitar el [:5] para traer más
                titulo = item.get("title", "Sin título")
                bajada = item.get("excerpt", "")
                print(f"📌 Noticia {i+1}: {titulo}")  # muestra cada titular

                noticias.append({
                    "medio": "df",
                    "fecha": fecha,
                    "titular": titulo.strip(),
                    "bajada": bajada.strip()
                })

        except Exception as e:
            print(f"❌ Error al parsear JSON: {e}")
    else:
        print(f"❌ Error HTTP: {response.status_code}")

    return noticias

def obtener_todas_las_noticias():
    return scrape_df_api()
