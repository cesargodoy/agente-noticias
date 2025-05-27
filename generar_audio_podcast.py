import os
import json
from datetime import datetime
import openai

# Tu clave debe estar cargada como variable de entorno en Render
openai.api_key = os.getenv("OPENAI_API_KEY")

INTRODUCCION = (
    "Bienvenidos al resumen diario de noticias del Diario Financiero y Emol, "
    "por parte de la vicepresidencia de Marketing y Estudios."
)

CIERRE = (
    "Muchas gracias por escuchar el resumen diario de noticias "
    "de la Vicepresidencia de Marketing y estudios."
)

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

def generar_audio_openai(texto, filename="resumen_podcast.mp3"):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",  # También puedes probar: "nova", "shimmer", "fable", "onyx", "echo"
        input=texto
    )
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"🎧 Audio guardado como: {filename}")

if __name__ == "__main__":
    noticias = cargar_noticias()
    if noticias:
        guion = construir_guion(noticias)
        generar_audio_openai(guion)
    else:
        print("⚠️ No hay noticias disponibles para generar audio.")
