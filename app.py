from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

client = OpenAI()

def ask_gpt(prompt, texto):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": texto}
            ] if texto else [
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['POST'])
def generar_contenido():
    data = request.get_json()

    # 🆕 Soporte para prompt personalizado
    prompt_directo = data.get("prompt", "").strip()
    if prompt_directo:
        contenido = ask_gpt(prompt_directo, "")
        return jsonify({"contenido": contenido})

    # 🧱 Soporte estructurado
    tipo = data.get("tipo", "").strip().lower()
    tema = data.get("tema", "").strip()
    kp = data.get("keywords_principales", [])
    ks = data.get("keywords_secundarias", [])

    if not tipo or not tema:
        return jsonify({"error": "Faltan el tipo o tema"}), 400

    prompt_base = {
        "landing": (
            "Redacta una landing page profesional en castellano chileno para un sitio público sobre: {tema}.\n\n"
            "Debe seguir las mejores prácticas de SEO:\n"
            "- No uses etiquetas HTML\n"
            "- Usa encabezados, párrafos, listas o llamados a la acción como texto claro\n"
            "- Al final del contenido, sugiere una estructura HTML (lista con H1, H2, etc.)\n"
            "- Incluye una meta descripción sugerida (máx 160 caracteres)\n"
            "- Usa lenguaje claro y natural apropiado para usuarios chilenos"
        ),
        "ctas": (
            "Genera llamados a la acción (CTAs) persuasivos en castellano chileno para un sitio público sobre: {tema}.\n"
            "No uses etiquetas HTML. Usa un estilo claro y directo."
        ),
        "uxscript": (
            "Redacta microcopys UX breves y efectivos en castellano chileno para una interfaz pública sobre: {tema}.\n"
            "No uses etiquetas HTML."
        )
    }

    prompt = prompt_base.get(tipo)
    if not prompt:
        return jsonify({"error": "Tipo no válido"}), 400

    prompt = prompt.format(tema=tema)

    if kp or ks:
        prompt += (
            "\n\nIntegrá las siguientes palabras clave de forma coherente y contextualizada, "
            "como parte de frases naturales relacionadas con el tema:"
        )
        if kp:
            prompt += f"\n- Principales: {', '.join(kp)}"
        if ks:
            prompt += f"\n- Secundarias: {', '.join(ks)}"

    contenido = ask_gpt(prompt, tema)
    return jsonify({"contenido": contenido})

@app.route('/sugerencia', methods=['POST'])
def sugerencia_parrafo():
    data = request.get_json()
    parrafo = data.get("parrafo", "").strip()

    if not parrafo:
        return jsonify({"error": "Falta el párrafo"}), 400

    prompt = (
        "Sugiere una mejor redacción para este párrafo en castellano chileno. "
        "Mantén el significado, pero mejora el estilo, la claridad y la fluidez. "
        "Devuelve solo el párrafo mejorado sin agregar explicaciones."
    )

    sugerencia = ask_gpt(prompt, parrafo)
    return jsonify({"sugerencia": sugerencia})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
