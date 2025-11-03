"""
Funciones para descargar y gestionar modelos de voz
"""
import os
import requests
import zipfile
from tqdm import tqdm
from traductorocr.utils.paths import resource_path

def download_vosk_model():
    """
    Descarga el modelo de voz pequeño en inglés de Vosk si no está presente
    """
    model_path = resource_path('vosk-model-small-en-us')
    if os.path.exists(model_path):
        return True
        
    # URL del modelo pequeño en inglés
    model_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    zip_path = resource_path('vosk-model.zip')
    
    try:
        print("Descargando modelo de voz (85MB)...")
        response = requests.get(model_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        with open(zip_path, 'wb') as f, tqdm(
            desc="Descargando",
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                progress.update(size)
                
        print("Extrayendo modelo...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(resource_path(''))
            
        # Renombrar la carpeta extraída
        extracted_dir = resource_path('vosk-model-small-en-us-0.15')
        if os.path.exists(extracted_dir):
            os.rename(extracted_dir, model_path)
            
        # Limpiar archivo zip
        os.remove(zip_path)
        print("Modelo instalado correctamente")
        return True
        
    except Exception as e:
        print(f"Error al descargar el modelo: {e}")
        if os.path.exists(zip_path):
            os.remove(zip_path)
        return False