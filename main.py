from flask import Flask, jsonify, send_file
from flask_cors import CORS
import os
import json
from datetime import datetime
from scraper import obtener_todas_las_noticias
from resumen_gpt import resumir_noticia

app = Flask(__name__)
CORS(app, origins=["https://03.cl"])  # permite solicitudes desde tu frontend

LOG_FILE = "log.txt"

def escribir_log(linea):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {linea}\n")

@app.route("/")
def home():
    return "✅ API de Noticias funcionando"

@app.route("/api/noticias", methods=["GET"])
def noticias_json():
    fecha = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join("data", f"noticias_{fecha}.json")

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)

    return jsonify({"error": "No hay noticias generadas hoy"}), 404

@app.route("/log.txt")
def ver_log():
    return send_file(LOG_FILE, mimetype="text/plain")

def procesar_y_guardar():
    escribir_log("🟢 Iniciando scraping")
    noticias = obtener_todas_las_noticias()
    escribir_log(f"🔍 Total noticias encontradas: {len(noticias)}")

    noticias_con_resumen = []

    for n in noticias:
        escribir_log(f"📰 Resumiendo: {n['titular']}")
        resumen = resumir_noticia(n['titular'], n['bajada'])
        n['resumen'] = resumen if resumen else "[Error al resumir]"
        noticias_con_resumen.append(n)

    os.makedirs("data", exist_ok=True)
    fecha_actual = datetime.now()
    archivo_json = f"data/noticias_{fecha_actual.strftime('%Y-%m-%d')}.json"

    salida = {
        "ultima_actualizacion": fecha_actual.strftime("%Y-%m-%d %H:%M"),
        "noticias": noticias_con_resumen
    }

    with open(archivo_json, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    escribir_log(f"✅ Archivo guardado: {archivo_json}")

if __name__ == "__main__":
    procesar_y_guardar()
    app.run(host="0.0.0.0", port=10000)
