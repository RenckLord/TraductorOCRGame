
import os
import sys
import tkinter as tk
from tkinter import messagebox

import pytesseract

from traductorocr.ui.design import TranslatorUI
from traductorocr.core.translator import TranslatorLogic
from traductorocr.core.config import *
from traductorocr.utils.paths import resource_path

def setup_environment() -> str:
    """
    Configura el entorno de la aplicación.

    Returns:
        str: Ruta a la fuente personalizada o None si no se encuentra
    """
    if getattr(sys, 'frozen', False):
        # Configurar Tesseract para aplicación congelada
        tesseract_path = resource_path('Tesseract-OCR')
        pytesseract.pytesseract.tesseract_cmd = os.path.join(tesseract_path, 'tesseract.exe')
        os.environ['TESSDATA_PREFIX'] = os.path.join(tesseract_path, 'tessdata')
        
        # Configurar fuente para aplicación congelada
        font_path = resource_path(os.path.join('resources', FONT_FILENAME))
        if not os.path.exists(font_path):
            messagebox.showerror("Error", f"No se encontró el archivo de fuente: {FONT_FILENAME}")
            font_path = None
    else:
        # Configurar fuente para desarrollo
        font_path = os.path.join('resources', FONT_FILENAME)
        if not os.path.exists(font_path):
            print(f"Advertencia: No se encontró {FONT_FILENAME}. Usando fuente por defecto.")
            font_path = None
    
    return font_path

def main() -> None:
    font_path = setup_environment()
    
    root = tk.Tk()
    root.title("Traductor OCR")
    root.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")
    
    ui = TranslatorUI(root, font_path)
    TranslatorLogic(ui)
    root.mainloop()

if __name__ == "__main__":
    main()