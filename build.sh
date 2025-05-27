#!/usr/bin/env bash

# Crear carpeta temporal
mkdir -p ffmpeg

# Descargar ffmpeg estático
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar xJ --strip-components=1 -C ffmpeg

# Hacerlo ejecutable
chmod +x ffmpeg/ffmpeg

# Agregar al path para que Python lo encuentre
export PATH=$PWD/ffmpeg:$PATH
