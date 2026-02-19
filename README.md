# Proyecto de Pruebas Automatizadas con Selenium y Pytest

Proyecto de automatización de pruebas para sitios web utilizando Selenium, Pytest e integración con Jenkins CI/CD.

## 🚀 Características

- ✅ Framework Selenium para automatización de navegador
- ✅ Pytest como framework de testing
- ✅ Page Object Model (POM) para mejor mantenimiento
- ✅ Configuración centralizada con variables de entorno
- ✅ Reportes HTML con pytest-html
- ✅ Cobertura de código con pytest-cov
- ✅ Integración con Jenkins (Jenkinsfile incluido)
- ✅ Markers para ejecutar tipos específicos de tests
- ✅ Logging completo y gestión de screenshots
- ✅ Webdriver Manager para gestión automática de drivers

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para control de versiones)
- Jenkins (para CI/CD)

## 🛠️ Instalación

### 1. Clonar o descargar el proyecto

```bash
cd Challenge
```

### 2. Crear entorno virtual

```bash
# En Windows
python -m venv .venv
.venv\Scripts\activate

# En Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con la configuración deseada
```

## 📁 Estructura del Proyecto

```
Challenge/
├── config/
│   └── config.py              # Configuración centralizada
├── src/
│   ├── base.py                # Clases base (DriverFactory, BasePage)
│   └── pages.py               # Page Objects (HomePage, etc.)
├── tests/
│   ├── conftest.py            # Configuración de fixtures de pytest
│   └── test_home.py           # Test cases de ejemplo
├── reports/                   # Reportes y logs (generado automáticamente)
├── .env.example               # Plantilla de variables de entorno
├── .gitignore                 # Archivo git ignore
├── Jenkinsfile                # Pipeline para Jenkins
├── pytest.ini                 # Configuración de pytest
├── requirements.txt           # Dependencias de Python
└── README.md                  # Este archivo
```

## ▶️ Ejecución de Tests

### Ejecutar todos los tests

```bash
pytest tests/
```

### Ejecutar tests con opción específica de navegador

```bash
# Chrome (por defecto)
pytest tests/ --browser=chrome

# Firefox
pytest tests/ --browser=firefox

# Modo headless
pytest tests/ --headless
```

### Ejecutar tests específicos por marker

```bash
# Tests de humo (smoke tests)
pytest tests/ -m smoke

# Tests de regresión
pytest tests/ -m regression

# Tests de sanidad
pytest tests/ -m sanity

# Tests críticos
pytest tests/ -m critical
```

### Ejecutar test específico

```bash
pytest tests/test_home.py::TestHomePage::test_page_title
```

### Con URL personalizada

```bash
pytest tests/ --base-url=https://www.tudominio.com
```

## 📊 Reportes

Los reportes se generan automáticamente en la carpeta `reports/`:

