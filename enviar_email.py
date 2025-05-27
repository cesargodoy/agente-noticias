import os
import json
import requests
from datetime import datetime
import base64

API_KEY = os.getenv("BREVO_API_KEY")

def obtener_archivos():
    fecha = datetime.now().strftime("%Y-%m-%d")
    json_path = f"data/noticias_{fecha}.json"
    audio_path = "resumen_podcast.mp3"

    archivos = []

    if os.path.exists(json_path):
        with open(json_path, "rb") as f:
            contenido = base64.b64encode(f.read()).decode()
            archivos.append({
                "content": contenido,
                "name": f"noticias_{fecha}.txt"
            })

    if os.path.exists(audio_path):
        with open(audio_path, "rb") as f:
            contenido = base64.b64encode(f.read()).decode()
            archivos.append({
                "content": contenido,
                "name": "resumen_podcast.mp3"
            })

    return archivos

def enviar_email():
    if not API_KEY:
        raise Exception("BREVO_API_KEY no configurado.")

    url = "https://api.brevo.com/v3/smtp/email"
    archivos = obtener_archivos()

    data = {
        "sender": {"name": "Resumen Noticias", "email": "cgodoy@gmail.com"},
        "to": [
            {"email": "cesar@03.cl"},
            {"email": "francisco.opazo75@gmail.com"},
            {"email": "fernando.larrain@gmail.com"}
        ],
        "subject": "Resumen diario de noticias",
        "htmlContent": "<p>Adjuntamos el resumen de noticias del día en formato TXT y audio MP3.</p>",
        "attachment": archivos
    }

    headers = {
        "accept": "application/json",
        "api-key": API_KEY,
        "content-type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        print("📬 Email enviado correctamente con Brevo.")
    else:
        print(f"❌ Error al enviar email: {response.status_code} - {response.text}")

if __name__ == "__main__":
    enviar_email()
