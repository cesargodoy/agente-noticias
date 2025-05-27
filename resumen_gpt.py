import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def resumir_noticia(titular, bajada):
    try:
        mensaje = (
            f"Titular: {titular}\nBajada: {bajada}\n\n"
            "Resume esta noticia en un texto de 4 a 5 líneas, en español, "
            "de forma clara, informativa y con un poco más de detalle que un titular."
        )

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un periodista chileno que redacta resúmenes de noticias para medios digitales."},
                {"role": "user", "content": mensaje}
            ],
            temperature=0.8,  # un poco más variado
            max_tokens=300    # permite más espacio de texto
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error al generar resumen: {e}")
        return ""
