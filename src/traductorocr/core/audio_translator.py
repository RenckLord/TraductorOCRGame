"""
Módulo para la captura y traducción de audio
"""
import os
import json
import threading
import queue
import time
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import numpy as np
from deep_translator import GoogleTranslator
from typing import Callable, Optional
from traductorocr.utils.paths import resource_path

class AudioTranslator:
    
    
    def _translate_text(self, text: str):
        """Función helper para traducir y enviar a la UI"""
        try:
            print(f"Texto reconocido (final): {text}")
            translation = self.translator.translate(text)
            # ¡SOLO ENVIAMOS LA TRADUCCIÓN!
            self.on_translation(translation)
        except Exception as e:
            print(f"Error en traducción: {e}")
            self.on_translation(f"Error al traducir: {e}")
    
    
    def __init__(self, on_translation: Callable[[str], None], on_error: Callable[[str], None]):
        """
        Inicializa el traductor de audio.
        
        Args:
            on_translation: Callback para cuando hay una nueva traducción
            on_error: Callback para cuando ocurre un error
        """
        self.translator = GoogleTranslator(source='en', target='es')
        self.audio_queue = queue.Queue()
        self.is_capturing = False
        self.capture_thread = None
        self.translation_thread = None
        self.on_translation = on_translation
        self.on_error = on_error
        
        # Configuración de audio
        self.samplerate = 16000
        self.channels = 1
        self.dtype = np.int16
        self.device = None  # Dispositivo de audio seleccionado
        
        self.last_partial_text = ""
        self.last_partial_time = 0
        self.debounce_time = 0.5  # 500ms de "calma" antes de traducir
        # --- FIN DE LO AÑADIDO ---
        
    def get_audio_devices(self):
        """Obtiene la lista de dispositivos de audio disponibles"""
        try:
            hostapis = sd.query_hostapis()
            devices = sd.query_devices()
            input_devices = []
            
            # Primero buscamos la Mezcla Estéreo (audio interno de Windows)
            for i, dev in enumerate(devices):
                if dev['max_input_channels'] > 0:
                    name = dev['name'].lower()
                    if ('stereo mix' in name or 'mezcla estéreo' in name or 
                        'what u hear' in name or 'lo que escuchas' in name):
                        input_devices.append((i, f"🔊 Mezcla Estéreo (Audio del Sistema)"))
                        break
            
            # Luego agregamos el resto de dispositivos
            for i, dev in enumerate(devices):
                if dev['max_input_channels'] > 0:
                    name = dev['name']
                    # Evitar duplicados
                    if any(name in device[1] for device in input_devices):
                        continue
                        
                    # Identificar tipo de dispositivo
                    if ('wasapi' in name.lower() and 'loopback' in name.lower()):
                        device_name = f"🔊 Audio del Sistema (WASAPI)"
                    elif any(keyword in name.lower() for keyword in ['headphone', 'auricular', 'headset']):
                        device_name = f"� {name}"
                    elif any(keyword in name.lower() for keyword in ['microphone', 'mic', 'micrófono']):
                        device_name = f"🎤 {name}"
                    else:
                        device_name = f"🎙️ {name}"
                        
                    # Verificar que el dispositivo funciona
                    try:
                        with sd.InputStream(device=i, channels=1, samplerate=16000, blocksize=1024):
                            input_devices.append((i, device_name))
                    except:
                        continue
                        
            return input_devices
        except Exception as e:
            self.on_error(f"Error al obtener dispositivos de audio: {str(e)}")
            return []
            
    def set_audio_device(self, device_id: int) -> None:
        """Establece el dispositivo de audio a usar"""
        try:
            # Obtener información del dispositivo
            device_info = sd.query_devices(device_id)
            self.device = device_id
            
            # Determinar configuración basada en el dispositivo
            device_name = device_info['name'].lower()
            
            # Configuración específica para HyperX Virtual Surround
            if 'hyperx virtual surround' in device_name:
                self.samplerate = 16000  # Forzar tasa para mejor compatibilidad
                self.channels = 1  # Forzar mono
                self.is_virtual_device = True
            else:
                # Usar la tasa de muestreo nativa del dispositivo
                self.samplerate = int(device_info['default_samplerate'])
                # Determinar el número de canales basado en el dispositivo
                if any(keyword in device_name for keyword in ['stereo mix', 'wasapi']):
                    self.channels = 2  # Usar estéreo para audio del sistema
                else:
                    self.channels = 1  # Usar mono para micrófonos
                self.is_virtual_device = False
                
            print(f"Dispositivo configurado: {device_info['name']} @ {self.samplerate}Hz")
            
            # Cargar el modelo de reconocimiento de voz
            model_path = resource_path('vosk-model-small-en-us')
            if not os.path.exists(model_path):
                self.on_error("Modelo de voz no encontrado")
                return
            
            # Inicializar el modelo solo si no existe o si cambió la tasa de muestreo
            if not hasattr(self, 'model') or not hasattr(self, 'recognizer'):
                self.model = Model(model_path)
                self.recognizer = KaldiRecognizer(self.model, self.samplerate)
            
            # Probar el dispositivo
            test_duration = 0.1  # 100ms de prueba
            try:
                with sd.InputStream(device=self.device,
                                 channels=self.channels,
                                 samplerate=self.samplerate,
                                 blocksize=int(self.samplerate * test_duration)):
                    pass  # Solo probamos que podemos abrir el stream
                print(f"Prueba de dispositivo exitosa: {device_info['name']}")
            except Exception as e:
                raise Exception(f"Error al probar dispositivo: {str(e)}")
                
        except Exception as e:
            self.on_error(f"Error al configurar dispositivo de audio: {str(e)}")
            self.device = None
        
    def start_capture(self) -> None:
        """Inicia la captura de audio"""
        if self.is_capturing:
            return
            
        self.is_capturing = True
        self.capture_thread = threading.Thread(target=self._capture_audio)
        self.translation_thread = threading.Thread(target=self._process_audio)
        self.capture_thread.daemon = True
        self.translation_thread.daemon = True
        self.capture_thread.start()
        self.translation_thread.start()
        
    def stop_capture(self) -> None:
        """Detiene la captura de audio"""
        self.is_capturing = False
        if self.capture_thread:
            self.capture_thread.join()
        if self.translation_thread:
            self.translation_thread.join()
            
    def _capture_audio(self) -> None:
        """Captura el audio del sistema"""
        if self.device is None:
            self.on_error("No hay dispositivo de audio seleccionado")
            return
            
        try:
            device_info = sd.query_devices(self.device)
            print(f"Iniciando captura de audio desde: {device_info['name']}")
            
            stream_config = {
                'device': self.device,
                'channels': self.channels,
                'samplerate': self.samplerate,
                'dtype': self.dtype,
                'blocksize': 4096 if self.channels == 2 else 2048,  # Buffer más grande para audio estéreo
                'callback': self._audio_callback
            }
            
            print("Configuración de captura:", stream_config)
            print("Iniciando stream de audio...")
            
            with sd.InputStream(**stream_config) as stream:
                while self.is_capturing:
                    if not stream.active:
                        raise Exception("El stream de audio se detuvo")
                    sd.sleep(100)
                    
        except Exception as e:
            import traceback
            print(f"Error en captura de audio: {str(e)}")
            print(traceback.format_exc())
            self.on_error(f"Error en captura de audio: {str(e)}")
            self.is_capturing = False
            
    def _audio_callback(self, indata: np.ndarray, frames: int, 
                        time: Optional[dict], status: Optional[sd.CallbackFlags]) -> None:
        """Callback para procesar el audio capturado"""
        if status:
            print(f"Error de estado en callback: {status}")
            return
        
        try:
            if indata is not None and np.any(indata):
                # (Tu lógica de depuración de audio crudo)
                audio_level = np.max(np.abs(indata))
                if audio_level > 500:
                    print(f"Nivel de audio crudo detectado: {audio_level}")
                
                processed_data = indata
                
                # Convertir a mono SI ES ESTÉREO
                if processed_data.shape[1] == 2:
                    # Convertir a float, promediar, y volver a int16
                    processed_data_float = processed_data.astype(np.float32)
                    mono_float = np.mean(processed_data_float, axis=1)
                    processed_data = mono_float.astype(np.int16)
                
                # Aplanar el array
                processed_data = processed_data.flatten()
                
                # Pre-procesar audio (si es virtual)
                if hasattr(self, 'is_virtual_device') and self.is_virtual_device:
                    processed_data = self._preprocess_virtual_audio(processed_data)
                
                # Poner BYTES en la cola para procesamiento
                self.audio_queue.put(processed_data.tobytes())
        except Exception as e:
            print(f"Error en callback de audio: {e}")
            
    def _preprocess_virtual_audio(self, audio_data: np.ndarray) -> np.ndarray:
        """Pre-procesa el audio de dispositivos virtuales (ahora en int16)"""
        try:
            # Aplicar un umbral de ruido (ej: ~1% del max int16)
            noise_threshold = 327
            audio_data[np.abs(audio_data) < noise_threshold] = 0
            return audio_data
        except Exception as e:
            print(f"Error en pre-procesamiento de audio: {e}")
            return audio_data
        
    def _process_audio(self) -> None:
        """Procesa y traduce el audio capturado en tiempo real con 'debounce'"""
        
        while self.is_capturing:
            try:
                # 1. Obtener bytes de audio de la cola
                audio_bytes = self.audio_queue.get(timeout=0.1) # Timeout corto
                
                # 2. Alimentar el trozo a Vosk
                if self.recognizer.AcceptWaveform(audio_bytes):
                    # A. Vosk detectó un resultado FINAL (una pausa larga)
                    result = json.loads(self.recognizer.Result())
                    text = result.get('text', '').strip()
                    if text:
                        # Es un resultado final, traducir de inmediato
                        self._translate_text(text)
                    self.last_partial_text = "" # Limpiar el borrador
                else:
                    # B. Vosk tiene un resultado PARCIAL (borrador)
                    partial_result = json.loads(self.recognizer.PartialResult())
                    partial_text = partial_result.get('partial', '').strip()
                    
                    if partial_text and partial_text != self.last_partial_text:
                        # El texto parcial ha cambiado. Actualizarlo y registrar la hora.
                        self.last_partial_text = partial_text
                        self.last_partial_time = time.time()
            
            except queue.Empty:
                # La cola está vacía (pausa corta o silencio).
                # Este es el lugar perfecto para comprobar nuestro "debounce".
                current_time = time.time()
                if (self.last_partial_text and 
                    (current_time - self.last_partial_time > self.debounce_time)):
                    
                    # Ha pasado 0.5s sin cambios. Traducir este "borrador estable".
                    text_to_translate = self.last_partial_text
                    
                    # ¡Importante! Reiniciar el texto parcial para no volver a traducirlo
                    self.last_partial_text = "" # Marcar como "traducido"
                    
                    # Llamar a la traducción EN UN HILO NUEVO
                    # para no bloquear este bucle de procesamiento de audio.
                    threading.Thread(target=self._translate_text, args=(text_to_translate,), daemon=True).start()
                else:
                    # No hay nada que hacer, solo es silencio.
                    pass
            
            except Exception as e:
                print(f"Error en procesamiento de audio: {e}")
                import traceback
                print(traceback.format_exc())
                self.last_partial_text = "" # Reset en caso de error
            
        #finally:
            # Al detener la captura, procesar lo que quede
            #if not self.is_capturing:
              #  final_result = json.loads(self.recognizer.FinalResult())
               # text = final_result.get('text', '').strip()
               # if text:
                #    self._translate_text(text)
                
    def _recognize_speech(self, audio_data: np.ndarray) -> Optional[str]:
        """Convierte el audio en texto usando reconocimiento de voz de Vosk"""
        try:
            # Convertir el audio a formato correcto para Vosk
            audio_data = (audio_data * 32768).astype('int16')
            
            if self.recognizer.AcceptWaveform(audio_data.tobytes()):
                result = json.loads(self.recognizer.Result())
                if result.get('text'):
                    return result['text']
            return None
        except Exception as e:
            self.on_error(f"Error en reconocimiento de voz: {str(e)}")
            return None