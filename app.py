from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS  # Importar CORS

app = Flask(__name__)

# Habilitar CORS para permitir solicitudes desde https://03.cl
CORS(app, resources={r"/scrape": {"origins": "https://03.cl"}})  # Solo permitir solicitudes desde Hostgator

# Función para hacer scraping de una URL
def scrape_page(url):
    try:
        # Hacemos una solicitud GET a la URL
        response = requests.get(url)
        # Usamos BeautifulSoup para parsear el HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos el primer título <h1> en la página
        title = soup.find('h1').text if soup.find('h1') else 'Título no encontrado'
        return {'url': url, 'title': title}
    except Exception as e:
        return {'url': url, 'error': str(e)}

# Ruta para hacer scraping de varias páginas
@app.route('/scrape')
def scrape():
    # Lista de URLs a scrapear
    urls = ['https://example1.com', 'https://example2.com', 'https://example3.com']
    
    # Realizamos el scraping para cada URL y almacenamos los resultados
    results = [scrape_page(url) for url in urls]
    
    # Devolvemos los resultados en formato JSON
    return jsonify(results)

if __name__ == '__main__':
    # Iniciamos el servidor en el puerto 5000, accesible desde cualquier IP
    app.run(debug=True, host='0.0.0.0', port=5000)
