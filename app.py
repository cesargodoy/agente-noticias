from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os
import openai

app = Flask(__name__)
CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        url = data.get("url")
        if not url:
            return jsonify({"error": "No se proporcionó una URL."}), 400

        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string.strip() if soup.title else ''
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        meta_charset = soup.find('meta', charset=True)
        h1_tags = soup.find_all('h1')

        missing_tags = []
        if not title:
            missing_tags.append('title')
        if not meta_desc:
            missing_tags.append('meta name="description"')
        if not meta_robots:
            missing_tags.append('meta name="robots"')
        if not meta_charset:
            missing_tags.append('meta charset')
        if not h1_tags:
            missing_tags.append('h1')

        visible_text = soup.get_text(separator=' ', strip=True)
        word_count = len(visible_text.split())

        headers = {
            'title': title,
            'h1': [h.get_text(strip=True) for h in h1_tags],
        }

        content_sample = visible_text[:1000]
        prompt = (
            "Analiza el siguiente contenido HTML desde una perspectiva SEO y genera recomendaciones prácticas para mejorar "
            "la visibilidad en buscadores. Considera estructura, palabras clave, etiquetas, accesibilidad y velocidad de carga.\n"
            f"Contenido: {content_sample}"
        )

        gpt_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un experto en SEO."},
                {"role": "user", "content": prompt}
            ]
        )

        analysis = gpt_response.choices[0].message.content.strip()

        return jsonify({
            "seo_summary": analysis,
            "headers": headers,
            "word_count": word_count,
            "missing_tags": missing_tags
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
