from flask import Flask, request, jsonify
from seo_utils import extract_seo_data
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS
import logging

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app, origins=["https://03.cl"])

# Habilita logging
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            logging.error("No se proporcionó una URL válida.")
            return jsonify({'error': 'No se proporcionó una URL válida.'}), 400

        url = data['url']
        logging.info(f"Recibida URL: {url}")

        seo_data = extract_seo_data(url)
        logging.info("Datos SEO extraídos correctamente")

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
        logging.info("Respuesta GPT recibida correctamente")

        return jsonify({
            'seo_summary': gpt_output,
            'original_data': seo_data
        })

    except Exception as e:
        logging.exception("Error interno al procesar la solicitud:")
        return jsonify({'error': 'Error interno del servidor.'}), 500


