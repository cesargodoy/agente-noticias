import os
import json
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition
import base64

def cargar_noticias():
    fecha = datetime.now().strftime("%Y-%m-%d")
    archivo = f"data/noticias_{fecha}.json"
    if not os.path.exists(archivo):
        return []
    with open(archivo, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("noticias", [])

def construir_html(noticias):
    bloques = []
    for n in noticias:
        bloque = f"<h3>{n['titular']}</h3><p><strong>Bajada:</strong> {n['bajada']}</p><p><em>{n['resumen']}</em></p><hr>"
        bloques.append(bloque)
    return "<h2>Resumen Diario de Noticias</h2>" + "".join(bloques)

def adjuntar_archivo(ruta, tipo):
    with open(ruta, "rb") as f:
        contenido = f.read()
    adjunto = Attachment()
    adjunto.file_content = FileContent(base64.b64encode(contenido).decode())
    adjunto.file_type = FileType(tipo)
    adjunto.file_name = FileName(os.path.basename(ruta))
    adjunto.disposition = Disposition("attachment")
    return adjunto

def enviar_email():
    api_key = os.environ.get("SENDGRID_API_KEY")
    if not api_key:
        raise Exception("SENDGRID_API_KEY no encontrada.")

    noticias = cargar_noticias()
    if not noticias:
        print("⚠️ No hay noticias disponibles para enviar.")
        return

    fecha = datetime.now().strftime("%Y-%m-%d")
    html_content = construir_html(noticias)

    message = Mail(
        from_email=Email("no-reply@03.cl", "Resumen Diario"),
        to_emails=To("cesar@03.cl"),
        subject="Prueba resumen noticias",
        html_content=Content("text/html", html_content)
    )

    # Adjuntar archivo de audio
    if os.path.exists("resumen_podcast.mp3"):
        message.add_attachment(adjuntar_archivo("resumen_podcast.mp3", "audio/mpeg"))

    # Adjuntar JSON de noticias
    json_path = f"data/noticias_{fecha}.json"
    if os.path.exists(json_path):
        message.add_attachment(adjuntar_archivo(json_path, "application/json"))

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f"✅ Email enviado. Status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error al enviar email: {e}")

if __name__ == "__main__":
    enviar_email()
