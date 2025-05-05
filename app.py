from flask import Flask, request, jsonify
from flask_cors import CORS  # Importamos CORS

# Inicializar Flask
app = Flask(__name__)

# Habilitar CORS para permitir solicitudes desde diferentes dominios
CORS(app)

# Función para simular una optimización SEO del texto
def optimize_text(text):
    # Aquí puedes agregar la lógica real de optimización SEO
    optimized_text = text.replace("SEO", "SEO optimizado")  # Ejemplo simple
    seo_summary = "Se han optimizado palabras clave, mejorado la legibilidad y añadido meta descripción."
    return optimized_text, seo_summary

# Función para simular el análisis SEO de una URL
def analyze_url(url):
    # Lógica para analizar una URL
    seo_summary = "URL optimizada. Se encontró un buen uso de palabras clave."
    optimized_text = "Texto optimizado para la URL."
    funnel_analysis = "Análisis del funnel: Añadir más llamadas a la acción."
    return optimized_text, seo_summary, funnel_analysis

# Ruta principal para procesar las solicitudes POST de la URL o el texto
@app.route('/', methods=['POST'])
def analyze():
    data = request.get_json()  # Obtener los datos del cuerpo de la solicitud
    
    # Si la solicitud contiene una URL
    if 'url' in data:
        url = data['url']
        optimized_text, seo_summary, funnel_analysis = analyze_url(url)
        return jsonify({
            'optimized_text': optimized_text,
            'seo_summary': seo_summary,
            'funnel_analysis': funnel_analysis
        })
    
    # Si la solicitud contiene un texto
    elif 'text' in data:
        text = data['text']
        optimized_text, seo_summary = optimize_text(text)
        return jsonify({
            'optimized_text': optimized_text,
            'seo_summary': seo_summary,
            'funnel_analysis': "Análisis del funnel: No aplicable para texto."
        })
    
    # Si no se proporcionó ni URL ni texto
    return jsonify({'error': 'No se proporcionó ni URL ni texto.'}), 400

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
