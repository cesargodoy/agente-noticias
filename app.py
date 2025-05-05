from flask import Flask, request, jsonify
from flask_cors import CORS

# Inicialización de la app Flask
app = Flask(__name__)

# Configuración de CORS para permitir solicitudes desde https://03.cl
CORS(app, resources={r"/analyze/*": {"origins": "https://03.cl"}}, supports_credentials=True)

# Manejo de la solicitud OPTIONS (para las solicitudes preflight CORS)
@app.route('/analyze/<path:subpath>', methods=['OPTIONS'])
def handle_options(subpath):
    return '', 204  # Responde con un código 204 a las solicitudes OPTIONS

# Endpoints para el análisis de URL
@app.route('/analyze/url', methods=['POST'])
def analyze_url():
    data = request.get_json()
    url = data.get('url')

    # Lógica para analizar la URL (esto es solo un ejemplo, agrega tu lógica real aquí)
    analysis_result = {
        "SEO": {
            "title": "Ejemplo de Título Optimizado",
            "meta_description": "Esta es una descripción atractiva y rica en palabras clave."
        },
        "Palabras clave": {
            "principales": ["SEO", "análisis", "optimización"],
            "densidad": "Adecuada"
        },
        "Links rotos": {
            "total": 0
        },
        "Semántica HTML": {
            "correcto": True
        },
        "Accesibilidad": {
            "imagenes_sin_alt": 0,
            "contraste": "Cumple"
        },
        "CTAs": {
            "total": 3
        },
        "Redacción para funnels": {
            "estructura": "AIDA"
        }
    }

    return jsonify(analysis_result)

# Endpoint para el análisis de contenido manual
@app.route('/analyze/text', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text = data.get('text')

    # Lógica para analizar el texto (esto es solo un ejemplo, agrega tu lógica real aquí)
    analysis_result = {
        "SEO": {
            "title": "Ejemplo de Título Optimizado",
            "meta_description": "Esta es una descripción atractiva y rica en palabras clave."
        },
        "Palabras clave": {
            "principales": ["SEO", "análisis", "optimización"],
            "densidad": "Adecuada"
        },
        "Links rotos": {
            "total": 0
        },
        "Semántica HTML": {
            "correcto": True
        },
        "Accesibilidad": {
            "imagenes_sin_alt": 0,
            "contraste": "Cumple"
        },
        "CTAs": {
            "total": 3
        },
        "Redacción para funnels": {
            "estructura": "AIDA"
        }
    }

    return jsonify(analysis_result)

# Ejecutar la app de Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
