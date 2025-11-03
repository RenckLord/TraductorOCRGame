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
        self.is_audio_expanded = False

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
        self.root.geometry("350x400")  # Altura inicial de 400
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
        self.create_audio_expand_button()
        self.create_audio_frame()
        
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
        
    def update_audio_devices(self, devices: list) -> None:
        """Actualiza la lista de dispositivos de audio"""
        self.device_list = devices
        if not devices:
            self.device_selector['values'] = ['No hay dispositivos disponibles']
            self.device_selector.set('No hay dispositivos disponibles')
            if hasattr(self, 'audio_capture_button'):
                self.audio_capture_button.configure(state='disabled')
            return
            
        device_names = [dev[1] for dev in devices]
        self.device_selector['values'] = device_names
        self.device_selector.set(device_names[0])  # Seleccionar el primer dispositivo
        if hasattr(self, 'audio_capture_button'):
            self.audio_capture_button.configure(state='normal')
        
    def get_selected_device_id(self) -> int:
        """Obtiene el ID del dispositivo seleccionado"""
        try:
            current_device = self.device_var.get()
            if current_device == 'No hay dispositivos disponibles':
                return None
                
            for device_id, name in self.device_list:
                if name == current_device:
                    return device_id
        except:
            pass
        return None
        
    def on_refresh_devices(self) -> None:
        """Refresca la lista de dispositivos de audio"""
        import sounddevice as sd
        try:
            devices = sd.query_devices()
            input_devices = []
            
            # Primero buscamos el dispositivo de mezcla estéreo o similar
            stereo_mix = None
            for i, dev in enumerate(devices):
                name = dev['name'].lower()
                if (dev['max_input_channels'] > 0 and 
                    ('stereo mix' in name or 
                     'estéreo mix' in name or 
                     'what u hear' in name or
                     'mezcla estéreo' in name or
                     'audio interno' in name or
                     'salida de audio' in name)):
                    stereo_mix = (i, f"🔊 {dev['name']} (Audio del Sistema)")
                    break
            
            # Si encontramos el stereo mix, lo añadimos primero
            if stereo_mix:
                input_devices.append(stereo_mix)
            
            # Luego añadimos el resto de dispositivos
            for i, dev in enumerate(devices):
                if dev['max_input_channels'] > 0:
                    try:
                        name = dev['name']
                        # Evitar duplicados y dispositivos predeterminados
                        if any(name in d[1] for d in input_devices):
                            continue
                            
                        if 'default' in name.lower() or 'predeterminado' in name.lower():
                            continue
                            
                        # Clasificar el dispositivo
                        if 'headset' in name.lower() or 'auricular' in name.lower():
                            device_name = f"🎧 {name} (Auriculares)"
                        elif 'microphone' in name.lower() or 'micrófono' in name.lower():
                            device_name = f"🎤 {name} (Micrófono)"
                        elif 'virtual' in name.lower():
                            device_name = f"🔊 {name} (Audio Virtual)"
                        else:
                            device_name = f"📱 {name}"
                            
                        # Verificar que el dispositivo funciona
                        with sd.InputStream(device=i, channels=1, samplerate=16000, blocksize=1024):
                            pass
                            
                        input_devices.append((i, device_name))
                    except:
                        continue  # Ignorar dispositivos que no se pueden abrir
                        
            self.update_audio_devices(input_devices)
        except Exception as e:
            import traceback
            print(f"Error al obtener dispositivos: {str(e)}")
            print(traceback.format_exc())
            self.update_audio_devices([])

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
        current_height = self.root.winfo_height()
        if self.is_expanded:
            self.inverse_frame.pack_forget()
            new_height = current_height - 150
            if new_height < 400:  # Altura mínima
                new_height = 400
            self.root.geometry(f"350x{new_height}")
            self.expand_button.config(text="Traductor Manual (ES -> EN) ▼")
            self.is_expanded = False
            # Reposicionar el panel de audio si está expandido
            if self.is_audio_expanded:
                self.audio_frame.pack(fill="both", expand=True, pady=5)
        else:
            new_height = current_height + 150
            self.root.geometry(f"350x{new_height}")
            self.inverse_frame.pack(fill="both", expand=True, pady=5)
            self.expand_button.config(text="Ocultar Traductor Manual ▲")
            self.is_expanded = True

    def create_audio_expand_button(self) -> None:
        """Crea el botón para expandir/contraer la traducción de audio"""
        self.audio_expand_button = ttk.Button(
            self.main_frame,
            text="Traductor de Audio (EN -> ES) ▼",
            style="Link.TButton",
            command=self.toggle_audio_expand
        )
        self.audio_expand_button.pack(fill="x", pady=(5, 0))
        self.is_audio_expanded = False

    def toggle_audio_expand(self) -> None:
        """Alterna entre mostrar/ocultar el panel de traducción de audio"""
        def get_height_from_geometry(geometry_str):
            """Extrae la altura de la cadena de geometría"""
            # Formato: 'anchoxalto+x+y' o 'anchoxalto'
            parts = geometry_str.split('+')[0]  # Tomar solo 'anchoxalto'
            return int(parts.split('x')[1])  # Tomar solo el alto
            
        if self.is_audio_expanded:
            self.audio_frame.pack_forget()
            try:
                current_height = get_height_from_geometry(self.root.geometry())
                new_height = max(300, current_height - 150)  # No menor que 300
                self.root.geometry(f"350x{new_height}")
            except (ValueError, IndexError):
                # Si hay error al parsear la geometría, usar tamaño predeterminado
                self.root.geometry("350x300")
            self.audio_expand_button.config(text="Traductor de Audio (EN -> ES) ▼")
            self.is_audio_expanded = False
        else:
            try:
                current_height = get_height_from_geometry(self.root.geometry())
                new_height = current_height + 150
                self.root.geometry(f"350x{new_height}")
            except (ValueError, IndexError):
                # Si hay error, agregar 150 al tamaño actual
                self.root.geometry("350x450")
            self.audio_frame.pack(fill="both", expand=True, pady=5)
            self.audio_expand_button.config(text="Ocultar Traductor de Audio ▲")
            self.is_audio_expanded = True

    def create_audio_frame(self) -> None:
        """Crea el panel de traducción de audio"""
        self.audio_frame = ttk.LabelFrame(
            self.main_frame,
            text="Traductor de Audio (EN -> ES)",
            padding=(5, 5)
        )
        
        # Frame superior para dispositivo y estado
        top_frame = ttk.Frame(self.audio_frame)
        top_frame.pack(fill="x", pady=(0, 5))
        
        # Frame izquierdo para selector de dispositivo
        device_frame = ttk.Frame(top_frame)
        device_frame.pack(side="left", fill="x", expand=True)
        
        # Selector de dispositivo de audio
        ttk.Label(
            device_frame,
            text="Dispositivo:",
            font=("Pearl", 8)
        ).pack(side="left", padx=(0, 5))
        
        self.device_var = tk.StringVar()
        self.device_selector = ttk.Combobox(
            device_frame,
            textvariable=self.device_var,
            state="readonly",
            width=30,
            font=("Pearl", 8)
        )
        self.device_selector.pack(side="left", fill="x", expand=True)
        
        # Botón de actualizar
        self.refresh_devices_button = ttk.Button(
            device_frame,
            text="⟳",
            width=3,
            style='Accent.TButton',
            command=self.on_refresh_devices
        )
        self.refresh_devices_button.pack(side="right", padx=(5, 0))
        
        # Frame para estado
        self.status_frame = ttk.Frame(top_frame)
        self.status_frame.pack(side="right", padx=(10, 0))
        
        self.audio_status_label = ttk.Label(
            self.status_frame,
            text="Estado:",
            font=("Pearl", 8)
        )
        self.audio_status_label.pack(side="left")
        
        self.audio_status_value = ttk.Label(
            self.status_frame,
            text="Inactivo",
            font=("Pearl", 8),
            foreground="red"
        )
        self.audio_status_value.pack(side="left", padx=(5, 0))
        
        # Botón de captura
        self.audio_capture_button = ttk.Button(
            self.audio_frame,
            text="Iniciar Captura de Audio",
            style='Accent.TButton'
        )
        self.audio_capture_button.pack(fill="x", pady=5)
        
        # Área de subtítulos/traducciones
        self.subtitles_text = Text(
            self.audio_frame,
            font=self.custom_font_object,
            fg=self.text_color,
            bg=self.popup_bg_color,
            wrap=tk.WORD,
            height=3,
            relief=tk.FLAT,
            state='disabled'
        )
        self.subtitles_text.pack(fill="both", expand=True)
        
        # Inicializar lista de dispositivos
        self.device_list = []
        self.on_refresh_devices()