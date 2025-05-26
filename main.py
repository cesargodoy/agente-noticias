from scraper import obtener_todas_las_noticias
from resumen_gpt import resumir_noticia
import json
from datetime import datetime

def procesar_y_guardar():
    noticias = obtener_todas_las_noticias()
    noticias_con_resumen = []

    for n in noticias:
        print(f"Resumiendo: {n['titular']}")  # Para control en logs
        resumen = resumir_noticia(n['titular'], n['bajada'])
        n['resumen'] = resumen if resumen else "[Error al resumir]"
        noticias_con_resumen.append(n)

    nombre_archivo = f"data/noticias_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        json.dump(noticias_con_resumen, f, ensure_ascii=False, indent=2)

    print(f"Archivo guardado: {nombre_archivo}")

if __name__ == "__main__":
    procesar_y_guardar()

