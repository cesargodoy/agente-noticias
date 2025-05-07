from flask import Flask, request, jsonify
from flask_cors import CO
from openai import OpenAI

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
    kp = data.get("keywords_principales", [])
    ks = data.get("keywords_secundarias", [])

    if not tipo or not tema:
        return jsonify({"error": "Faltan el tipo o tema"}), 400

    prompt_base = {
        "landing": "Redacta una landing page con enfoque UX para marketing digital sobre: {tema}.",
        "email": "Escribe un email de marketing digital claro y persuasivo sobre: {tema}.",
        "post": "Genera un post atractivo para redes sociales sobre: {tema}.",
        "uxscript": "Redacta microtextos UX útiles para una interfaz digital sobre: {tema}."
    }

    prompt = prompt_base.get(tipo)
    if not prompt:
        return jsonify({"error": "Tipo no válido"}), 400

    # Agregar keywords al prompt si existen
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
