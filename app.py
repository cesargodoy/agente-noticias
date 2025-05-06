from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS  # Importar CORS

app = Flask(__name__)

# Habilitar CORS para permitir solicitudes desde https://03.cl
CORS(app, resources={r"/": {"origins": "https://03.cl"}})  # Solo permitir solicitudes desde Hostgator

# Función para hacer scraping de una URL proporcionada
def scrape_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Hacemos la solicitud GET a la URL con los encabezados
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción si la respuesta HTTP es un error (404, 500, etc.)

        # Usamos BeautifulSoup para parsear el HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer el texto de las etiquetas <p>, <h1>, <h2>, <title> y otras relevantes
        paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'span', 'li'])
        page_text = ' '.join([para.get_text() for para in paragraphs])  # Unir el texto de las etiquetas
        page_text = page_text[:1500]  # Limitar el texto extraído (1500 caracteres)

        return {'url': url, 'text': page_text}
    
    except requests.exceptions.RequestException as e:
        return {'url': url, 'error': str(e)}

# Ruta para hacer scraping de una URL proporcionada por el usuario (raíz '/')
@app.route('/')
def scrape():
    url = request.args.get('url')  # Obtener la URL del parámetro de consulta

    if not url:
        return jsonify({'error': 'URL no proporcionada'}), 400  # Si no se proporciona la URL, devolvemos un error
    
    result = scrape_page(url)  # Realizar el scraping de la URL proporcionada
    return jsonify(result)  # Devolvemos los resultados en formato JSON

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
