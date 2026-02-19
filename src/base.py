from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from config.config import Config
import logging
import os

logger = logging.getLogger(__name__)


class DriverFactory:
    """Factory para crear instancias del WebDriver"""
    
    @staticmethod
    def create_driver(browser=None):
        """
        Crea una instancia del WebDriver según el navegador especificado
        
        Args:
            browser (str): Navegador a usar (chrome, firefox, edge)
            
        Returns:
            WebDriver: Instancia del WebDriver
        """
        browser = browser or Config.BROWSER.lower()
        
        options = None
        driver = None
        
        try:
            if browser == 'chrome':
                options = webdriver.ChromeOptions()
                if Config.HEADLESS:
                    options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
                
                # Usar webdriver-manager para obtener la ruta del driver
                driver_path = ChromeDriverManager().install()
                # Validar que el archivo existe
                if os.path.exists(driver_path):
                    service = ChromeService(driver_path)
                    driver = webdriver.Chrome(service=service, options=options)
                else:
                    logger.error(f"El archivo del driver no existe: {driver_path}")
                    raise FileNotFoundError(f"ChromeDriver no encontrado en: {driver_path}")
                
            elif browser == 'firefox':
                options = webdriver.FirefoxOptions()
                if Config.HEADLESS:
                    options.add_argument('--headless')
                options.add_argument('--width=1920')
                options.add_argument('--height=1080')
                
                driver_path = GeckoDriverManager().install()
                if os.path.exists(driver_path):
                    service = FirefoxService(driver_path)
                    driver = webdriver.Firefox(service=service, options=options)
                else:
                    logger.error(f"El archivo del driver no existe: {driver_path}")
                    raise FileNotFoundError(f"GeckoDriver no encontrado en: {driver_path}")
                
            else:
                raise ValueError(f"Navegador no soportado: {browser}")
            
            # Configurar timeouts
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
            
            logger.info(f"WebDriver creado exitosamente para {browser}")
            return driver
            
        except Exception as e:
            logger.error(f"Error al crear el WebDriver: {str(e)}")
            raise


class BasePage:
    """Clase base para las páginas - Page Object Model"""
    
    def __init__(self, driver):
        """
        Inicializa la página base
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def find_element(self, locator):
        """Encuentra un elemento usando el wait explícito"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """Encuentra múltiples elementos"""
        return self.driver.find_elements(*locator)
    
    def click(self, locator):
        """Click en un elemento"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        self.logger.info(f"Click realizado en: {locator}")
    
    def send_keys(self, locator, text):
        """Envía texto a un elemento"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"Texto enviado a {locator}: {text}")
    
    def get_text(self, locator):
        """Obtiene el texto de un elemento"""
        element = self.find_element(locator)
        return element.text
    
    def is_element_visible(self, locator):
        """Verifica si un elemento es visible"""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False
    
    def get_page_title(self):
        """Obtiene el título de la página"""
        return self.driver.title
    
    def get_current_url(self):
        """Obtiene la URL actual"""
        return self.driver.current_url
