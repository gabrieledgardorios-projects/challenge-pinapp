import pytest
import logging
import os
from datetime import datetime
from src.base import DriverFactory
from config.config import Config
import allure

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{Config.REPORTS_DIR}/test.log"),
        logging.StreamHandler()
    ]
)


@pytest.fixture(scope="function")
def driver():
    """
    Fixture que proporciona una instancia de WebDriver para cada test
    """
    logging.info("Inicializando WebDriver")
    
    # Crear directorios necesarios
    os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(Config.REPORTS_DIR, exist_ok=True)
    
    driver_instance = DriverFactory.create_driver()
    
    yield driver_instance
    
    logging.info("Cerrando WebDriver")
    driver_instance.quit()


@pytest.fixture(scope="function")
def take_screenshot(driver):
    """
    Fixture para tomar screenshots en caso de fallo
    """
    def _take_screenshot(name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{Config.SCREENSHOTS_DIR}/{name}_{timestamp}.png"
        driver.save_screenshot(filename)
        logging.info(f"Screenshot guardado: {filename}")
        # Adjuntar screenshot a Allure
        allure.attach.file(
            filename,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
    
    return _take_screenshot


def pytest_addoption(parser):
    """Agregar opciones personalizadas de pytest"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Navegador a usar: chrome, firefox"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Ejecutar en modo headless"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=Config.BASE_URL,
        help="URL base del sitio web"
    )


@pytest.fixture(scope="session", autouse=True)
def configure_test_environment(request):
    """
    Configura el ambiente de pruebas al inicio de la sesión
    """
    Config.BROWSER = request.config.getoption("--browser")
    Config.HEADLESS = request.config.getoption("--headless")
    Config.BASE_URL = request.config.getoption("--base-url")
    
    logging.info(f"Ambiente configurado:")
    logging.info(f"  - Browser: {Config.BROWSER}")
    logging.info(f"  - Headless: {Config.HEADLESS}")
    logging.info(f"  - Base URL: {Config.BASE_URL}")
    
    # Agregar información al reporte de Allure
    allure.dynamic.parameter("browser", Config.BROWSER)
    allure.dynamic.parameter("headless", Config.HEADLESS)
    allure.dynamic.parameter("base_url", Config.BASE_URL)
