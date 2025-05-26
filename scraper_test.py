import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "es-CL,es;q=0.9",
    "Referer": "https://www.google.com/"
}

def test_scrape_df_html():
    url = "https://www.df.cl/"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ Error al obtener HTML: {response.status_code}")
        return

    html = response.text

    # Guarda una copia del HTML para inspección
    with open("df_raw.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ HTML guardado como df_raw.html (primeros 1000 caracteres):\n")
    print(html[:1000])

    soup = BeautifulSoup(html, "html.parser")

    # Intentamos encontrar bloques de noticias visibles sin JS
    blocks = soup.select("article.highlight__news, .news-card, h3 a")

    print(f"\n🔍 Total de posibles noticias detectadas: {len(blocks)}\n")

    for i, b in enumerate(blocks[:5]):
        print(f"{i+1}) {b.get_text(strip=True)}")

if __name__ == "__main__":
    test_scrape_df_html()
