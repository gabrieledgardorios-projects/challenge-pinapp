from selenium.webdriver.common.by import By
from src.base import BasePage


class HomePage(BasePage):
    """Page Object para la página de inicio"""
    
    # Locators
    SEARCH_INPUT = (By.ID, "twotabsearchtextbox")
    SEARCH_SUBMIT_BUTTON = (By.ID, "nav-search-submit-button")
    LOGO = (By.CLASS_NAME, "logo")
    MENU_ITEMS = (By.CSS_SELECTOR, "nav ul li")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def load(self):
        from config.config import Config
        self.driver.get(Config.BASE_URL)
        self.logger.info(f"Página de inicio cargada: {Config.BASE_URL}")
    
    def search_product(self, product):
        self.send_keys(self.SEARCH_INPUT, product)
        self.click(self.SEARCH_SUBMIT_BUTTON)
        self.logger.info(f"Búsqueda realizada: {product}")