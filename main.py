from flask import Flask, jsonify, send_file
from flask_cors import CORS
import os
import json
from datetime import datetime
import subprocess
from scraper import obtener_todas_las_noticias
from resumen_gpt import resumir_noticia

app = Flask(__name__)
CORS(app, origins=["https://03.cl"])

LOG_FILE = "log.txt"
BANCA_KEYWORDS = ["banco", "banca", "financiero", "financiera", "crédito", "interés", "santander", "Banco Santander"]
MARCA_OBJETIVO = ["santander", "banco santander"]

def escribir_log(linea):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {linea}\n")

def es_noticia_de_santander(noticia):
    texto = f"{noticia['titular']} {noticia['bajada']} {noticia.get('resumen', '')}".lower()
    tiene_santander = any(kw in texto for kw in MARCA_OBJETIVO)
    es_banca = any(kw in texto for kw in BANCA_KEYWORDS)
    return tiene_santander and es_banca

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

@app.route("/api/santander", methods=["GET"])
def noticias_santander():
    fecha = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join("data", f"santander_{fecha}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({"error": "No hay noticias filtradas por Santander"}), 404

@app.route("/log.txt")
def ver_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("[log.txt creado automáticamente]\n")
    return send_file(LOG_FILE, mimetype="text/plain")

@app.route("/resumen.mp3")
def resumen_podcast():
    ruta = "resumen_podcast.mp3"
    if os.path.exists(ruta):
        return send_file(ruta, mimetype="audio/mpeg")
    return "Audio no disponible", 404

def procesar_y_guardar():
    escribir_log("🟢 Iniciando scraping")
    noticias = obtener_todas_las_noticias()
    escribir_log(f"🔍 Total noticias encontradas: {len(noticias)}")

    noticias_con_resumen = []
    santander_relevantes = []

    for n in noticias:
        escribir_log(f"📰 Resumiendo: {n['titular']}")
        resumen = resumir_noticia(n['titular'], n['bajada'])
        n['resumen'] = resumen if resumen else "[Error al resumir]"
        noticias_con_resumen.append(n)
        if es_noticia_de_santander(n):
            santander_relevantes.append(n)

    os.makedirs("data", exist_ok=True)
    fecha_actual = datetime.now()
    fecha_str = fecha_actual.strftime('%Y-%m-%d')

    salida_general = {
        "ultima_actualizacion": fecha_actual.strftime("%Y-%m-%d %H:%M"),
        "noticias": noticias_con_resumen
    }
    salida_santander = {
        "ultima_actualizacion": fecha_actual.strftime("%Y-%m-%d %H:%M"),
        "noticias": santander_relevantes
    }

    with open(f"data/noticias_{fecha_str}.json", "w", encoding="utf-8") as f:
        json.dump(salida_general, f, ensure_ascii=False, indent=2)
    with open(f"data/santander_{fecha_str}.json", "w", encoding="utf-8") as f:
        json.dump(salida_santander, f, ensure_ascii=False, indent=2)

    escribir_log(f"✅ Archivos guardados: noticias_{fecha_str}.json y santander_{fecha_str}.json")

    try:
        subprocess.run(["python", "generar_audio_podcast.py"], check=True)
        escribir_log("🎧 Audio podcast generado correctamente.")
    except Exception as e:
        escribir_log(f"❌ Error al generar podcast: {e}")

if __name__ == "__main__":
    procesar_y_guardar()
    app.run(host="0.0.0.0", port=10000)
