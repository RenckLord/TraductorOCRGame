"""
Utilidades generales para la aplicación
"""
import os
import sys

def resource_path(relative_path: str) -> str:
    """
    Obtiene la ruta del recurso tanto en desarrollo como en aplicación congelada.

    Args:
        relative_path (str): Ruta relativa al recurso

    Returns:
        str: Ruta absoluta al recurso
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)