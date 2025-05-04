from flask import Flask, request, jsonify
from seo_utils import extract_seo_data
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url')

    try:
        seo_data = extract_seo_data(url)

        prompt = (
            "Analiza el siguiente contenido HTML desde una perspectiva SEO y "
            "genera recomendaciones prácticas para mejorar la visibilidad en buscadores. "
            "Considera estructura, palabras clave, etiquetas, accesibilidad y velocidad de carga. "
            f"Contenido: {seo_data['text_sample']}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )

        gpt_output = response['choices'][0]['message']['content']

        return jsonify({
            'seo_summary': gpt_output,
            'original_data': seo_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
