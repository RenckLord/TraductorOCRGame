import cv2
import numpy as np
import pytesseract
from mss import mss
from deep_translator import GoogleTranslator
import tkinter as tk
from tkinter import colorchooser
import threading

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
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2
        )

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

class TranslatorLogic:
    def __init__(self, ui):
        self.ui = ui
        self.setup_bindings()

    def setup_bindings(self):
        self.ui.capture_button.configure(command=self.start_capture_process)
        self.ui.alpha_slider.configure(command=self.update_transparency)
        self.ui.color_button.configure(command=self.change_text_color)
        self.ui.inverse_button.configure(command=self.run_inverse_translation)

    def update_transparency(self, value):
        self.ui.root.attributes("-alpha", float(value))

    def change_text_color(self):
        color_code = colorchooser.askcolor(
            title="Elige un color de texto",
            initialcolor=self.ui.text_color
        )
        if color_code[1]:
            self.ui.text_color = color_code[1]
            self.ui.result_text.config(state='normal')
            self.ui.result_text.config(fg=self.ui.text_color)
            self.ui.result_text.config(state='disabled')
            self.ui.inverse_result_label.config(fg=self.ui.text_color)

# Removed toggle_expand as it's no longer needed

    def start_capture_process(self):
        self.ui.root.withdraw()
        selector_root = tk.Toplevel(self.ui.root)
        app = AreaSelector(selector_root)
        selector_root.wait_window()
        box = app.selection_box
        self.ui.root.deiconify()
        if box:
            self.run_ocr_thread(box)

    def run_ocr_thread(self, box):
        # Deshabilitar controles durante la traducción
        self.ui.capture_button.config(state="disabled")
        self.ui.color_button.config(state="disabled")
        self.ui.inverse_button.config(state="disabled")
        
        # Mostrar estado
        self.update_result_text("Traduciendo...")
        self.ui.root.update_idletasks()
        
        # Mostrar barra de progreso
        self.ui.progressbar.pack(pady=(0,5), padx=10, fill='x', before=self.ui.result_frame)
        self.ui.progressbar.start()
        
        # Iniciar proceso de OCR en un hilo separado
        threading.Thread(target=self.ocr_task, args=(box,), daemon=True).start()

    def ocr_task(self, box):
        result_message = ""
        try:
            monitor = {
                "top": int(box[1]),
                "left": int(box[0]),
                "width": int(box[2]),
                "height": int(box[3])
            }
            with mss() as sct:
                sct_img = sct.grab(monitor)
            img_np = np.array(sct_img)
            gray_img = cv2.cvtColor(img_np, cv2.COLOR_BGRA2GRAY)
            _ , processed_img = cv2.threshold(gray_img, 80, 255, cv2.THRESH_BINARY)
            
            text_from_ocr = pytesseract.image_to_string(processed_img, lang='eng')
            results = text_from_ocr.split('\n')
            
            if not results:
                result_message = "No se detectó texto."
            else:
                cleaned_results = [line for line in results if line.strip()]
                text_to_translate = "\n".join(cleaned_results)
                if not text_to_translate:
                    result_message = "No se detectó texto útil."
                else:
                    translator = GoogleTranslator(source='en', target='es')
                    result_message = translator.translate(text_to_translate)
        except Exception as e:
            result_message = f"Error: {e}"
            
        self.ui.root.after(0, self.finish_ocr, result_message)

    def finish_ocr(self, result):
        # Detener y ocultar la barra de progreso
        self.ui.progressbar.stop()
        self.ui.progressbar.pack_forget()
        
        # Re-habilitar controles
        self.ui.capture_button.config(state="normal")
        self.ui.color_button.config(state="normal")
        self.ui.inverse_button.config(state="normal")
        
        # Mostrar resultado
        self.update_result_text(result)
        self.ui.root.update_idletasks()

    def update_result_text(self, text):
        self.ui.result_text.config(state='normal')    
        self.ui.result_text.delete('1.0', tk.END)     
        self.ui.result_text.insert('1.0', text)
        self.ui.result_text.config(wrap=tk.WORD)
        self.ui.result_text.config(state='disabled')

    def run_inverse_translation(self):
        text_to_translate = self.ui.inverse_entry.get()
        if not text_to_translate:
            self.ui.inverse_result_label.config(text="Escribe algo primero.")
            return
        threading.Thread(
            target=self._inverse_translate_task,
            args=(text_to_translate,),
            daemon=True
        ).start()

    def _inverse_translate_task(self, text):
        try:
            translated_text = GoogleTranslator(source='es', target='en').translate(text)
            self.ui.root.after(
                0,
                lambda: self.ui.inverse_result_label.configure(text=translated_text)
            )
        except Exception as e:
            error_msg = f"Error: {e}"
            self.ui.root.after(
                0,
                lambda: self.ui.inverse_result_label.configure(text=error_msg)
            )