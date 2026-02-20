from selenium.webdriver.common.by import By
from src.base import BasePage
import allure
import logging
import time

logger = logging.getLogger(__name__)


class ProductResultsPage(BasePage):
    """Page Object para la página de resultados de productos"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def change_money_to_dollars(self):
        """Cambia la moneda a USD si está disponible"""
        with allure.step("Intentar cambiar moneda a USD"):
            try:
                # Verificar si ya está en USD
                if self.get_current_url().find("currency=USD") != -1:
                    logger.info("La moneda ya está en USD")
                    return
                
                # Intentar hacer click en el botón de opciones de idioma/moneda
                language_and_money_options = (By.XPATH, "//*[@id='icp-nav-flyout']/button")
                if not self.is_element_visible(language_and_money_options):
                    logger.warning("No se encontró el selector de moneda")
                    return
                
                self.click(language_and_money_options)
                time.sleep(2)
                
                # Buscar la opción USD
                usd_option = (By.XPATH, "//a[contains(@href, 'currency=USD')]")
                if not self.is_element_visible(usd_option):
                    logger.warning("No se encontró la opción de USD")
                    return
                
                self.click(usd_option)
                time.sleep(5)
                logger.info("Moneda cambiada a USD exitosamente")
                
            except Exception as e:
                logger.warning(f"No se pudo cambiar la moneda: {str(e)}. Continuando con la moneda actual.")

    def get_brands_filter_locator(self, brand):
        """
        Retorna el locator para seleccionar una marca específica
        Args:
            brand (str): Nombre de la marca
        Returns:
            tuple: Tupla (By, locator_string)
        """
        return (By.XPATH, f"//li[contains(.//span, '{brand}')]//a")
    
    def get_brand_checked_locator(self, brand):
        """
        Retorna el locator para verificar si una marca está seleccionada
        Args:
            brand (str): Nombre de la marca
        Returns:
            tuple: Tupla (By, locator_string)
        """
        return (By.XPATH,
            f"//li[contains(.//span, '{brand}')]//a[@aria-current='true']"
        )
    
    def apply_brand_filter(self, brand):
        """
        Aplica el filtro de marca haciendo click en el link del filtro
        Args:
            brand (str): Nombre de la marca a filtrar
        """
        with allure.step(f"Seleccionar marca: {brand}"):
            locator = self.get_brands_filter_locator(brand)
            self.is_element_visible(locator)
            self.click(locator)
            logger.info(f"Marca '{brand}' filtrada")
    
    def is_brand_filter_applied(self, brand):
        """
        Verifica si el filtro de marca está aplicado
        Args:
            brand (str): Nombre de la marca     
        Returns:
            bool: True si el checkbox está marcado, False en caso contrario
        """
        with allure.step(f"Verificar si marca {brand} está seleccionada"):
            locator = self.get_brand_checked_locator(brand)
            result = self.is_element_visible(locator)
            logger.info(f"Marca '{brand}' seleccionada: {result}")
            return result
        
    def apply_price_filter(self, price_range):
        """
        Aplica el filtro de precio ingresando el rango vía URL
        Args:
            price_range (str): Rango de precio en formato "min-max" (ej: "50-100")
        """
        with allure.step(f"Aplicar filtro de precio: {price_range}"):
            try:
                min_price, max_price = price_range.split("-")
                current_url = self.get_current_url()
                if current_url.find(f"low-price={min_price}") != -1 and current_url.find(f"high-price={max_price}") != -1:
                    logger.info(f"El filtro de precio {price_range} ya está aplicado")
                    return
                else:
                    new_url = f"{current_url}&low-price={min_price}&high-price={max_price}"
                    self.driver.get(new_url)
                    time.sleep(5)
                    logger.info(f"Filtro de precio {price_range} aplicado exitosamente")
            except Exception as e:
                logger.warning(f"No se pudo aplicar el filtro de precio: {str(e)}.")

    def get_product_count(self):
        """Obtiene el número de productos encontrados en la página de resultados"""
        with allure.step("Obtener número de productos encontrados"):
            try:
                # El formato es: "1-48 of over 20,000 results for"
                # Necesitamos extraer el número después de "over" y antes de "results"
                count_locator = (By.XPATH, "//span[contains(text(), 'results for')]")
                time.sleep(2)
                if self.is_element_visible(count_locator):
                    count_text = self.get_text(count_locator)
                    
                    parts = count_text.split()
                    
                    count = 0
                    for i, part in enumerate(parts):
                        if 'results' in part.lower() and i > 0:
                            number_str = parts[i-1].replace(",", "")
                            try:
                                count = int(number_str)
                                break
                            except:
                                pass
                
                    logger.info(f"Número de productos encontrados: {count}")
                    return count
                else:
                    logger.warning("No se encontró el elemento con el número de productos")
                    return 0
            except Exception as e:
                logger.warning(f"No se pudo obtener el número de productos: {str(e)}.")
                return 0

    def sort_by_options(self):
            """Abre el menú de opciones de ordenamiento"""
            with allure.step("Abrir menú de opciones de ordenamiento"):
                time.sleep(1)
                sort_options = (By.XPATH, "//select[@id='s-result-sort-select']/following-sibling::span")
                self.is_element_visible(sort_options)
                self.click(sort_options)

    def sort_by(self, sort_option):
        """
        Ordena los productos según la opción especificada
        Args:
            sort_option (str): Opción de ordenamiento. Opciones disponibles:
                - "price_high_low": Precio del más alto al más bajo
                - "avg_review": Promedio Opinión del cliente
                - "newest": Llegadas más recientes
        """
        sort_options_map = {
            "price_high_low": "//div[@aria-hidden='false']//*[@id='s-result-sort-select_2']",
            "avg_review": "//div[@aria-hidden='false']//*[@id='s-result-sort-select_3']",
            "newest": "//div[@aria-hidden='false']//*[@id='s-result-sort-select_4']"
        }
        
        with allure.step(f"Ordenar productos por: {sort_option}"):
            try:
                if sort_option not in sort_options_map:
                    logger.warning(f"Opción de ordenamiento '{sort_option}' no válida. Opciones disponibles: {list(sort_options_map.keys())}")
                    return False
                
                self.sort_by_options()
                time.sleep(1)
                
                sort_element_xpath = sort_options_map[sort_option]
                sort_element = (By.XPATH, sort_element_xpath)
                
                self.is_element_visible(sort_element)
                self.click(sort_element)
                time.sleep(1)
                
                logger.info(f"Productos ordenados por: {sort_option}")
                return True
            except Exception as e:
                logger.warning(f"No se pudo ordenar los productos: {str(e)}")
                return False

    def get_first_five_products_info(self):
        """Obtiene el nombre y precio de los cinco primeros productos"""
        with allure.step("Obtener información de los cinco primeros productos"):
            products_info = []
            try:
                time.sleep(2)
                product_elements = self.find_elements((By.XPATH, "//div[@data-component-type='s-search-result']"))[:5]
                
                for product in product_elements:
                    try:
                        product_name = product.find_element(By.XPATH, ".//h2//span").text
                        time.sleep(1)
                        
                        try:
                            product.find_element(By.XPATH, ".//a[contains(text(),'See options')]")
                            price = "Varía según opciones"
                            logger.info(f"Producto encontrado: {product_name} - Precio: {price}")
                        except:
                            try:
                                price_whole = product.find_element(By.XPATH, ".//span[@class='a-price-whole']").text.replace(",", "")
                                price_fraction = product.find_element(By.XPATH, ".//span[@class='a-price-fraction']").text
                                price = f"{price_whole}.{price_fraction}"
                                logger.info(f"Producto encontrado: {product_name} - Precio: {price}")
                            except:
                                price = "Precio no disponible"
                                logger.warning(f"Producto encontrado: {product_name} - Precio no disponible")
                        
                        products_info.append({"name": product_name, "price": price})
                    except Exception as e:
                        logger.warning(f"Error procesando un producto: {str(e)}")
                        continue
                
                logger.info("Información de los cinco primeros productos obtenida correctamente")
                return products_info
            except Exception as e:
                logger.warning(f"No se pudo obtener la información de los productos: {str(e)}.")
                return products_info