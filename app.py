from flask import Flask, request, jsonify
from seo_utils import extract_seo_data
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS
import logging

# Cargar la clave API desde el entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Inicializar la app Flask
app = Flask(__name__)

# Configurar CORS para permitir el dominio del frontend
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

        # Realizar scraping
        seo_data = extract_seo_data(url)
        logging.info("✅ Scraping exitoso")

        # Crear prompt para GPT
        prompt = (
            "Analiza el siguiente contenido HTML desde una perspectiva SEO y "
            "genera recomendaciones prácticas para mejorar la visibilidad en buscadores. "
            "Considera estructura, palabras clave, etiquetas, accesibilidad y velocidad de carga. "
            f"Contenido: {seo_data['text_sample']}"
        )

        # Llamar a OpenAI con gpt-4.1-mini
        response = openai.ChatCompletion.create(
            model="gpt-4.1-mini",  # ← Asegúrate de tener acceso a este modelo
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
        logging.exception("❌ Error durante el análisis SEO:")
        return jsonify({'error': str(e)}), 500
