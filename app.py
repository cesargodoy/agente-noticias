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

        # Verificar si la respuesta es exitosa (código 200)
        if response.status_code != 200:
            return {'error': f'No se puede acceder a la página. Código de error: {response.status_code}'}

        # Usamos BeautifulSoup para parsear el HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraemos TODO el HTML de la página
        page_html = soup.prettify()  # Usamos prettify para darle formato al HTML

        return {'url': url, 'html': page_html}
    
    except requests.exceptions.RequestException as e:
        # Manejo de excepciones (problemas con la conexión, timeout, etc.)
        return {'error': f'Error de conexión: {str(e)}'}

# Ruta para hacer scraping de una URL proporcionada por el usuario (raíz '/')
@app.route('/')
def scrape():
    url = request.args.get('url')  # Obtener la URL del parámetro de consulta

    if not url:
        return jsonify({'error': 'URL no proporcionada'}), 400  # Si no se proporciona la URL, devolvemos un error
    
    result = scrape_page(url)  # Realizar el scraping de la URL proporcionada
    return jsonify(result)  # Devolvemos los resultados en formato JSON

if __name__ == '__main__':
    # Iniciamos el servidor en el puerto 5000, accesible desde cualquier IP
    app.run(debug=True, host='0.0.0.0', port=5000)
