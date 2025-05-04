import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}

def extract_seo_data(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
    except requests.RequestException as e:
        return {
            'title': '',
            'meta_description': '',
            'headers': {},
            'word_count': 0,
            'text_sample': f'Error al acceder a la URL: {str(e)}'
        }

    soup = BeautifulSoup(res.text, 'html.parser')

    title = soup.title.string.strip() if soup.title else ''
    description = soup.find('meta', attrs={'name': 'description'})
    meta_desc = description['content'].strip() if description and 'content' in description.attrs else ''

    headers = {
        'h1': [h.get_text(strip=True) for h in soup.find_all('h1')],
        'h2': [h.get_text(strip=True) for h in soup.find_all('h2')],
        'h3': [h.get_text(strip=True) for h in soup.find_all('h3')]
    }

    text_content = soup.get_text(separator=' ', strip=True)
    word_count = len(text_content.split())

    return {
        'title': title,
        'meta_description': meta_desc,
        'headers': headers,
        'word_count': word_count,
        'text_sample': text_content[:2000]
    }
