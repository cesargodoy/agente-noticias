# 🚀 SEO Analyzer Backend (Flask + OpenAI)

Este proyecto analiza el contenido HTML de un sitio web, extrae información clave y usa GPT-4 para generar un diagnóstico SEO con sugerencias prácticas.

### Endpoint:
- `POST /analyze`
  - Body JSON: `{ "url": "https://ejemplo.com" }`
  - Respuesta: resumen SEO + mejoras sugeridas

Usa:
- Flask (API REST)
- BeautifulSoup (Scraping)
- OpenAI API (GPT-4)
- Desplegado en Render.com
