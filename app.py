from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": "https://03.cl"}})

def scrape_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return {'error': f'No se puede acceder a la página. Código de error: {response.status_code}'}

        soup = BeautifulSoup(response.text, 'html.parser')

        # Eliminar etiquetas no deseadas (scripts, estilos, multimedia y formularios)
        for tag in soup(['script', 'style', 'img', 'video', 'audio', 'svg', 'form', 'input', 'textarea', 'button', 'select', 'label']):
            tag.decompose()

        # Eliminar todos los atributos de todas las etiquetas
        for tag in soup.find_all(True):
            tag.attrs = {}

        # Extraer solo el contenido del body
        body = soup.body
        clean_html = body.prettify() if body else soup.prettify()

        return {'url': url, 'html': clean_html}

    except requests.exceptions.RequestException as e:
        return {'error': f'Error de conexión: {str(e)}'}

@app.route('/')
def scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL no proporcionada'}), 400

    result = scrape_page(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
