## TraductorOCRGame v3.0
TraductorOCRGame es una herramienta de escritorio multifuncional para Windows, diseñada para jugadores. Ofrece traducción en tiempo real tanto de texto en pantalla (mediante OCR) como de audio (mediante reconocimiento de voz).

La aplicación combina un potente motor de OCR con el reconocimiento de voz de Vosk y deep-translator para romper las barreras del idioma en tus juegos.

## Características Principales
1. Traductor de OCR (EN -> ES)
Selección de Área: Captura cualquier texto en tu pantalla con un simple clic y arrastre.

Ajuste de Previsualización (Ajustar OCR): ¿Texto claro sobre fondo oscuro? ¿Oscuro sobre fondo claro? No hay problema. Un afinador visual te permite ajustar el umbral (threshold) y la inversión de la imagen para garantizar la máxima precisión del OCR en cualquier situación.

Traductor Manual (ES -> EN): Un panel desplegable para traducciones rápidas de español a inglés.

2. Traductor de Audio (EN -> ES)
Reconocimiento de Voz en Vivo: Utiliza el motor de Vosk para capturar audio en inglés, ya sea desde tu micrófono o (con la configuración adecuada) directamente del audio de tu sistema.

Traducción Rápida: Transcribe y traduce el habla con pausas cortas, ideal para seguir diálogos en juegos, videos o streams.

Selector de Dispositivo: Elige la fuente de audio que deseas traducir.

3. Interfaz
Tema Oscuro Moderno: Interfaz rediseñada con ttkbootstrap (tema "darkly") para una apariencia limpia y profesional, similar a las aplicaciones de gaming modernas.

Siempre Visible: La ventana se mantiene encima de tu juego para que no pierdas de vista la traducción.

Ajuste de Transparencia: Configura la opacidad de la ventana para una integración perfecta con tu juego.

## Requisitos
Usuario Final (EXE)
Windows 10 / 11.

(Opcional pero recomendado) VB-CABLE Virtual Audio Device para la traducción de audio del sistema.

Desarrollo
Python 3.8+

Tesseract OCR (instalado y en el PATH del sistema).

Todas las dependencias listadas en requirements.txt.

Instalación
Usuario Final
Ve a la página de Releases.

Descarga el archivo TraductorOCR.exe de la última versión.

Ejecuta el archivo. (No requiere instalación).

## Desarrollo
Clona el repositorio:

Bash

git clone https://github.com/RenckLord/TraductorOCRGame.git
cd TraductorOCRGame
(Recomendado) Instala Tesseract OCR desde UB-Mannheim/tesseract.

Crea y activa un entorno virtual:

Bash

python -m venv .venv
.\.venv\Scripts\Activate
Instala las dependencias:

Bash

pip install -r requirements.txt
## ⚠️ Configuración OBLIGATORIA para Traducción de Audio del Sistema ⚠️
Para traducir el audio de tu juego (y no tu voz), la aplicación necesita "escuchar" la salida de audio de tu PC. Dispositivos como "Mezcla estéreo" (Stereo Mix) a veces fallan o no existen (especialmente en portátiles o con auriculares USB como HyperX).

La solución más robusta es usar un cable de audio virtual.

Pasos de Configuración con VB-CABLE
Instalar VB-CABLE:

Descarga e instala VB-CABLE Virtual Audio Device (es gratuito).

Reinicia tu PC si es necesario.

Configurar Salida de Windows:

Haz clic derecho en el ícono de altavoz 🔊 de Windows -> Sonidos.

Ve a la pestaña "Reproducción".

Establece CABLE Input (el dispositivo virtual) como tu dispositivo predeterminado.

En este punto, dejarás de escuchar el audio de tu PC. Es normal.

Configurar "Escuchar" (Para que tú oigas):

En la misma ventana de "Sonidos", ve a la pestaña "Grabar".

Busca CABLE Output -> clic derecho -> Propiedades.

Ve a la pestaña "Escuchar".

Marca la casilla "Escuchar este dispositivo".

En el menú "Reproducir a través de este dispositivo", selecciona tus audífonos o altavoces reales (ej: "Altavoces (HyperX)").

Pulsa "Aplicar". Ahora deberías volver a escuchar el audio de tu PC.

Configurar el TraductorOCR:

Inicia la aplicación.

En el panel "Traductor de Audio", selecciona CABLE Output como tu dispositivo.

Inicia la captura.
¡Excelente idea! Ese README estaba pidiendo una jubilación a gritos. Se quedó atascado en la versión 1.0, mientras que nosotros ya estamos construyendo la 3.0.

Aquí tienes una versión completamente actualizada que incluye las nuevas funciones de audio, el ajuste de OCR y, lo más importante, las instrucciones para el VB-CABLE.

TraductorOCRGame v3.0
TraductorOCRGame es una herramienta de escritorio multifuncional para Windows, diseñada para jugadores. Ofrece traducción en tiempo real tanto de texto en pantalla (mediante OCR) como de audio (mediante reconocimiento de voz).

