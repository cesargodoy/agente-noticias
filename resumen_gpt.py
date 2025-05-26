import os
import openai

# Carga la clave desde variables de entorno (asegúrate de definir OPENAI_API_KEY en Render)
openai.api_key = os.getenv("OPENAI_API_KEY")

def resumir_noticia(titulo, bajada):
    prompt = f"""
Eres un asistente que resume noticias para un dashboard informativo. Resume la siguiente noticia en un solo párrafo breve, claro y objetivo:

Título: {titulo}
Bajada: {bajada}

Resumen:"""

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4-0613",  # También puedes usar "gpt-3.5-turbo" si prefieres menor costo
            messages=[
                {"role": "system", "content": "Eres un asistente experto en resumir noticias."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        resumen = respuesta['choices'][0]['message']['content'].strip()
        return resumen

    except Exception as e:
        print(f"Error al generar resumen: {e}")
        return None

