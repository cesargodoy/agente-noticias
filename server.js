const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const cors = require('cors');
require('dotenv').config();

const app = express();

// 🟢 Permitir CORS desde cualquier origen
app.use(cors());

app.use(express.json());

app.post('/', async (req, res) => {
  const { url } = req.body;
  console.log("Analizando URL:", url);

  try {
    const { data: html } = await axios.get(url);
    const $ = cheerio.load(html);
    const title = $('title').text();
    const metaDescription = $('meta[name="description"]').attr('content') || '';
    const h1 = $('h1').first().text();

    const prompt = `Analiza el siguiente sitio web y proporciona recomendaciones para mejorar su SEO:\n\nTítulo: ${title}\nMeta descripción: ${metaDescription}\nEncabezado H1: ${h1}`;

    console.log("Prompt:", prompt);

    const openaiResponse = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-4', // Cambiar a 'gpt-3.5-turbo' si no tienes acceso
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
    if (error.response) {
      console.error("❌ Error OpenAI:", JSON.stringify(error.response.data, null, 2));
      res.status(500).json({ error: error.response.data });
    } else {
      console.error("❌ Error general:", error.message);
      res.status(500).json({ error: 'Error interno del servidor' });
    }
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en puerto ${PORT}`);
});

