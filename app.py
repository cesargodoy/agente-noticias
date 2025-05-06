from flask import Flask, jsonify, request
import requests
import os
from bs4 import BeautifulSoup
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": "https://03.cl"}})

client = OpenAI()

def scrape_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return None, f'Error al acceder a la URL (código {response.status_code})'

        soup = BeautifulSoup(response.text, 'html.parser')

        # Eliminar contenido no textual
        for tag in soup(['script', 'style', 'img', 'video', 'audio', 'svg',
                         'form', 'input', 'textarea', 'button', 'select', 'label']):
            tag.decompose()

        # Limpiar atributos de todas las etiquetas
        for tag in soup.find_all(True):
            tag.attrs = {}
        for a in soup.find_all('a'):
            a.attrs = {}

        body = soup.body
        if not body:
            return None, "No se encontró contenido en el body"

        text = body.get_text(separator="\n", strip=True)
        return text, None

    except Exception as e:
        return None, str(e)

def summarize_text_with_gpt(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Resumí claramente el siguiente texto en español."},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error al generar el resumen: {str(e)}"

@app.route('/')
def summarize_scraped_url():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Falta la URL'}), 400

    text, error = scrape_text(url)
    if error:
        return jsonify({'error': error}), 500

    summary = summarize_text_with_gpt(text)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
