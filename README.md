# Traductor OCR para Juegos

Este es un traductor en tiempo real construido con Python y Tesseract. 
Permite seleccionar un área de la pantalla (en un juego) y traduce 
el texto de inglés a español.

## Características
- Captura de pantalla y OCR con Tesseract y OpenCV.
- Traducción usando Google Translate.
- GUI construida con Tkinter.
- Función de traductor inverso (Español a Inglés).

## Instalación

1.  Clona el repositorio.
2.  Crea un entorno virtual: `python -m venv .venv`
3.  Activa el entorno: `.\.venv\Scripts\Activate`
4.  Instala las dependencias: `pip install -r requirements.txt`
5.  (Solo Windows) Instala Tesseract-OCR: [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
6.  Ejecuta el script: `python traductorocr.py`