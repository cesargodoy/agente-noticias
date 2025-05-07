from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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
    kp = data.get("keywords_principales", [])
    ks = data.get("keywords_secundarias", [])

    if not tipo or not tema:
        return jsonify({"error": "Faltan el tipo o tema"}), 400

    prompt_base = {
        "landing": "Redacta una landing page con enfoque UX para un sitio público sobre: {tema}.",
        "ctas": "Genera llamados a la acción (CTAs) claros, inclusivos y persuasivos para un sitio público sobre: {tema}.",
        "uxscript": "Redacta microcopys UX breves y efectivos para una interfaz pública sobre: {tema}."
    }

    prompt = prompt_base.get(tipo)
    if not prompt:
        return jsonify({"error": "Tipo no válido"}), 400

    if kp or ks:
        prompt += "\n\nIncluye de forma natural estas palabras clave:"
        if kp:
            prompt += f"\n- Principales: {', '.join(kp)}"
        if ks:
            prompt += f"\n- Secundarias: {', '.join(ks)}"

    contenido = ask_gpt(prompt, tema)
    return jsonify({"contenido": contenido})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
