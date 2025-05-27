#!/usr/bin/env bash

echo "🔧 Descargando e instalando FFmpeg..."

# Crear carpeta local para FFmpeg
mkdir -p ffmpeg

# Descargar y descomprimir versión estática de FFmpeg
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar xJ --strip-components=1 -C ffmpeg

# Hacer el ejecutable accesible
chmod +x ffmpeg/ffmpeg

# Añadirlo al PATH para que pydub lo detecte
echo 'export PATH=$PWD/ffmpeg:$PATH' >> ~/.bashrc
export PATH=$PWD/ffmpeg:$PATH

echo "✅ FFmpeg instalado y disponible en: $PWD/ffmpeg"
