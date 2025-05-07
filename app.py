from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI()

def ask_gpt(prompt, tema):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": tema}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['POST'])
def generar_contenido():
    data = request.get_json()
    tipo = data.get("tipo", "").strip().lower()
    tema = data.get("tema", "").strip()

    if not tipo or not tema:
        return jsonify({"error": "Faltan el tipo o tema"}), 400

    prompt_map = {
        "landing": f"Redacta una landing page con enfoque UX para marketing digital sobre: {tema}",
        "email": f"Escribe un email de marketing digital con redacción clara y orientada a conversión sobre: {tema}",
        "post": f"Genera un post corto para redes sociales con enfoque de marketing digital UX sobre: {tema}",
        "uxscript": f"Escribe microtextos UX para una interfaz digital sobre: {tema}",
    }

    prompt = prompt_map.get(tipo)
    if not prompt:
        return jsonify({"error": "Tipo no válido"}), 400

    contenido = ask_gpt(prompt, tema)
    return jsonify({"contenido": contenido})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
