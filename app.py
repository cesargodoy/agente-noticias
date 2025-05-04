from flask import Flask, request, jsonify
from seo_utils import extract_seo_data
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS
import logging

# Cargar clave de OpenAI desde .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# CORS con soporte para preflight
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "https://03.cl"}})

# Configurar logs
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'No se proporcionó una URL válida'}), 400

        url = data['url']
        logging.info(f"🔍 Analizando URL: {url}")

        seo_data = extract_seo_data(url)
        logging.info("✅ Scraping exitoso")

        prompt = (
            "Analiza el siguiente contenido HTML desde una perspectiva SEO y "
            "genera recomendaciones prácticas para mejorar la visibilidad en buscadores. "
            "Considera estructura, palabras clave, etiquetas, accesibilidad y velocidad de carga. "
            f"Contenido: {seo_data['text_sample']}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ✅ CAMBIO AQUÍ
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )

        gpt_output = response['choices'][0]['message']['content']
        logging.info("✅ GPT respondió correctamente")

        return jsonify({
            'seo_summary': gpt_output,
            'original_data': seo_data
        })

    except Exception as e:
        logging.exception("❌ Error en análisis SEO:")
        return jsonify({'error': str(e)}), 500
