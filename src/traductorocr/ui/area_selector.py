"""
Selector de área de pantalla
"""
import tkinter as tk
from typing import Optional, Tuple

class AreaSelector:
    def __init__(self, root: tk.Tk):
        """
        Inicializa el selector de área.

        Args:
            root (tk.Tk): Ventana raíz de Tkinter
        """
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)
        self.root.attributes("-topmost", True)
        
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        
        self.start_x: Optional[float] = None
        self.start_y: Optional[float] = None
        self.rect: Optional[int] = None
        self.selection_box: Optional[Tuple[float, float, float, float]] = None
        
        self._bind_events()

    def _bind_events(self) -> None:
        """Vincula los eventos del mouse a los métodos correspondientes"""
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event) -> None:
        """Maneja el evento de presionar el botón del mouse"""
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        
        if self.rect:
            self.canvas.delete(self.rect)
        
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            self.start_x, self.start_y,
            outline='red',
            width=2
        )

    def on_mouse_drag(self, event) -> None:
        """Maneja el evento de arrastrar el mouse"""
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event) -> None:
        """Maneja el evento de soltar el botón del mouse"""
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        
        self.selection_box = (
            min(self.start_x, end_x),
            min(self.start_y, end_y),
            abs(self.start_x - end_x),
            abs(self.start_y - end_y)
        )
        self.root.destroy()