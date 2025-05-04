import requests
from bs4 import BeautifulSoup

def extract_seo_data(url):
    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.text, 'html.parser')

    title = soup.title.string if soup.title else ''
    description = soup.find('meta', attrs={'name': 'description'})
    meta_desc = description['content'] if description else ''
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
