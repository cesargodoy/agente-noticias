import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import re

# Inicialización de la app Flask
app = Flask(__name__)

# Configuración de CORS para permitir solicitudes desde https://03.cl y http://www.03.cl
CORS(app, resources={r"/*": {"origins": ["https://03.cl", "http://www.03.cl"]}}, supports_credentials=True)

# Manejo de la solicitud OPTIONS (para las solicitudes preflight CORS)
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# Asegurarse de que las rutas OPTIONS sean manejadas correctamente
@app.route('/', methods=['OPTIONS'])
def handle_options():
    print("Preflight request received for /")
    return '', 204  # Responde con un código 204 a las solicitudes OPTIONS

# Función para analizar enlaces rotos
def check_broken_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    broken_links = []

    for link in links:
        link_url = link['href']
        if not link_url.startswith('http'):
            continue  # Solo comprobar enlaces completos (no relativos)
        try:
            link_response = requests.head(link_url, allow_redirects=True)
            if link_response.status_code != 200:
                broken_links.append(link_url)
        except requests.RequestException:
            broken_links.append(link_url)

    return broken_links

# Función básica de análisis SEO
def seo_analysis(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.title.string if soup.title else 'No Title'
    meta_description = ''
    
    meta_tag = soup.find('meta', {'name': 'description'})
    if meta_tag and 'content' in meta_tag.attrs:
        meta_description = meta_tag['content']
    
    return {
        'title': title,
        'meta_description': meta_description
    }

# Función de análisis de semántica HTML
def html_semantics(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Verificar el uso de elementos semánticos básicos
    elements = ['header', 'footer', 'main', 'article', 'section', 'nav']
    used_elements = {element: len(soup.find_all(element)) > 0 for element in elements}
    
    return used_elements

# Endpoint para el análisis de URL (raíz de la aplicación)
@app.route('/', methods=['POST'])
def analyze_url():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        # Realizar análisis SEO
        seo_result = seo_analysis(url)
        
        # Verificar enlaces rotos
        broken_links = check_broken_links(url)
        
        # Analizar semántica HTML
        semantics = html_semantics(url)
        
        # Devolver los resultados en formato JSON
        result = {
            "SEO": seo_result,
            "Broken Links": broken_links,
            "HTML Semantics": semantics
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ejecutar la app de Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
