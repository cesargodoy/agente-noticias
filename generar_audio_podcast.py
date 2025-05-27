import os
import json
from datetime import datetime
from gtts import gTTS

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

def generar_audio(texto, filename="resumen_podcast.mp3"):
    tts = gTTS(text=texto, lang='es')
    tts.save(filename)
    print(f"🎧 Audio guardado como: {filename}")

if __name__ == "__main__":
    noticias = cargar_noticias()
    if noticias:
        guion = construir_guion(noticias)
        generar_audio(guion)
    else:
        print("⚠️ No hay noticias disponibles para generar audio.")
