from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa la extensión CORS
import requests
from bs4 import BeautifulSoup
import openai
import os

app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)

# Tu clave API de OpenAI (GPT-4 mini) desde la variable de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/', methods=['POST'])
def scrape_and_analyze():
    # Obtén la URL desde el cuerpo de la solicitud
    url = request.json.get('url')
    
    if not url:
        return jsonify({"error": "URL es requerida"}), 400
    
    # Realiza el scraping de la página
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Usa BeautifulSoup para analizar el contenido HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()  # Extrae solo el texto
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al obtener la página: {str(e)}"}), 500

    # Llama a la API de GPT para analizar el contenido SEO
    try:
        analysis = openai.Completion.create(
            model="gpt-4",  # Asegúrate de tener acceso al modelo GPT-4 mini
            prompt=f"Analiza este contenido desde una perspectiva SEO y da recomendaciones: {content}",
            max_tokens=500
        )
        seo_analysis = analysis.choices[0].text.strip()
        
    except Exception as e:
        return jsonify({"error": f"Error al analizar con GPT-4: {str(e)}"}), 500
    
    return jsonify({"seo_analysis": seo_analysis})

if __name__ == '__main__':
    app.run(debug=True)
