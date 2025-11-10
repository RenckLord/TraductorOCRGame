## TraductorOCRGame v3.0 

> Herramienta de escritorio para Windows que ofrece traducción en tiempo real de texto (OCR) y audio (Voz) en tus juegos.

TraductorOCRGame combina un potente motor de OCR con el reconocimiento de voz de Vosk y `deep-translator` para romper las barreras del idioma en tus juegos.

---

## Características Principales

#### 1. Traductor de OCR (EN -> ES)
* **Selección de Área:** Captura cualquier texto en tu pantalla con un simple clic y arrastre.
* **Ajuste de Previsualización (Ajustar OCR):** ¿Texto claro sobre fondo oscuro? ¿Oscuro sobre fondo claro? Un afinador visual te permite ajustar el umbral (threshold) y la inversión de la imagen, garantizando la máxima precisión en cualquier situación.
* **Traductor Manual (ES -> EN):** Un panel desplegable para traducciones rápidas de español a inglés.

#### 2. Traductor de Audio (EN -> ES)
* **Reconocimiento de Voz en Vivo:** Captura audio en inglés (micrófono o audio del sistema) usando el motor de Vosk.
* **Traducción Rápida:** Transcribe y traduce diálogos con pausas cortas, ideal para seguir cinemáticas, videos o streams.
* **Selector de Dispositivo:** Elige exactamente qué fuente de audio quieres traducir.

#### 3. Interfaz Moderna
* **Tema Oscuro:** Interfaz rediseñada con `ttkbootstrap` (tema "litera") para una apariencia limpia y profesional.
* **Siempre Visible:** La ventana se mantiene encima de tu juego para que no pierdas de vista la traducción.
* **Ajuste de Transparencia:** Configura la opacidad de la ventana para una integración perfecta.

---

## 📋 Requisitos

#### 🧑‍💻 Para Usuarios (EXE)
* Windows 10 / 11.
* (Opcional pero recomendado) [**VB-CABLE Virtual Audio Device**](https://vb-audio.com/Cable/) (para la traducción de audio del sistema).

#### 👩‍🔬 Para Desarrolladores
* Python 3.8+
* Tesseract OCR (instalado y en el PATH del sistema).
* Todas las dependencias listadas en `requirements.txt`.

---

## 📦 Instalación

#### 🧑‍💻 Para Usuarios
1.  Ve a la [**página de Releases**](https://github.com/RenckLord/TraductorOCRGame/releases) de este repositorio.
2.  Descarga el `TraductorOCR.exe` de la última versión.
3.  Ejecuta el archivo. (No requiere instalación).

#### 👩‍🔬 Para Desarrolladores
1.  Clona el repositorio:
    ```bash
    git clone [https://github.com/RenckLord/TraductorOCRGame.git](https://github.com/RenckLord/TraductorOCRGame.git)
    cd TraductorOCRGame
    ```
2.  (Recomendado) Instala Tesseract OCR desde [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki).
3.  Crea y activa un entorno virtual:
    ```bash
    python -m venv .venv
    .\.venv\Scripts\Activate
    ```
4.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
5.  Ejecuta la aplicación:
    ```bash
    python -m src.traductorocr
    ```

---

## ⚠️ Configuración OBLIGATORIA para Audio del Sistema ⚠️

> Para traducir el audio de tu juego (y no tu voz), la aplicación necesita "escuchar" la salida de audio de tu PC. Dispositivos como "Mezcla estéreo" (Stereo Mix) a veces fallan o no existen (especialmente en portátiles o con auriculares USB como HyperX).
>
> **La solución más robusta es usar un cable de audio virtual.**

### Pasos de Configuración con VB-CABLE

1.  **Instalar VB-CABLE:**
    * Descarga e instala [**VB-CABLE Virtual Audio Device**](https://vb-audio.com/Cable/) (es gratuito).
    * Reinicia tu PC si es necesario.

2.  **Configurar Salida de Windows (Audio del Juego):**
    * Haz clic derecho en el ícono de altavoz 🔊 de Windows -> **Sonidos**.
    * Ve a la pestaña **"Reproducción"**.
    * Establece **`CABLE Input`** (el dispositivo virtual) como tu **dispositivo predeterminado**.
    * *(En este punto, dejarás de escuchar el audio de tu PC. Es normal).*

3.  **Configurar "Escuchar" (Para que tú oigas):**
    * En la misma ventana de "Sonidos", ve a la pestaña **"Grabar"**.
    * Busca **`CABLE Output`** -> clic derecho -> **Propiedades**.
    * Ve a la pestaña **"Escuchar"**.
    * Marca la casilla **"Escuchar este dispositivo"**.
    * En el menú "Reproducir a través de este dispositivo", selecciona tus **audífonos o altavoces reales** (ej: "Altavoces (HyperX)").
    * Pulsa "Aplicar". *(Ahora deberías volver a escuchar el audio de tu PC).*

4.  **Configurar el TraductorOCR:**
    * Inicia la aplicación.
    * En el panel "Traductor de Audio", selecciona **`CABLE Output`** como tu dispositivo.
    * Inicia la captura.

¡Listo! Ahora la aplicación y tus audífonos están "escuchando" la misma señal de audio, permitiendo la traducción en vivo.

---

## 📂 Estructura del Proyecto

## Estructura del Proyecto
```
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
```