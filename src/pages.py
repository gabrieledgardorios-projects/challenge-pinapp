from selenium.webdriver.common.by import By
from src.base import BasePage


class HomePage(BasePage):
    """Page Object para la página de inicio"""
    
    # Locators
    SEARCH_INPUT = (By.ID, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGO = (By.CLASS_NAME, "logo")
    MENU_ITEMS = (By.CSS_SELECTOR, "nav ul li")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def load(self):
        """Carga la página de inicio"""
        from config.config import Config
        self.driver.get(Config.BASE_URL)
        self.logger.info(f"Página de inicio cargada: {Config.BASE_URL}")
    
    def search(self, query):
        """Realiza una búsqueda"""
        self.send_keys(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
        self.logger.info(f"Búsqueda realizada: {query}")
    
    def get_logo_text(self):
        """Obtiene el texto del logo"""
        return self.get_text(self.LOGO)
    
    def get_menu_items_count(self):
        """Obtiene la cantidad de items en el menú"""
        return len(self.find_elements(self.MENU_ITEMS))
    
    def is_page_loaded(self):
        """Verifica que la página se cargó correctamente"""
        return self.is_element_visible(self.LOGO)