- **report.html** - Reporte HTML de tests
- **allure-report/** - Reporte Allure interactivo (mejor visualización)
- **coverage/** - Reporte de cobertura de código
- **screenshots/** - Screenshots en caso de fallos
- **test.log** - Archivo de log detallado

### Generar Reporte Allure

```bash
# Después de ejecutar los tests
allure serve reports/allure-results
```

Esto abrirá un servidor local con el reporte interactivo de Allure en el navegador.

Para visualizar el reporte HTML tradicional:

```bash
# En Windows
start reports/report.html

# En Linux/Mac
open reports/report.html
```

## 🏗️ Estructura del Código

### Page Object Model (POM)

```python
from src.pages import HomePage
from src.base import DriverFactory

driver = DriverFactory.create_driver()
home = HomePage(driver)
home.load()
home.search("término de búsqueda")
```

### Decoradores de Allure en Tests

```python
import pytest
import allure
from src.pages import HomePage

@allure.feature("Home Page")
@allure.story("Page Load")
class TestHomePage:
    
    @pytest.mark.smoke
    @allure.title("Verificar título de página")
    @allure.description("Valida que el título sea correcto")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_page_title(self, driver):
        """Verifica que el título de la página sea correcto"""
        with allure.step("Cargar página"):
            home = HomePage(driver)
            home.load()
        
        with allure.step("Obtener título"):
            title = home.get_page_title()
        
        with allure.step("Validar"):
            assert title, "Título vacío"
        
        allure.attach(title, name="Page Title", 
                     attachment_type=allure.attachment_type.TEXT)
```

### Crear nuevos Page Objects

```python
from selenium.webdriver.common.by import By
from src.base import BasePage

class ProductPage(BasePage):
    PRODUCT_TITLE = (By.CLASS_NAME, "product-title")
    ADD_TO_CART = (By.ID, "add-cart-btn")
    
    def get_product_title(self):
        return self.get_text(self.PRODUCT_TITLE)
    
    def add_product_to_cart(self):
        self.click(self.ADD_TO_CART)
```

### Crear nuevos Tests

```python
import pytest
from src.pages import ProductPage

class TestProductPage:
    @pytest.mark.smoke
    def test_product_title_visible(self, driver):
        product = ProductPage(driver)
        assert product.get_product_title(), "Título no encontrado"
```

## 🔗 Integración con Jenkins

### Configurar Pipeline en Jenkins

1. Crear nuevo Job (Pipeline)
2. Seleccionar "Pipeline script from SCM"
3. Seleccionar Git como SCM
4. Ingresar la URL del repositorio
5. Especificar la rama (main, develop, etc.)
6. Apuntar al archivo Jenkinsfile

### Parámetros disponibles en Jenkins

- **BROWSER**: chrome o firefox
- **HEADLESS**: true o false
- **BASE_URL**: URL del sitio a probar
- **TEST_TYPE**: all, smoke, regression, sanity

### Ejemplo de ejecución en Jenkins

```groovy
// Los parámetros se pasan automáticamente
// al pipeline desde la UI de Jenkins
```

## 🐛 Debugging

### Ver logs detallados

```bash
pytest tests/ -v --tb=long
```

### Ejecutar sin headless para ver el navegador

```bash
pytest tests/ --headless=False
```

### Aumentar espera explícita en conftest.py

```python
Config.EXPLICIT_WAIT = 30  # segundos
```

## 📝 Mejores Prácticas

1. **Organización**: Mantener un Page Object por cada página
2. **Naming**: Usar nombres descriptivos en test functions
3. **Markers**: Usar markers apropiados (smoke, regression, etc.)
4. **Allure Decoradores**: Usar `@allure.feature`, `@allure.story`, `@allure.severity`
5. **Allure Steps**: Dividir tests en pasos con `with allure.step()`
6. **Attachments**: Adjuntar datos relevantes con `allure.attach()`
7. **Logs**: Aprovechar el logging para debug
8. **Esperas**: Usar WebDriverWait en lugar de sleep
9. **Fixtures**: Reutilizar fixtures de conftest.py
10. **Screenshots**: Capturar automáticamente en caso de fallos

## 🚨 Troubleshooting

### Error: "No module named 'selenium'"

```bash
pip install -r requirements.txt
```

### Error: "Chrome driver not found"

El proyecto usa `webdriver-manager` que descarga automáticamente los drivers.
Si hay problemas, limpiar la caché:

```bash
pip install --upgrade webdriver-manager
```

### Error: "Allure no encontrado"

Instalar Allure Command Line:

```bash
# Windows (requiere Chocolatey)
choco install allure

# Linux
brew install allure

# Manual (Windows/Linux/Mac)
# Descargar desde: https://github.com/allure-framework/allure2/releases
# Extraer y agregar bin a PATH
```

### Tests muy lentos

Aumentar el tamaño de la ventana o reducir timeouts:

```python
# En config/config.py
IMPLICIT_WAIT = 5
EXPLICIT_WAIT = 10
```

## 📚 Referencias

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Allure Report](https://docs.qameta.io/allure/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)
- [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/)

## 📄 Licencia

Este proyecto está disponible bajo la licencia MIT.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Hacer fork del proyecto
2. Crear una rama para la feature (`git checkout -b feature/AmazingFeature`)
3. Commit de los cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## ❓ Preguntas o Problemas

Si tienes preguntas o encuentras problemas, abre un issue en el proyecto.
