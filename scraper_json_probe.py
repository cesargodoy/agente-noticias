import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "es-CL,es;q=0.9",
    "Referer": "https://www.google.com/"
}

def analizar_html_df():
    url = "https://www.df.cl/"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ Error HTTP: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Guardamos HTML completo para analizar si es necesario luego
    with open("df_raw_full.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"✅ HTML guardado como df_raw_full.html")
    print("🔎 Buscando scripts con JSON sospechoso...\n")

    scripts = soup.find_all("script")

    encontrados = 0

    for i, script in enumerate(scripts):
        if script.string:
            contenido = script.string.strip()
            if re.search(r'"title"\s*:', contenido) or re.search(r'"slug"\s*:', contenido):
                print(f"\n🎯 Posible bloque JSON en <script> #{i} (primeros 500 caracteres):\n")
                print(contenido[:500])
                encontrados += 1

    if encontrados == 0:
        print("⚠️ No se encontraron bloques JSON útiles en <script>")

    print("\n🔍 Explorando elementos <h3> visibles con texto largo...\n")
    h3s = soup.find_all("h3")
    for i, h3 in enumerate(h3s[:10]):
        text = h3.get_text(strip=True)
        if len(text) > 30:
            print(f"📰 H3 #{i+1}: {text}")

if __name__ == "__main__":
    analizar_html_df()
