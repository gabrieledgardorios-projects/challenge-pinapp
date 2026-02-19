import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base del proyecto"""
    
    # URLs del sitio web a probar
    BASE_URL = os.getenv('BASE_URL', 'https://www.amazon.com')
    
    # Configuración del navegador
    BROWSER = os.getenv('BROWSER', 'chrome')
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
    
    # Timeouts
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', '20'))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
    
    # Directorios
    REPORTS_DIR = 'reports'
    SCREENSHOTS_DIR = 'reports/screenshots'
    
    # Ambiente
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')
