"""
Diseño de la interfaz de usuario
"""
import tkinter as tk
from tkinter import font as tkFont, ttk, Text, colorchooser

from traductorocr.core.config import (
    DEFAULT_TEXT_COLOR,
    DEFAULT_BG_COLOR,
    DEFAULT_FONT_SIZE,
    POPUP_WRAP_LENGTH,
    DEFAULT_MIN_HEIGHT,
    DEFAULT_EXPANDED_HEIGHT
)

class TranslatorUI:
    def __init__(self, root: tk.Tk, custom_font_path: str = None):
        """
        Inicializa la interfaz de usuario.

        Args:
            root (tk.Tk): Ventana raíz de Tkinter
            custom_font_path (str, optional): Ruta a la fuente personalizada
        """
        self.root = root
        style = ttk.Style(self.root)
        style.theme_use('clam')

        self.setup_fonts(custom_font_path)
        self.setup_window()
        self.create_widgets()
        self.is_expanded = False

    def setup_fonts(self, custom_font_path: str) -> None:
        """Configura las fuentes de la aplicación"""
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.custom_font_object = self.default_font
        
        if custom_font_path:
            try:
                self.custom_font_object = tkFont.Font(
                    family="Pearl", 
                    size=DEFAULT_FONT_SIZE, 
                    weight="bold"
                )
            except Exception as e:
                print(f"Error al cargar la fuente: {e}")
                self.custom_font_object = self.default_font

        self.arrow_font = tkFont.Font(family='Pearl', size=8)

    def setup_window(self) -> None:
        """Configura las propiedades de la ventana"""
        self.root.geometry("350x300")
        self.root.wm_attributes("-topmost", True)
        self.root.attributes("-alpha", 1.0)
        
        self.text_color = DEFAULT_TEXT_COLOR
        self.popup_bg_color = DEFAULT_BG_COLOR
        self.last_popup_req_height = 50

    def create_widgets(self) -> None:
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Controles y ajustes
        self.create_controls()
        self.create_settings()
        self.create_result_area()
        self.create_expand_button()
        self.create_inverse_frame()
        
        # Aplicar estilo al botón de captura
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Pearl', 10))

    def create_controls(self) -> None:
        """Crea los controles principales"""
        self.controls_frame = ttk.Frame(self.main_frame)
        self.controls_frame.pack(fill="x", pady=5)
        
        self.capture_button = ttk.Button(
            self.controls_frame,
            text="Seleccionar Zona y Traducir (EN -> ES)",
            style='Accent.TButton'
        )
        self.capture_button.pack(fill="x", ipady=5)
        
        self.progressbar = ttk.Progressbar(
            self.controls_frame,
            mode='indeterminate'
        )

    def create_settings(self) -> None:
        """Crea el panel de ajustes"""
        self.settings_frame = ttk.LabelFrame(
            self.main_frame,
            text="Ajustes",
            padding=(5, 5)
        )
        self.settings_frame.pack(fill="x", pady=5)
        
        # Control de transparencia
        ttk.Label(
            self.settings_frame,
            text="Transparencia Ventana:"
        ).grid(row=0, column=0, sticky="w")
        
        self.alpha_slider = ttk.Scale(
            self.settings_frame,
            from_=0.1,
            to=1.0,
            orient=tk.HORIZONTAL
        )
        self.alpha_slider.set(1.0)
        self.alpha_slider.grid(row=0, column=1, sticky="ew")
        
        # Control de color
        self.color_button = ttk.Button(
            self.settings_frame,
            text="Color Texto"
        )
        self.color_button.grid(row=0, column=2, padx=(10, 0))
        
        self.settings_frame.columnconfigure(1, weight=1)

    def create_result_area(self) -> None:
        """Crea el área de resultados"""
        self.result_frame = ttk.Frame(
            self.main_frame,
            style='Result.TFrame'
        )
        self.result_frame.pack(fill="both", expand=True, pady=5)
        
        self.result_text = Text(
            self.result_frame,
            font=self.custom_font_object,
            fg=self.text_color,
            bg=self.popup_bg_color,
            wrap=tk.WORD,
            padx=10,
            pady=10,
            relief=tk.FLAT,
            state='disabled',
            height=4
        )
        self.result_text.pack(fill="both", expand=True)

    # Métodos públicos para la lógica
    def disable_controls(self) -> None:
        """Deshabilita los controles durante el procesamiento"""
        self.capture_button.state(['disabled'])
        self.color_button.state(['disabled'])
        self.progressbar.start()
        self.progressbar.pack(fill="x", pady=5)

    def enable_controls(self) -> None:
        """Habilita los controles después del procesamiento"""
        self.capture_button.state(['!disabled'])
        self.color_button.state(['!disabled'])
        self.progressbar.stop()
        self.progressbar.pack_forget()

    def update_result(self, text: str) -> None:
        """Actualiza el texto del resultado"""
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', text)
        self.result_text.config(state='disabled')

    def show_loading(self, message: str) -> None:
        """Muestra mensaje de carga"""
        self.update_result(message)

    def get_inverse_text(self) -> str:
        """Obtiene el texto a traducir inversamente"""
        return self.inverse_entry.get()

    def create_expand_button(self) -> None:
        """Crea el botón para expandir/contraer la traducción inversa"""
        self.expand_button = ttk.Button(
            self.main_frame,
            text="Traductor Manual (ES -> EN) ▼",
            style="Link.TButton"
        )
        self.expand_button.pack(fill="x", pady=(5, 0))

        # Estilo para botón tipo link
        style = ttk.Style()
        style.configure("Link.TButton", font=("Pearl", 8))

    def create_inverse_frame(self) -> None:
        """Crea el panel de traducción inversa"""
        self.inverse_frame = ttk.Frame(self.main_frame)
        
        ttk.Label(
            self.inverse_frame,
            text="Escribe en Español:",
            font=self.custom_font_object
        ).pack(fill="x", pady=(5, 2))
        
        self.inverse_entry = ttk.Entry(
            self.inverse_frame,
            font=self.custom_font_object
        )
        self.inverse_entry.pack(fill="x", pady=2)
        
        self.inverse_button = ttk.Button(
            self.inverse_frame,
            text="Traducir a Inglés",
            style="Accent.TButton"
        )
        self.inverse_button.pack(fill="x", pady=5)
        
        ttk.Label(
            self.inverse_frame,
            text="Resultado en Inglés:",
            font=self.custom_font_object
        ).pack(fill="x", pady=(5, 2))
        
        self.inverse_result_text = Text(
            self.inverse_frame,
            font=self.custom_font_object,
            
            fg=self.text_color,
            bg=self.popup_bg_color,
            wrap=tk.WORD,
            height=4,
            relief=tk.FLAT
        )
        self.inverse_result_text.pack(fill="both", expand=True)

    def show_inverse_result(self, text: str) -> None:
        """Muestra el resultado de la traducción inversa"""
        self.inverse_result_text.config(state='normal')
        self.inverse_result_text.delete('1.0', tk.END)
        self.inverse_result_text.insert('1.0', text)
        self.inverse_result_text.config(state='disabled')

    def get_inverse_text(self) -> str:
        """Obtiene el texto para traducción inversa"""
        return self.inverse_entry.get()

    def toggle_expand(self) -> None:
        """Alterna entre mostrar/ocultar el panel de traducción inversa"""
        if self.is_expanded:
            self.inverse_frame.pack_forget()
            self.root.geometry(f"350x{DEFAULT_MIN_HEIGHT}")
            self.expand_button.config(text="Traductor Manual (ES -> EN) ▼")
            self.is_expanded = False
        else:
            self.root.geometry(f"350x{DEFAULT_EXPANDED_HEIGHT}")
            self.inverse_frame.pack(fill="both", expand=True, pady=5)
            self.expand_button.config(text="Ocultar Traductor Manual ▲")
            self.is_expanded = True