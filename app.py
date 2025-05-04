from flask import Flask, request, jsonify
from seo_utils import extract_seo_data
import os
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app, origins=["https://03.cl"])
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'No se proporcionó una URL válida'}), 400

        url = data['url']
        logging.info(f"Probando scraping en URL: {url}")

        seo_data = extract_seo_data(url)

        return jsonify({
            'original_data': seo_data,
            'message': 'Scraping realizado correctamente (sin análisis GPT)'
        })

    except Exception as e:
        logging.exception("Error durante el scraping:")
        return jsonify({'error': 'Error interno al analizar la URL'}), 500
