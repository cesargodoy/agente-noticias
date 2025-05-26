from flask import Flask, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
from scraper import obtener_todas_las_noticias
from resumen_gpt import resumir_noticia

app = Flask(__name__)
CORS(app, origins=["https://03.cl"])  # Permite llamadas desde tu frontend

@app.route("/")
def home():
    return "✅ API de Noticias funcionando"

@app.route("/api/noticias", methods=["GET"])
def noticias_json():
    fecha = datetime.now().strftime("%Y-%m-%d")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(BASE_DIR, "data", f"noticias_{fecha}.json")

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)

    return jsonify({"error": "No hay noticias generadas hoy"}), 404

def procesar_y_guardar():
    noticias = obtener_todas_las_noticias()
    noticias_con_resumen = []

    for n in noticias:
        print(f"Resumiendo: {n['titular']}")
        resumen = resumir_noticia(n['titular'], n['bajada'])
        n['resumen'] = resumen if resumen else "[Error al resumir]"
        noticias_con_resumen.append(n)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(BASE_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)

    fecha_actual = datetime.now()
    nombre_archivo = os.path.join(data_dir, f"noticias_{fecha_actual.strftime('%Y-%m-%d')}.json")

    salida = {
        "ultima_actualizacion": fecha_actual.strftime("%Y-%m-%d %H:%M"),
        "noticias": noticias_con_resumen
    }

    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    print(f"✅ Archivo guardado: {nombre_archivo}")

if __name__ == "__main__":
    procesar_y_guardar()
    app.run(host="0.0.0.0", port=10000)
