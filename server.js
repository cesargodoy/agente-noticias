const express = require('express');
const cors = require('cors');
const axios = require('axios');
const cheerio = require('cheerio');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(cors());
app.post('/', async (req, res) => {
  const { url } = req.body;
  
  try {
    // Realizar scraping del sitio
    const { data: html } = await axios.get(url);
    const $ = cheerio.load(html);
    const title = $('title').text();
    const metaDescription = $('meta[name="description"]').attr('content') || '';
    const h1 = $('h1').first().text();

    // Preparar el prompt para ChatGPT
    const prompt = `
      Analiza el siguiente sitio web y proporciona recomendaciones para mejorar su SEO:

      Título: ${title}
      Meta descripción: ${metaDescription}
      Encabezado H1: ${h1}
    `;

    // Llamar a la API de OpenAI
    const openaiResponse = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-4',
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.7
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`
        }
      }
    );

    const recomendaciones = openaiResponse.data.choices[0].message.content.trim();
    res.json({ recomendaciones });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error al analizar el sitio' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor escuchando en el puerto ${PORT}`);
});
