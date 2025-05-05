const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3000;  // Render asignará un puerto dinámico

// Habilitar CORS para permitir solicitudes desde https://03.cl
app.use(cors({
  origin: 'https://03.cl',  // Cambia esto si tienes un subdominio o varios orígenes
  methods: ['GET'],
}));

// Función para hacer scraping de una URL y extraer el título
async function scrapePage(url) {
  try {
    const { data } = await axios.get(url);
    const $ = cheerio.load(data);

    // Ejemplo: Extraer el título de la página (puedes modificar esto según lo que necesites)
    const title = $('h1').text() || 'Título no encontrado';
    return { url, title };
  } catch (error) {
    console.error(`Error al hacer scraping en ${url}:`, error);
    return { url, error: 'Error al obtener los datos' };
  }
}

// Ruta para scrapear múltiples páginas
app.get('/scrape', async (req, res) => {
  // Lista de URLs a scrapear
  const urlsToScrape = [
    'https://example1.com',
    'https://example2.com',
    'https://example3.com',
  ];

  try {
    // Scraping de todas las páginas de forma paralela
    const scrapeResults = await Promise.all(urlsToScrape.map(url => scrapePage(url)));
    res.json(scrapeResults);  // Devuelve los resultados del scraping
  } catch (error) {
    res.status(500).json({ error: 'Error al realizar el scraping' });
  }
});

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor corriendo en http://localhost:${port}`);
});
