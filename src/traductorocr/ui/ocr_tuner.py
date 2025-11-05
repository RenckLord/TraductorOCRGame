# src/traductorocr/ui/ocr_tuner.py
"""
Módulo para la ventana emergente de ajuste de OCR (Tuner).
"""
import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk

class OcrTuner:
    def __init__(self, parent, sample_image: np.ndarray, initial_threshold: int, initial_invert: bool):

        self.parent = parent
        self.original_image = sample_image
        
        # Variables para guardar los ajustes
        self.threshold_var = tk.IntVar(value=initial_threshold)
        self.invert_var = tk.BooleanVar(value=initial_invert)
        
        # Variable para almacenar el resultado final
        self.result = {
            "threshold": initial_threshold,
            "invert": initial_invert
        }
        
        # Crear la ventana Toplevel (emergente)
        self.window = tk.Toplevel(parent)
        self.window.title("Ajustar Previsualización de OCR")
        self.window.attributes("-topmost", True)
        
        # --- Crear Widgets ---
        self.main_frame = ttk.Frame(self.window, padding=10)
        self.main_frame.pack(fill="both", expand=True)
        
        # Frame para la imagen
        self.image_frame = ttk.LabelFrame(self.main_frame, text="Previsualización")
        self.image_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(fill="both", expand=True)
        
        # Frame para los controles
        self.controls_frame = ttk.LabelFrame(self.main_frame, text="Controles")
        self.controls_frame.pack(side="right", fill="y")
        
        self._create_controls()
        
        # Actualizar la previsualización inicial
        self._update_preview()

    def _create_controls(self):
        """Crea los sliders y checkboxes de control."""
        # Slider de Umbral (Threshold)
        ttk.Label(self.controls_frame, text="Umbral (Threshold):").pack(pady=5)
        
        self.threshold_slider = ttk.Scale(
            self.controls_frame,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            variable=self.threshold_var,
            command=lambda v: self._update_preview() # Actualiza al mover
        )
        self.threshold_slider.pack(fill="x", padx=10)
        
        # Checkbox de Invertir
        self.invert_check = ttk.Checkbutton(
            self.controls_frame,
            text="Invertir (Texto oscuro sobre fondo claro)",
            variable=self.invert_var,
            command=self._update_preview # Actualiza al marcar
        )
        self.invert_check.pack(pady=10, fill="x")
        
        # Botón de Guardar
        self.save_button = ttk.Button(
            self.controls_frame,
            text="Guardar y Cerrar",
            command=self._on_save
        )
        self.save_button.pack(pady=20, fill="x")

    def _update_preview(self):
        """Aplica los filtros a la imagen original y actualiza el label."""
        try:
            # 1. Obtener valores actuales de los controles
            threshold = self.threshold_var.get()
            invert = self.invert_var.get()
            
            # 2. Determinar el modo de OpenCV
            # Si "invert" es True, usamos THRESH_BINARY_INV (para texto oscuro)
            # Si es False, usamos THRESH_BINARY (para texto claro)
            thresh_mode = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
            
            # 3. Aplicar el filtro a la imagen original
            # (Asegurarse de que esté en escala de grises si no lo está)
            if len(self.original_image.shape) == 3:
                gray_img = cv2.cvtColor(self.original_image, cv2.COLOR_BGRA2GRAY)
            else:
                gray_img = self.original_image
                
            _, processed_img = cv2.threshold(gray_img, threshold, 255, thresh_mode)
            
            # 4. Convertir la imagen de OpenCV (np.ndarray) a una imagen de Tkinter
            img_pil = Image.fromarray(processed_img)
            
            # Redimensionar si es muy grande para la ventana (opcional pero bueno)
            max_size = (400, 300)
            img_pil.thumbnail(max_size, Image.LANCZOS)
            
            img_tk = ImageTk.PhotoImage(image=img_pil)
            
            # 5. Actualizar el label
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk # Guardar referencia para evitar el garbage collector
            
        except Exception as e:
            print(f"Error actualizando previsualización: {e}")

    def _on_save(self):
        """Guarda los valores seleccionados y cierra la ventana."""
        self.result["threshold"] = self.threshold_var.get()
        self.result["invert"] = self.invert_var.get()
        self.window.destroy()

    def show(self):
        """Muestra la ventana y espera hasta que se cierre."""
        # 'transient' la pone sobre la ventana padre
        self.window.transient(self.parent)
        # 'grab_set' bloquea la interacción con la ventana principal
        self.window.grab_set()
        # 'wait_window' espera hasta que self.window.destroy() sea llamada
        self.parent.wait_window(self.window)
        # Devuelve el resultado después de que la ventana se cierra
        return self.result