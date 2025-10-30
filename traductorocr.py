import os
import sys
import tkinter as tk
from tkinter import messagebox
import pytesseract
from ui_design import TranslatorUI
from translator_logic import TranslatorLogic
from config import *
import utils

def setup_environment():
    """Configura el entorno de la aplicación"""
    if getattr(sys, 'frozen', False):
        # Configurar Tesseract para aplicación congelada
        tesseract_path = utils.resource_path('Tesseract-OCR')
        pytesseract.pytesseract.tesseract_cmd = os.path.join(tesseract_path, 'tesseract.exe')
        os.environ['TESSDATA_PREFIX'] = os.path.join(tesseract_path, 'tessdata')
        
        # Configurar fuente para aplicación congelada
        font_path = utils.resource_path(FONT_FILENAME)
        if not os.path.exists(font_path):
            messagebox.showerror("Error", f"No se encontró el archivo de fuente: {FONT_FILENAME}")
            font_path = None
    else:
        # Configurar fuente para desarrollo
        font_path = FONT_FILENAME if os.path.exists(FONT_FILENAME) else None
        if font_path is None:
            print(f"Advertencia: No se encontró {FONT_FILENAME}. Usando fuente por defecto.")
    
    return font_path

def main():
    """Función principal que inicia la aplicación"""
    font_path = setup_environment()
    
    root = tk.Tk()
    root.title("Traductor OCR")
    root.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")
    
    ui = TranslatorUI(root, font_path)
    TranslatorLogic(ui)
    root.mainloop()

if __name__ == "__main__":
    main()