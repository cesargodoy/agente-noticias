import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "es-CL,es;q=0.9",
    "Referer": "https://www.google.com/"
}

def test_scrape_df():
    url = "https://www.df.cl/"
    response = requests.get(url, headers=HEADERS)
    html = response.text

    print("▶ HTML recibido (primeros 1000 caracteres):\n")
    print(html[:1000])
    print("\n✅ Longitud total del HTML:", len(html))

    soup = BeautifulSoup(html, "html.parser")
    noticias = soup.select("article.highlight__news")

    print("\n📰 Total de elementos encontrados con 'article.highlight__news':", len(noticias))

    for i, item in enumerate(noticias[:3]):
        titulo_tag = item.select_one(".highlight__title")
        print(f"\n{i+1}) Título:", titulo_tag.get_text(strip=True) if titulo_tag else "No encontrado")

if __name__ == "__main__":
    test_scrape_df()
