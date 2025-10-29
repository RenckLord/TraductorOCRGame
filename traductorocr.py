

import sys
import tkinter as tk
from tkinter import scrolledtext, font as tkFont 
from mss import mss, tools
from deep_translator import GoogleTranslator
import cv2
import numpy as np
import pytesseract 

# --- CONFIGURACIÓN ---
TARGET_LANGUAGE = 'es'   
INVERSE_TARGET_LANGUAGE = 'en' 
THRESHOLD_VALUE = 80  


class AreaSelector:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)
        self.root.attributes("-topmost", True)
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.selection_box = None
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_mouse_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        self.selection_box = (
            min(self.start_x, end_x), min(self.start_y, end_y),
            abs(self.start_x - end_x), abs(self.start_y - end_y)
        )
        self.root.destroy()

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Traductor OCR")
        self.root.geometry("350x450") 
        self.root.wm_attributes("-topmost", True)
        
        self.is_expanded = False 
        self.min_height = 450
        self.expanded_height = 600 


        print("Motor Tesseract listo.")

        self.ocr_frame = tk.Frame(self.root)
        self.ocr_frame.pack(fill="x", padx=10, pady=5)
        
        self.capture_button = tk.Button(self.ocr_frame, text="Seleccionar Zona y Traducir (EN -> ES)", command=self.start_capture_process)
        self.capture_button.pack(fill="x")

        self.text_output = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=20, font=("Arial", 10), bg="white", fg="black")
        self.text_output.pack(pady=5, padx=10, fill="both", expand=True)
        self.text_output.config(state='disabled')

        # --- BOTÓN PARA EXPANDIR ---
        arrow_font = tkFont.Font(family='Arial', size=8)
        self.expand_button = tk.Button(self.root, text="Traductor Manual (ES -> EN) ▼", font=arrow_font, command=self.toggle_expand)
        self.expand_button.pack(fill="x", padx=10, pady=(0, 5))

        # --- SECCIÓN INFERIOR  ---
        self.inverse_frame = tk.Frame(self.root)
        
        tk.Label(self.inverse_frame, text="Escribe en Español:").pack(fill="x", padx=5)
        
        self.inverse_entry = tk.Entry(self.inverse_frame, font=("Arial", 10))
        self.inverse_entry.pack(fill="x", padx=5, pady=2)
        
        self.inverse_button = tk.Button(self.inverse_frame, text="Traducir a Inglés", command=self.run_inverse_translation)
        self.inverse_button.pack(fill="x", padx=5, pady=5)
        
        tk.Label(self.inverse_frame, text="Resultado en Inglés:").pack(fill="x", padx=5)
        
        self.inverse_result_label = tk.Label(self.inverse_frame, text="", font=("Arial", 10, "bold"), bg="white", fg="black", anchor="w", justify="left", wraplength=330)
        self.inverse_result_label.pack(fill="x", padx=5, pady=2)
        
    def toggle_expand(self):
        """Muestra u oculta la sección de traducción inversa."""
        if self.is_expanded:
            self.inverse_frame.pack_forget()
            self.root.geometry(f"350x{self.min_height}")
            self.expand_button.config(text="Traductor Manual (ES -> EN) ▼")
            self.is_expanded = False
        else:
            self.root.geometry(f"350x{self.expanded_height}")
            self.inverse_frame.pack(fill="both", expand=True, padx=10, pady=5)
            self.expand_button.config(text="Ocultar Traductor Manual ▲")
            self.is_expanded = True
            
    def run_inverse_translation(self):
        """Toma el texto del Entry y lo traduce a inglés."""
        text_to_translate = self.inverse_entry.get()
        if not text_to_translate:
            self.inverse_result_label.config(text="Escribe algo primero.")
            return
            
        try:
            print("Traduciendo de ES a EN...")
            translated_text = GoogleTranslator(source='auto', target=INVERSE_TARGET_LANGUAGE).translate(text_to_translate)
            print(f"Resultado: {translated_text}")
            self.inverse_result_label.config(text=translated_text)
            
        except Exception as e:
            error_msg = f"Error de traducción: {e}"
            print(error_msg)
            self.inverse_result_label.config(text=error_msg)

    def start_capture_process(self):
        self.root.withdraw()
        selector_root = tk.Toplevel(self.root)
        app = AreaSelector(selector_root)
        selector_root.wait_window()
        box = app.selection_box
        self.root.deiconify()
        if box:
            self.run_ocr_and_translate(box)

    def run_ocr_and_translate(self, box):
        """Función de OCR (Inglés -> Español)"""
        if not box or box[2] == 0 or box[3] == 0:
            print("No se seleccionó área.")
            return

        try:
            monitor = {"top": int(box[1]), "left": int(box[0]), "width": int(box[2]), "height": int(box[3])}
            
            with mss() as sct:
                sct_img = sct.grab(monitor)

            # --- PRE-PROCESAMIENTO ---
            img_np = np.array(sct_img)
            gray_img = cv2.cvtColor(img_np, cv2.COLOR_BGRA2GRAY)
            _ , processed_img = cv2.threshold(gray_img, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
            
            cv2.imwrite("debug_image.png", processed_img)

            print("Realizando OCR (Tesseract) sobre la imagen procesada...")
            text_from_ocr = pytesseract.image_to_string(processed_img, lang='eng')
            results = text_from_ocr.split('\n')
            # ------------------------------------
            
            if not results:
                print("No se detectó texto.")
                self.update_text_output("No se detectó texto.")
                return
                
            print(f"Texto detectado (lista): {results}")

            print("Traduciendo (EN -> ES)...")
            
            # Filtramos líneas vacías que Tesseract a veces crea
            cleaned_results = [line for line in results if line.strip()]
            text_to_translate = "\n".join(cleaned_results)
            
            if not text_to_translate:
                print("No se detectó texto útil.")
                self.update_text_output("No se detectó texto útil.")
                return

            translator = GoogleTranslator(source='auto', target=TARGET_LANGUAGE)
            final_text = translator.translate(text_to_translate)

            print(f"Traducción final:\n{final_text}")
            
            # 7. Mostrar resultado en la GUI
            self.update_text_output(final_text)
            
        except Exception as e:
            error_msg = f"Ocurrió un error: {e}"
            print(error_msg)
            self.update_text_output(error_msg)

    def update_text_output(self, text):
        """Actualiza el cuadro de texto principal del OCR."""
        self.text_output.config(state='normal')
        self.text_output.delete('1.0', tk.END)
        self.text_output.insert(tk.END, text)
        self.text_output.config(state='disabled')
    
if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()