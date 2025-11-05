
import os
import sys
import tkinter as tk
import ttkbootstrap as ttk 
import pytesseract

from traductorocr.ui.design import TranslatorUI
from traductorocr.core.translator import TranslatorLogic
from traductorocr.core.config import *
from traductorocr.utils.paths import resource_path

def setup_environment() -> str:

    from traductorocr.utils.voice_models import download_vosk_model
    download_vosk_model()

    if getattr(sys, 'frozen', False):
        tesseract_path = resource_path('Tesseract-OCR')
        pytesseract.pytesseract.tesseract_cmd = os.path.join(tesseract_path, 'tesseract.exe')
        os.environ['TESSDATA_PREFIX'] = os.path.join(tesseract_path, 'tessdata')
        
        font_path = resource_path(os.path.join('resources', FONT_FILENAME))
        if not os.path.exists(font_path):
            messagebox.showerror("Error", f"No se encontró el archivo de fuente: {FONT_FILENAME}")
            font_path = None
    else:
        font_path = os.path.join('resources', FONT_FILENAME)
        if not os.path.exists(font_path):
            print(f"Advertencia: No se encontró {FONT_FILENAME}. Usando fuente por defecto.")
            font_path = None
    
    return font_path

def main() -> None:
    font_path = setup_environment()
    
    root = ttk.Window(themename="litera") 
    root.title("Traductor OCR")
    root.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")
    root.resizable(False, False) 
    
    ui = TranslatorUI(root, font_path)
    TranslatorLogic(ui)
    root.mainloop()

if __name__ == "__main__":
    main()