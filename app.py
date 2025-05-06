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

    text, error = scrape_text(url)
    if error:
        return jsonify({'error': error}), 500

    # Generar resumen
    summary_prompt = "Resumí claramente el siguiente texto en español."
    summary = ask_gpt(summary_prompt, text)

    # Generar análisis SEO
    seo_prompt = (
        "Evalúa el siguiente contenido web en términos de SEO usando estos criterios:\n\n"
        "1. Calidad del contenido\n"
        "   - Relevancia\n   - Originalidad\n   - Claridad y legibilidad\n   - Precisión\n   - Autoridad\n   - Atractivo\n"
        "2. Estructura\n"
        "   - Títulos y subtítulos\n   - Párrafos\n   - Listas y viñetas\n   - Sintaxis general\n"
        "3. Keywords\n"
        "   - Relevancia\n   - Uso adecuado\n"
        "4. Enlaces\n"
        "   - Enlaces internos\n   - Enlaces externos\n   - Texto anclaje\n"
        "5. Experiencia de usuario\n"
        "   - Accesibilidad\n   - Uso de alt en imágenes (si aplica)\n\n"
        "Entrega un informe estructurado punto por punto y comenta brevemente cada aspecto."
    )
    seo_report = ask_gpt(seo_prompt, text)

    return jsonify({
        'summary': summary,
        'seo_report': seo_report
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
