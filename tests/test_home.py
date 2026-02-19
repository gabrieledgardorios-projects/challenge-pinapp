import pytest
import logging
import allure
from src.pages import HomePage


logger = logging.getLogger(__name__)


@allure.feature("Home Page")
@allure.story("Page Load and UI Elements")
class TestHomePage:
    """Suite de tests para la página de inicio"""
    
    @pytest.mark.smoke
    @allure.title("Verificar título de la página")
    @allure.description("Valida que el título de la página sea correcto")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_page_title(self, driver):
        """Verifica que el título de la página sea correcto"""
        with allure.step("Cargar la página de inicio"):
            home_page = HomePage(driver)
            home_page.load()
        
        with allure.step("Obtener el título de la página"):
            title = home_page.get_page_title()
        
        with allure.step("Verificar que el título no está vacío"):
            assert title, "El título de la página está vacío"
        
        allure.attach(title, name="Page Title", attachment_type=allure.attachment_type.TEXT)
        logger.info(f"Título de la página: {title}")
    
    @pytest.mark.smoke
    @allure.title("Verificar carga correcta de la página")
    @allure.description("Valida que la página se cargue correctamente")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_page_loaded_successfully(self, driver):
        """Verifica que la página se cargue correctamente"""
        with allure.step("Cargar la página de inicio"):
            home_page = HomePage(driver)
            home_page.load()
        
        with allure.step("Verificar que la página se cargó correctamente"):
            assert home_page.is_page_loaded(), "La página no se cargó correctamente"
        
        logger.info("Página cargada exitosamente")
    
    @pytest.mark.regression
    @allure.title("Verificar URL correcta")
    @allure.description("Valida que la URL sea la esperada")
    @allure.severity(allure.severity_level.NORMAL)
    def test_url_is_correct(self, driver):
        """Verifica que la URL sea correcta"""
        from config.config import Config
        
        with allure.step("Cargar la página de inicio"):
            home_page = HomePage(driver)
            home_page.load()
        
        with allure.step("Obtener la URL actual"):
            current_url = home_page.get_current_url()
        
        with allure.step(f"Verificar que URL contiene {Config.BASE_URL}"):
            assert Config.BASE_URL in current_url, \
                f"URL incorrecta. Esperado: {Config.BASE_URL}, Actual: {current_url}"
        
        allure.attach(current_url, name="Current URL", attachment_type=allure.attachment_type.TEXT)
        logger.info(f"URL verificada correctamente: {current_url}")
    
    @pytest.mark.regression
    @allure.title("Verificar existencia de items en menú")
    @allure.description("Valida que existan items en el menú de navegación")
    @allure.severity(allure.severity_level.NORMAL)
    def test_menu_items_exist(self, driver):
        """Verifica que existan items en el menú"""
        with allure.step("Cargar la página de inicio"):
            home_page = HomePage(driver)
            home_page.load()
        
        with allure.step("Contar items en el menú"):
            menu_count = home_page.get_menu_items_count()
        
        with allure.step("Verificar que existen items"):
            assert menu_count > 0, "No se encontraron items en el menú"
        
        allure.attach(str(menu_count), name="Menu Items Count", attachment_type=allure.attachment_type.TEXT)
        logger.info(f"Items en el menú encontrados: {menu_count}")
    
    @pytest.mark.sanity
    @allure.title("Verificar existencia del campo de búsqueda")
    @allure.description("Valida que el campo de búsqueda sea visible")
    @allure.severity(allure.severity_level.MINOR)
    def test_search_input_exists(self, driver, take_screenshot):
        """Verifica que el campo de búsqueda exista"""
        with allure.step("Cargar la página de inicio"):
            home_page = HomePage(driver)
            home_page.load()
        
        with allure.step("Verificar visibilidad del campo de búsqueda"):
            try:
                assert home_page.is_element_visible(home_page.SEARCH_INPUT), \
                    "El campo de búsqueda no es visible"
                logger.info("Campo de búsqueda visible")
            except AssertionError as e:
                with allure.step("Capturar screenshot del error"):
                    take_screenshot("search_input_not_found")
                raise
