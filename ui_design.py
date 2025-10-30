import tkinter as tk
from tkinter import font as tkFont, ttk, Text

class TranslatorUI:
    def __init__(self, root, custom_font_path=None):
        self.root = root
        self.root.title("Traductor OCR")
        style = ttk.Style(self.root)
        style.theme_use('clam')

        self.setup_fonts(custom_font_path)
        self.setup_window()
        self.create_widgets()

    def setup_fonts(self, custom_font_path):
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.custom_font_object = self.default_font
        if custom_font_path:
            try:
                self.custom_font_object = tkFont.Font(family="Pearl", size=11, weight="bold")
            except:
                self.custom_font_object = self.default_font
        self.arrow_font = tkFont.Font(family='Arial', size=8)

    def setup_window(self):
        self.root.geometry("350x300")
        self.root.wm_attributes("-topmost", True)
        self.root.attributes("-alpha", 1.0)
        self.is_expanded = False
        self.min_height = 300
        self.expanded_height = 450
        self.text_color = "white"
        self.popup_bg_color = "#282c34"
        self.last_popup_req_height = 50

    def create_widgets(self):
        # Frame principal para organizar verticalmente
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Sección superior: controles OCR y ajustes
        self.create_controls()
        self.create_settings()
        
        # Aplicar estilo al botón de captura
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Arial', 10))
        
        # Área de texto traducido
        self.result_frame = tk.Frame(
            self.main_frame,
            bg=self.popup_bg_color,
            bd=0,
            highlightthickness=0
        )
        self.result_frame.pack(fill="both", expand=True, pady=(10,5))
        
        self.result_text = Text(
            self.result_frame,
            font=self.custom_font_object,
            fg=self.text_color,
            bg=self.popup_bg_color,
            wrap=tk.WORD,
            padx=10,
            pady=10,
            borderwidth=0,
            relief=tk.FLAT,
            state='disabled',
            height=6
        )
        self.result_text.pack(fill="both", expand=True)
        
        # Manual translator section
        self.manual_frame = tk.LabelFrame(self.main_frame, text="Traductor Manual (ES -> EN)", padx=10, pady=5)
        self.manual_frame.pack(fill="x", pady=(5,5))
        
        # Input
        self.inverse_entry = tk.Entry(self.manual_frame, font=("Arial", 10))
        self.inverse_entry.pack(fill="x", pady=(0,5))
        
        # Translate button
        self.inverse_button = ttk.Button(
            self.manual_frame,
            text="Traducir a Inglés"
        )
        self.inverse_button.pack(fill="x", pady=(0,5))
        
        # Result
        self.inverse_result_label = tk.Label(
            self.manual_frame,
            text="",
            font=("Pearl", 11, "bold"),
            bg=self.popup_bg_color,
            fg=self.text_color,
            anchor="w",
            justify="left",
            wraplength=330,
            padx=5,
            pady=5
        )
        self.inverse_result_label.pack(fill="x", pady=(0,5))

    def create_controls(self):
        # Frame para los controles principales
        self.controls_frame = tk.Frame(self.main_frame)
        self.controls_frame.pack(fill="x", pady=(0, 5))
        
        # Botón de captura
        self.capture_button = ttk.Button(
            self.controls_frame, 
            text="Seleccionar Zona y Traducir (EN -> ES)",
            style='Accent.TButton'
        )
        self.capture_button.pack(fill="x", ipady=5)
        
        # Barra de progreso
        self.progressbar = ttk.Progressbar(self.main_frame, mode='indeterminate')

    def create_settings(self):
        # Frame para ajustes
        self.settings_frame = tk.LabelFrame(self.main_frame, text="Ajustes")
        self.settings_frame.pack(fill='x', pady=5)
        
        # Frame interno para organizar los controles
        inner_frame = tk.Frame(self.settings_frame)
        inner_frame.pack(fill='x', padx=10, pady=5)
        
        # Etiqueta de transparencia
        tk.Label(inner_frame, text="Transparencia Ventana:").grid(row=0, column=0, sticky="w")
        
        # Control deslizante de transparencia
        self.alpha_slider = tk.Scale(
            inner_frame,
            from_=0.1,
            to=1.0,
            resolution=0.05,
            orient=tk.HORIZONTAL
        )
        self.alpha_slider.set(1.0)
        self.alpha_slider.grid(row=0, column=1, sticky="ew", padx=(5, 10))
        
        # Botón de color
        self.color_button = ttk.Button(
            inner_frame,
            text="Color Texto"
        )
        self.color_button.grid(row=0, column=2, sticky="e")
        
        # Configurar el grid
        inner_frame.columnconfigure(1, weight=1)

# Removed expand_button and create_inverse_frame as they are no longer needed

    def create_text_popup(self):
        self.text_popup = tk.Toplevel(self.root)
        self.text_popup.overrideredirect(True)
        self.text_popup.wm_attributes("-topmost", True)
        self.text_popup.attributes("-alpha", 1.0)
        self.text_popup.configure(bg=self.popup_bg_color)

        container_frame = tk.Frame(
            self.text_popup,
            bg=self.popup_bg_color,
            borderwidth=0,
            highlightthickness=0
        )
        container_frame.pack(fill="both", expand=True)

        self.popup_text = Text(
            container_frame,
            font=self.custom_font_object,
            fg=self.text_color,
            bg=self.popup_bg_color,
            wrap=tk.WORD,
            padx=10,
            pady=10,
            borderwidth=0,
            relief=tk.FLAT,
            state='disabled',
            height=1
        )
        self.popup_text.pack(fill="both", expand=True, padx=0, pady=0)
        self.text_popup.withdraw()

    def on_main_window_move(self, event):
        if self.text_popup.winfo_viewable():
            self.position_popup()

    def position_popup(self):
        self.root.update_idletasks()
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_height = self.root.winfo_height()
        root_width = self.root.winfo_width()
        
        popup_x = root_x + 5
        popup_y = root_y + root_height + 5
        
        self.text_popup.geometry(
            f"{root_width}x{self.last_popup_req_height}+{popup_x}+{popup_y}"
        )
        self.text_popup.lift()