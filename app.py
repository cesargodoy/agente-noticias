from flask import Flask, jsonify, request
import requests
import os
from bs4 import BeautifulSoup
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": "https://03.cl"}})

client = OpenAI()

def scrape_text_and_metadata(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return None, f'Error al acceder a la URL (código {response.status_code})', None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer metadatos del head
        head = soup.head
        metadata = {
            'title': head.title.string.strip() if head and head.title else None,
            'description': None,
            'canonical': None,
            'alt_tags': [],
            'title_attributes': [],
            'links': [],
            'broken_links': []
        }

        desc_tag = head.find('meta', attrs={'name': 'description'})
        if desc_tag and desc_tag.get('content'):
            metadata['description'] = desc_tag['content']

        canonical_tag = head.find('link', attrs={'rel': 'canonical'})
        if canonical_tag and canonical_tag.get('href'):
            metadata['canonical'] = canonical_tag['href']

        # Buscar alt en imágenes y title en cualquier tag
        for img in soup.find_all('img'):
            if img.get('alt'):
                metadata['alt_tags'].append(img['alt'])

        for tag in soup.find_all(attrs={'title': True}):
            metadata['title_attributes'].append(tag['title'])

        # Capturar enlaces
        links = soup.find_all('a', href=True)
        for a in links:
            href = a['href']
            metadata['links'].append(href)
            # Validar enlaces HTTP/HTTPS
            if href.startswith('http'):
                try:
                    res = requests.head(href, timeout=5)
                    if res.status_code >= 400:
                        metadata['broken_links'].append(href)
                except Exception:
                    metadata['broken_links'].append(href)

        # Limpiar contenido
        for tag in soup(['script', 'style', 'video', 'audio', 'svg', 'form', 'input', 'textarea', 'button', 'select', 'label']):
            tag.decompose()

        for tag in soup.find_all(True):
            if tag.name != 'a':
                tag.attrs = {}

        body = soup.body
        full_text = ''
        if head:
            full_text += head.get_text(separator="\n", strip=True) + "\n"
        if body:
            full_text += body.get_text(separator="\n", strip=True)

        return full_text.strip(), None, metadata

    except Exception as e:
        return None, str(e), None

def ask_gpt(prompt, content):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ],
            temperature=0.7,
            max_tokens=900
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def summarize_and_analyze():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Falta la URL'}), 400

    text, error, metadata = scrape_text_and_metadata(url)
    if error:
        return jsonify({'error': error}), 500

    summary = ask_gpt("Resumí claramente el siguiente texto en español.", text)

    seo_prompt = (
        "Evalúa el siguiente contenido web en términos de SEO usando estos criterios:\n\n"
        "1. Calidad del contenido (relevancia, originalidad, legibilidad, precisión, autoridad, atractivo)\n"
        "2. Estructura (títulos, párrafos, listas, sintaxis)\n"
        "3. Keywords (relevancia, uso adecuado)\n"
        "4. Enlaces (internos, externos, texto anclaje)\n"
        "5. Experiencia de usuario (accesibilidad, uso de alt en imágenes)\n\n"
        "Entrega un informe estructurado en español."
    )
    seo_report = ask_gpt(seo_prompt, text)

    suggestions_prompt = (
        "Basado en el contenido web y en un análisis SEO previo, sugiere mejoras claras, prácticas y específicas "
        "para optimizar esta página web en términos de SEO. Usa viñetas o numeración. Escribe en español."
    )
    suggestions = ask_gpt(suggestions_prompt, text)

    return jsonify({
        'summary': summary,
        'seo_report': seo_report,
        'suggestions': suggestions,
        'metadata_info': metadata
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
