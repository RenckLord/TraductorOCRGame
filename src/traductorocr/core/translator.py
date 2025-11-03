"""
Lógica principal del traductor
"""
import tkinter as tk
import threading
from mss import mss
import numpy as np
import cv2
import pytesseract
from deep_translator import GoogleTranslator

from traductorocr.ui.area_selector import AreaSelector
from traductorocr.core.config import TARGET_LANGUAGE, INVERSE_TARGET_LANGUAGE, THRESHOLD_VALUE
from traductorocr.core.audio_translator import AudioTranslator

class TranslatorLogic:
    def __init__(self, ui):
        self.ui = ui
        self.audio_translator = AudioTranslator(
            on_translation=self._on_audio_translation,
            on_error=self._on_audio_error
        )
        self.is_capturing_audio = False
        self.selected_device_id = None
        self.setup_bindings()

    def setup_bindings(self):
        """Configura los enlaces de eventos"""
        self.ui.capture_button.config(command=self.start_capture_process)
        self.ui.alpha_slider.config(command=self.update_transparency)
        self.ui.color_button.config(command=self.change_text_color)
        self.ui.expand_button.config(command=self.ui.toggle_expand)
        self.ui.inverse_button.config(command=self.run_inverse_translation)
        self.ui.audio_capture_button.config(command=self.toggle_audio_capture)
        self.ui.device_selector.bind('<<ComboboxSelected>>', self._on_device_selected)

    def start_capture_process(self):
        """Inicia el proceso de captura de área"""
        self.ui.root.withdraw()
        selector_root = tk.Toplevel(self.ui.root)
        app = AreaSelector(selector_root)
        selector_root.wait_window()
        box = app.selection_box
        self.ui.root.deiconify()
        if box:
            self.run_ocr_thread(box)

    def run_ocr_thread(self, box):
        """Ejecuta el OCR en un hilo separado"""
        self.ui.disable_controls()
        self.ui.show_loading("Traduciendo...")
        threading.Thread(target=self.ocr_task, args=(box,), daemon=True).start()

    def ocr_task(self, box):
        """Realiza el OCR y la traducción"""
        result_message = ""
        try:
            # Capturar y procesar imagen
            monitor = {
                "top": int(box[1]), 
                "left": int(box[0]), 
                "width": int(box[2]), 
                "height": int(box[3])
            }
            with mss() as sct:
                sct_img = sct.grab(monitor)
            
            # Procesar imagen
            img_np = np.array(sct_img)
            gray_img = cv2.cvtColor(img_np, cv2.COLOR_BGRA2GRAY)
            _, processed_img = cv2.threshold(gray_img, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
            
            # OCR
            text_from_ocr = pytesseract.image_to_string(processed_img, lang='eng')
            results = text_from_ocr.split('\n')
            
            if not results:
                result_message = "No se detectó texto."
            else:
                # Limpiar y traducir resultados
                cleaned_results = [line for line in results if line.strip()]
                text_to_translate = "\n".join(cleaned_results)
                
                if not text_to_translate:
                    result_message = "No se detectó texto útil."
                else:
                    # Traducir
                    translator = GoogleTranslator(source='en', target=TARGET_LANGUAGE)
                    result_message = translator.translate(text_to_translate)
        except Exception as e:
            result_message = f"Error: {e}"
        
        self.ui.root.after(0, self.finish_ocr, result_message)

    def finish_ocr(self, result):
        """Finaliza el proceso de OCR actualizando la UI"""
        self.ui.enable_controls()
        self.ui.update_result(result)

    def update_transparency(self, value):
        """Actualiza la transparencia de la ventana"""
        self.ui.root.attributes("-alpha", float(value))

    def change_text_color(self):
        """Cambia el color del texto"""
        from tkinter import colorchooser
        color_code = colorchooser.askcolor(title="Elige un color de texto", initialcolor=self.ui.text_color)
        if color_code[1]:
            self.ui.text_color = color_code[1]
            self.ui.result_text.config(fg=self.ui.text_color)
            self.ui.inverse_result_text.config(fg=self.ui.text_color)
            
    def run_inverse_translation(self):
        """Inicia el proceso de traducción inversa"""
        text_to_translate = self.ui.get_inverse_text()
        if not text_to_translate:
            self.ui.show_inverse_result("Escribe algo primero.")
            return
        
        threading.Thread(
            target=self._inverse_translate_task,
            args=(text_to_translate,),
            daemon=True
        ).start()

    def _inverse_translate_task(self, text):
        try:
            translator = GoogleTranslator(source='es', target=INVERSE_TARGET_LANGUAGE)
            translated_text = translator.translate(text)
            self.ui.root.after(0, self.ui.show_inverse_result, translated_text)
        except Exception as e:
            error_msg = f"Error: {e}"
            self.ui.root.after(0, self.ui.show_inverse_result, error_msg)
            
    def _on_device_selected(self, event=None):
        """Maneja la selección de un nuevo dispositivo de audio"""
        device_id = self.ui.get_selected_device_id()
        if device_id is not None:
            print(f"Dispositivo seleccionado: {device_id}")
            self.selected_device_id = device_id
            self.audio_translator.set_audio_device(device_id)
            
    def toggle_audio_capture(self):
        """Alterna entre iniciar/detener la captura de audio"""
        if not self.selected_device_id:
            self.ui.audio_status_value.config(text="Inactivo - Seleccione un dispositivo")
            return
            
        if self.is_capturing_audio:
            self.audio_translator.stop_capture()
            self.is_capturing_audio = False
            self.ui.audio_capture_button.config(text="Iniciar Captura de Audio")
            self.ui.audio_status_value.config(text="Inactivo", foreground="red")
        else:
            try:
                self.audio_translator.start_capture()
                self.is_capturing_audio = True
                self.ui.audio_capture_button.config(text="Detener Captura")
                self.ui.audio_status_value.config(text="Capturando...", foreground="green")
            except Exception as e:
                self.ui.audio_status_value.config(text=f"Error: {str(e)}", foreground="red")
            
    def _on_audio_translation(self, translation):
        """Callback para cuando hay una nueva traducción de audio"""
        self.ui.subtitles_text.config(state='normal')
        self.ui.subtitles_text.delete('1.0', 'end')
        self.ui.subtitles_text.insert('1.0', translation)
        self.ui.subtitles_text.config(state='disabled')
        
    def _on_audio_error(self, error):
        """Callback para cuando hay un error en la traducción de audio"""
        self.ui.audio_status_label.config(text=f"Error: {error}")