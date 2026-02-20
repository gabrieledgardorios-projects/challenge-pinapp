import cv2
import threading
import logging
import time
import numpy as np
from datetime import datetime
from PIL import ImageGrab

logger = logging.getLogger(__name__)


class VideoRecorder:
    """Clase para grabar videos de la ejecución de tests"""
    
    def __init__(self, output_path, fps=5):
        """
        Inicializa el grabador de video
        
        Args:
            output_path (str): Ruta completa del archivo de salida (.avi)
            fps (int): Fotogramas por segundo (default: 5)
        """
        self.output_path = output_path
        self.fps = fps
        self.recording = False
        self.thread = None
        self.writer = None
        
        # Obtener resolución de pantalla
        screen = ImageGrab.grab()
        self.resolution = (screen.width, screen.height)
        
        logger.info(f"VideoRecorder inicializado: {output_path} ({self.resolution[0]}x{self.resolution[1]}) @ {fps} fps")
    
    def start(self):
        """Inicia la grabación de video en un thread separado"""
        if self.recording:
            logger.warning("Ya está grabando")
            return
        
        self.recording = True
        
        try:
            # Crear codec y writer
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.writer = cv2.VideoWriter(
                self.output_path,
                fourcc,
                self.fps,
                self.resolution
            )
            
            # Iniciar thread de grabación
            self.thread = threading.Thread(target=self._record_loop, daemon=True)
            self.thread.start()
            
            logger.info(f"Grabación iniciada: {self.output_path}")
        except Exception as e:
            logger.error(f"Error al iniciar grabación: {str(e)}")
            self.recording = False
    
    def _record_loop(self):
        """Loop de grabación que se ejecuta en un thread separado"""
        try:
            while self.recording:
                # Capturar pantalla
                screenshot = ImageGrab.grab()
                
                # Convertir PIL Image a numpy array
                frame = np.array(screenshot)
                
                # Convertir de RGB a BGR para OpenCV
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Redimensionar si es necesario
                frame = cv2.resize(frame, self.resolution)
                
                # Escribir frame
                if self.writer and self.writer.isOpened():
                    self.writer.write(frame)
                
                # Pequeña pausa para no saturar CPU
                time.sleep(1.0 / self.fps)
                
        except Exception as e:
            logger.error(f"Error en loop de grabación: {str(e)}")
    
    def stop(self):
        """Detiene la grabación y libera recursos"""
        if not self.recording:
            logger.warning("No está grabando")
            return
        
        try:
            self.recording = False
            
            # Esperar a que el thread termine
            if self.thread:
                self.thread.join(timeout=5)
            
            # Liberar el writer
            if self.writer:
                self.writer.release()
                self.writer = None
            
            logger.info(f"Grabación detenida: {self.output_path}")
            
            # Verificar que el archivo se creó
            import os
            if os.path.exists(self.output_path):
                file_size = os.path.getsize(self.output_path)
                logger.info(f"Video guardado: {self.output_path} ({file_size} bytes)")
            else:
                logger.warning(f"No se encontró el archivo: {self.output_path}")
                
        except Exception as e:
            logger.error(f"Error al detener grabación: {str(e)}")
