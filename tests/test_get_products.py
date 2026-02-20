import pytest
import logging
import allure
from src.pages.home_page import HomePage
from src.pages.product_results_page import ProductResultsPage


logger = logging.getLogger(__name__)


@allure.feature("Get Products Page")
class TestGetProducts:
    """Suite de tests para la página de productos"""
    
    def test_get_information_of_products(self, driver):
        """Verifica que se puedan obtener la información de los productos correctamente"""
        home = HomePage(driver)
        products = ProductResultsPage(driver)
        
        with allure.step("Cargar página de inicio"):
            home.load()
        
        with allure.step("Buscar un producto específico"):
            home.search_product("zapatos")

        with allure.step("Cambiar moneda a USD si es necesario"):
            products.change_money_to_dollars()
        
        with allure.step("Filtrar resultados por Marca"):
            products.apply_brand_filter("Skechers")

        with allure.step("Verificar que el filtro de marca se aplicó correctamente"):
            assert products.is_brand_filter_applied("Skechers"), "El filtro de marca no se aplicó correctamente"

        with allure.step("Filtrar por rango de precio"):
            products.apply_price_filter("100-200")
            
        with allure.step("Obtener el número de productos encontrados"):
            product_count = products.get_product_count()
            print(f"\n*** NÚMERO DE PRODUCTOS ENCONTRADOS: {product_count} ***\n")

        with allure.step("Ordenar por Precio de más alto a más bajo y obtener el nombre y precio de los cinco primeros productos"):
            products.sort_by("price_high_low")
            price_desc_product_info = products.get_first_five_products_info()
            for idx, info in enumerate(price_desc_product_info, start=1):
                print(f"Producto por precio descendente {idx}: {info['name']} - Precio: {info['price']}")

        with allure.step("Ordenar por Nuevos lanzamiento y obtener el nombre y precio de los cinco primeros productos"):
            products.sort_by("newest")
            newest_product_info = products.get_first_five_products_info()
            for idx, info in enumerate(newest_product_info, start=1):
                print(f"Nuevo Producto {idx}: {info['name']} - Precio: {info['price']}")

        with allure.step("Ordenar por Opinión del cliente y obtener el nombre y precio de los cinco primeros productos"):
            products.sort_by("avg_review")
            review_product_info = products.get_first_five_products_info()
            for idx, info in enumerate(review_product_info, start=1):
                print(f"Producto con mejor opinión {idx}: {info['name']} - Precio: {info['price']}")