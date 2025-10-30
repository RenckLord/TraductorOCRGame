# Traductor OCR para Juegos

Un traductor en tiempo real construido con Python y Tesseract que permite seleccionar un área de la pantalla (en un juego) y traduce el texto de inglés a español.

## Características

- Captura de pantalla y OCR con Tesseract y OpenCV
- Traducción usando Google Translate
- Interfaz gráfica construida con Tkinter
- Función de traductor inverso (Español a Inglés)
- Personalización de colores y transparencia
- Modo siempre visible

## Requisitos

- Python 3.8 o superior
- Tesseract OCR (solo Windows)

## Instalación

### Desarrollo

1. Clona el repositorio:
   ```bash
   git clone https://github.com/RenckLord/TraductorOCRGame.git
   cd TraductorOCRGame
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```

3. Instala el paquete en modo desarrollo:
   ```bash
   pip install -e .
   ```

4. Instala Tesseract OCR (solo Windows):
   - Descarga el instalador desde [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - Ejecuta el instalador y sigue las instrucciones

### Usuario Final

1. Descarga el último release desde la [página de releases](https://github.com/RenckLord/TraductorOCRGame/releases)
2. Ejecuta el instalador y sigue las instrucciones

## Uso

1. Inicia la aplicación:
   ```bash
   traductorocr
   ```
   
2. Haz clic en "Seleccionar Zona y Traducir"
3. Selecciona el área de la pantalla con texto en inglés
4. La traducción aparecerá automáticamente

## Estructura del Proyecto

```
TraductorOCRGame/
│
├── src/
│   └── traductorocr/
│       ├── core/           # Lógica principal
│       ├── ui/            # Interfaz de usuario
│       └── utils/         # Utilidades
│
├── resources/             # Recursos (fuentes, etc.)
├── tests/                # Tests unitarios
├── setup.py              # Configuración del paquete
└── README.md            # Este archivo
```

## Contribuir

1. Haz un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.