import os
import json
from datetime import datetime
import openai
from pydub import AudioSegment

openai.api_key = os.getenv("OPENAI_API_KEY")

INTRODUCCION = (
    "Bienvenidos al resumen diario de noticias del Diario Financiero y Emol, "
    "por parte de la vicepresidencia de Marketing y Estudios."
)

CIERRE = (
    "Muchas gracias por escuchar el resumen diario de noticias "
    "de la Vicepresidencia de Marketing y estudios."
)

MAX_CHARS = 4000

def cargar_noticias():
    fecha = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join("data", f"noticias_{fecha}.json")
    if not os.path.exists(path):
        print("❌ No se encontró el archivo de noticias.")
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("noticias", [])

def construir_guion(noticias):
    bloques = [INTRODUCCION]
    for i, n in enumerate(noticias, 1):
        bloques.append(f"Noticia {i}: {n['titular']}. {n['resumen']}")
    bloques.append(CIERRE)
    return "\n\n".join(bloques)

def dividir_texto(texto, max_chars=MAX_CHARS):
    partes = []
    while len(texto) > max_chars:
        corte = texto[:max_chars].rfind(".")
        if corte == -1:
            corte = max_chars
        partes.append(texto[:corte+1].strip())
        texto = texto[corte+1:].strip()
    if texto:
        partes.append(texto)
    return partes

def generar_audio_partes(partes):
    archivos = []
    for i, parte in enumerate(partes):
        response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=parte
        )
        nombre = f"parte_{i+1}.mp3"
        with open(nombre, "wb") as f:
            f.write(response.content)
        archivos.append(nombre)
    return archivos

def unir_audios(archivos, salida="resumen_podcast.mp3"):
    combinado = AudioSegment.empty()
    for archivo in archivos:
        combinado += AudioSegment.from_mp3(archivo)
    combinado.export(salida, format="mp3")
    print(f"🎧 Audio final generado: {salida}")
    for archivo in archivos:
        os.remove(archivo)

if __name__ == "__main__":
    noticias = cargar_noticias()
    if noticias:
        guion = construir_guion(noticias)
        partes = dividir_texto(guion)
        archivos = generar_audio_partes(partes)
        unir_audios(archivos)
    else:
        print("⚠️ No hay noticias disponibles para generar audio.")