La aplicación combina un potente motor de OCR con el reconocimiento de voz de Vosk y deep-translator para romper las barreras del idioma en tus juegos.

## Características Principales
1. Traductor de OCR (EN -> ES)
Selección de Área: Captura cualquier texto en tu pantalla con un simple clic y arrastre.

Ajuste de Previsualización (Ajustar OCR): ¿Texto claro sobre fondo oscuro? ¿Oscuro sobre fondo claro? No hay problema. Un afinador visual te permite ajustar el umbral (threshold) y la inversión de la imagen para garantizar la máxima precisión del OCR en cualquier situación.

Traductor Manual (ES -> EN): Un panel desplegable para traducciones rápidas de español a inglés.

2. Traductor de Audio (EN -> ES)
Reconocimiento de Voz en Vivo: Utiliza el motor de Vosk para capturar audio en inglés, ya sea desde tu micrófono o (con la configuración adecuada) directamente del audio de tu sistema.

Traducción Rápida: Transcribe y traduce el habla con pausas cortas, ideal para seguir diálogos en juegos, videos o streams.

Selector de Dispositivo: Elige la fuente de audio que deseas traducir.

3. Interfaz
Tema Oscuro Moderno: Interfaz rediseñada con ttkbootstrap (tema "darkly") para una apariencia limpia y profesional, similar a las aplicaciones de gaming modernas.

Siempre Visible: La ventana se mantiene encima de tu juego para que no pierdas de vista la traducción.

Ajuste de Transparencia: Configura la opacidad de la ventana para una integración perfecta con tu juego.

Requisitos
Usuario Final (EXE)
Windows 10 / 11.

(Opcional pero recomendado) VB-CABLE Virtual Audio Device para la traducción de audio del sistema.

## Desarrollo
Python 3.8+

Tesseract OCR (instalado y en el PATH del sistema).

Todas las dependencias listadas en requirements.txt.

Instalación
Usuario Final
Ve a la página de Releases.

Descarga el archivo TraductorOCR.exe de la última versión.

Ejecuta el archivo. (No requiere instalación).

## Desarrollo
Clona el repositorio:

Bash

git clone https://github.com/RenckLord/TraductorOCRGame.git
cd TraductorOCRGame
(Recomendado) Instala Tesseract OCR desde UB-Mannheim/tesseract.

Crea y activa un entorno virtual:

Bash

python -m venv .venv
.\.venv\Scripts\Activate
Instala las dependencias:

Bash

pip install -r requirements.txt
⚠️ Configuración OBLIGATORIA para Traducción de Audio del Sistema ⚠️
Para traducir el audio de tu juego (y no tu voz), la aplicación necesita "escuchar" la salida de audio de tu PC. Dispositivos como "Mezcla estéreo" (Stereo Mix) a veces fallan o no existen (especialmente en portátiles o con auriculares USB como HyperX).

La solución más robusta es usar un cable de audio virtual.

## Pasos de Configuración con VB-CABLE
Instalar VB-CABLE:

Descarga e instala VB-CABLE Virtual Audio Device (es gratuito).

Reinicia tu PC si es necesario.

Configurar Salida de Windows:

Haz clic derecho en el ícono de altavoz 🔊 de Windows -> Sonidos.

Ve a la pestaña "Reproducción".

Establece CABLE Input (el dispositivo virtual) como tu dispositivo predeterminado.

En este punto, dejarás de escuchar el audio de tu PC. Es normal.

Configurar "Escuchar" (Para que tú oigas):

En la misma ventana de "Sonidos", ve a la pestaña "Grabar".

Busca CABLE Output -> clic derecho -> Propiedades.

Ve a la pestaña "Escuchar".

Marca la casilla "Escuchar este dispositivo".

En el menú "Reproducir a través de este dispositivo", selecciona tus audífonos o altavoces reales (ej: "Altavoces (HyperX)").

Pulsa "Aplicar". Ahora deberías volver a escuchar el audio de tu PC.

Configurar el TraductorOCR:

Inicia la aplicación.

En el panel "Traductor de Audio", selecciona CABLE Output como tu dispositivo.

Inicia la captura.

¡Listo! Ahora la aplicación y tus audífonos están "escuchando" la misma señal de audio, permitiendo la traducción en vivo.


## Estructura del Proyecto

TraductorOCRGame/
│
├── src/
│    └── traductorocr/
│       ├── core/         # Lógica de audio y OCR (translator.py, audio_translator.py)
│       ├── ui/           # Diseño de la UI (design.py, ocr_tuner.py)
│       └── utils/        # Gestión de rutas y modelos (paths.py, voice_models.py)
│       └── __main__.py   # Punto de entrada
│
├── resources/            # Fuente 'pearl.ttf'
├── vosk-model-small-en-us/ # Modelo de reconocimiento de voz
├── setup.py              # Configuración del paquete
├── requirements.txt      # Dependencias
└── README.md             # Este archivo