import os
import openai

# Asegúrate de que esta línea esté presente
openai.api_key = os.getenv("OPENAI_API_KEY")

def resumir_noticia(titular, bajada):
    try:
        mensaje = f"Titular: {titular}\nBajada: {bajada}\n\nResume esta noticia en máximo 3 líneas, en español, con lenguaje claro."

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un periodista que redacta resúmenes breves y claros."},
                {"role": "user", "content": mensaje}
            ],
            temperature=0.7,
            max_tokens=100
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error al generar resumen: {e}")
        return ""
