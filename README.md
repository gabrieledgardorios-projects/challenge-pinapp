# Automatización de Pruebas Web - Amazon.com Testing Framework

## 📋 Descripción General

Framework robusto que automatiza flujos de búsqueda en Amazon.com con:
- ✅ **Grabación automática de video** (bajo consumo de CPU)
- ✅ **Filtrado dinámico** por marca y precio con verificación
- ✅ **Extracción de datos** de productos (nombres, precios, opciones)
- ✅ **Ordenamiento flexible** (5 opciones: precio, reseñas, fecha, relevancia)
- ✅ **Page Object Model** para máxima mantenibilidad
- ✅ **Reportes** completos (HTML, Allure, Coverage)
- ✅ **Jenkins CI/CD** con notificaciones por email

### Stack Tecnológico

| Componente | Versión | Uso |
|-----------|---------|-----|
| Python | 3.12.7 | Lenguaje |
| Selenium | 4.15.2 | Automatización |
| Pytest | 7.4.3 | Testing |
| OpenCV | 4.8+ | Grabación video |
| Allure | 2.13.2 | Reportes |
| WebDriver Manager | 4.0+ | ChromeDriver automático |

## 📋 Requisitos Previos

```
Python 3.12.7
pip (gestor de paquetes)
Git (opcional)
```

### Dependencias Clave
```
selenium>=4.15.2
pytest>=7.4.3
pytest-html>=4.1.1
pytest-cov>=4.1.0
allure-pytest>=2.13.2
opencv-python>=4.8.0
numpy>=1.24.0
pillow>=10.0.0
webdriver-manager>=4.0.0
```

## 🛠️ Instalación y Configuración

### 1. Clonar o descargar el proyecto

```bash
cd Challenge
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Verificar instalación

```bash
pytest --version
python -c "import selenium; print(selenium.__version__)"
python -c "import allure; print(allure.__version__)"
```

## 📁 Estructura del Proyecto

```
Challenge/
├── config/
│   ├── config.py                    # Configuración centralizada (URLs, timeouts, etc.)
│   └── __pycache__/
├── src/
│   ├── base.py                      # DriverFactory y BasePage (métodos reutilizables)
│   ├── pages/
│   │   ├── home_page.py            # Page Object para página principal
│   │   ├── product_results_page.py # Page Object para resultados (CORE)
│   │   └── __pycache__/
│   ├── utils/
│   │   ├── video_recorder.py       # Clase VideoRecorder para grabación
│   │   └── __init__.py
│   └── __init__.py
├── tests/
│   ├── conftest.py                  # Fixtures de pytest (driver, video_recorder)
│   ├── test_get_products.py        # Test case principal
│   └── __pycache__/
├── reports/                         # Se genera automáticamente
│   ├── report.html                 # Reporte Pytest
│   ├── allure-results/             # Datos para Allure
│   ├── coverage/                   # Cobertura de código
│   ├── screenshots/                # Screenshots en fallos
│   ├── *.avi                       # Videos de test grabados
│   └── test.log                    # Logs detallados
├── .gitignore                       # Archivo de git ignore
├── Jenkinsfile                      # Pipeline para Jenkins CI/CD
├── pytest.ini                       # Configuración de Pytest
├── requirements.txt                 # Dependencias
└── README.md                        # Este archivo
```

## ▶️ Ejecución de Tests

### Ejecutar test específico (recomendado para ver grabación)

```bash
.\.venv\Scripts\python -m pytest tests/test_get_products.py::TestGetProducts::test_get_information_of_products -v -s
```

**Parámetros explicados:**
- `-v`: Verbose (salida detallada)
- `-s`: Show print statements (mostrar logs en consola)

### Ejecutar todos los tests

```bash
.\.venv\Scripts\python -m pytest tests/ -v
```

### Ejecutar con opciones personalizadas

```bash
# Browser específico
pytest tests/ --browser=chrome

# Completamente visible (sin headless)
pytest tests/ --headless=False

# URL personalizada
pytest tests/ --base-url=https://www.amazon.com
```

## 🎥 Video Recording

La grabación es **completamente automática**:
- Se inicia con cada test, se detiene al finalizar
- 5 FPS (bajo consumo CPU), resolución nativa
- Ubicación: `reports/test_name_timestamp.avi` (~15 MB)
- Compatible con VLC, Windows Media Player

Ver video:
```bash
# Windows
start reports/test_get_information_of_products_*.avi
```

## 📊 Reportes

- **HTML Report**: `reports/report.html` (Estado, duración, logs, cobertura)
- **Allure Report**: `allure serve reports/allure-results` (Interactivo, tendencias, videos)
- **Coverage Report**: `reports/coverage/index.html` (~76% cobertura global)

**Page Object Model (POM):**
- BasePage: Métodos comunes (click, send_keys, get_text, etc.)
- HomePage: Operación inicial y búsqueda
- ProductResultsPage: Filtrado, ordenamiento, extracción

**Flujo:**
```
Inicio → VideoRecorder inicia → WebDriver crea → 
Búsqueda → Filtros (marca/precio) → Ordenamiento → 
Extracción datos → VideoRecorder detiene → Reportes
```

**Manejo de Elementos Duplicados:**
```xpath
# Usa aria-hidden para seleccionar solo el elemento visible
//div[@aria-hidden='false']//*[@id='s-result-sort-select_2']
```

## 🚀 Integración CI/CD con Jenkins

### Pasos para ejecutar Jenkins y el job

#### 1. Instalar Java (si no tienes)
Descarga e instala Java 17+ desde https://adoptium.net/

#### 2. Descargar Jenkins WAR
En la raíz del proyecto:
```powershell
Invoke-WebRequest -Uri "https://mirrors.jenkins.io/war-stable/2.479.3/jenkins.war" -OutFile "jenkins.war"
```

#### 3. Ejecutar Jenkins
```powershell
java -jar jenkins.war --httpPort=8080
```
Abre tu navegador en http://localhost:8080

#### 4. Primer acceso
Jenkins te pedirá una contraseña inicial:
```
C:\Users\TU_USUARIO\.jenkins\secrets\initialAdminPassword
```
Usa el usuario `admin` y esa contraseña.

#### 5. Crear un Job Freestyle
1. Click en "New Item"
2. Nombre: `Amazon-Test-Job`
3. Selecciona "Freestyle job"
4. Click OK

#### 6. Configurar parámetros
Marca "This project is parameterized" y agrega:
- **BROWSER** (Choice): chrome, firefox
- **HEADLESS** (Boolean): false
- **BASE_URL** (String): https://www.amazon.com
- **TEST_TYPE** (Choice): all, smoke, regression, sanity
- **EMAIL_RECIPIENTS** (String): tu@correo.com
- **SEND_EMAIL** (Boolean): false

#### 7. Build step (Execute Windows batch command)
Pega este comando:
```batch
@echo off
cd /d C:\Users\TU_USUARIO\OneDrive\Escritorio\Challenge
call .venv\Scripts\activate.bat
pip install -r requirements.txt

set BROWSER=%BROWSER%
set HEADLESS=%HEADLESS%
set BASE_URL=%BASE_URL%
set SEND_EMAIL=%SEND_EMAIL%
set EMAIL_RECIPIENTS=%EMAIL_RECIPIENTS%

if "%HEADLESS%"=="true" (
   pytest tests/ -v --browser=%BROWSER% --headless --base-url=%BASE_URL% --alluredir=reports/allure-results
) else (
   pytest tests/ -v --browser=%BROWSER% --base-url=%BASE_URL% --alluredir=reports/allure-results
)

allure generate reports/allure-results -o reports/allure-report --clean
python send_email_report.py

echo.
echo ========== RESUMEN DEL BUILD ==========
echo Browser: %BROWSER%
echo Headless: %HEADLESS%
echo Base URL: %BASE_URL%
echo Send Email: %SEND_EMAIL%
echo Email Recipients: %EMAIL_RECIPIENTS%
echo ======================================
```

#### 8. Configurar variables de entorno para email
En Jenkins → Manage Jenkins → Configure System → Global properties → Environment variables:
- `SENDER_EMAIL`: tu_email@gmail.com
- `SENDER_PASSWORD`: contraseña de aplicación (no la normal)

#### 9. Ejecutar el job
Click en "Build with Parameters", selecciona valores y ejecuta.

#### 10. Resultado
- Reportes generados en `reports/`
- Email enviado si `SEND_EMAIL` está activado
- Artefactos descargables: logs, videos, screenshots

---

### Troubleshooting
- Si el email no se envía: revisa variables de entorno, credenciales, y configuración SMTP.
- Si Jenkins no arranca: revisa versión de Java y puerto 8080.
- Si Allure no funciona: instala Allure CLI y verifica PATH.

---

### Ejemplo de ejecución local
```powershell
pytest tests/ --browser=chrome --headless --base-url=https://www.amazon.com --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean
python send_email_report.py
```

---

### Parámetros del job
| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| BROWSER | Choice | chrome | Navegador: chrome o firefox |
| HEADLESS | Boolean | false | Ejecutar sin interfaz gráfica |
| BASE_URL | String | https://www.amazon.com | URL del sitio a probar |
| TEST_TYPE | Choice | all | Tipo de test: all, smoke, regression, sanity |
| EMAIL_RECIPIENTS | String | qa-team@example.com | Email para notificaciones |
| SEND_EMAIL | Boolean | false | Activar notificaciones por email |

#### 📋 Stages del Pipeline

1. **Información del Build**
   - Muestra todos los parámetros y configuración
   - Genera timestamp único para el build

2. **Validación de Entorno**
   - Verifica Python, pip y dependencias
   - Crea directorios necesarios para reportes

3. **Setup de Dependencias**
   - Crea entorno virtual aislado
   - Instala requirements.txt
   - Verifica instalaciones críticas

4. **Ejecutar Tests**
   - Ejecuta pytest con parámetros configurados
   - Genera reportes HTML, Allure y Cobertura
   - Maneja fallos sin interrumpir el pipeline

5. **Generar Reportes Allure**
   - Crea visualización interactiva de Allure
   - Fallback si Allure CLI no está disponible

6. **Publicar Reportes en Jenkins**
   - Publica 3 reportes HTML en Jenkins:
     - Pytest HTML Report
     - Code Coverage Report
     - Allure Report (si disponible)

7. **Archivar Artefactos**
   - Guarda logs, screenshots, videos
   - Permite descargar para análisis posterior

8. **Preparar Email**
   - Genera HTML profesional para email
   - Incluye links a todos los reportes
   - Se ejecuta si SEND_EMAIL=true

### 📧 Configuración de Email en Jenkins

#### Requisitos Previos

1. **Plugin instalado**: Email Extension Plugin
   ```
   Manage Jenkins → Manage Plugins → Email Extension Plugin (marcar y instalar)
   ```

2. **Configurar servidor SMTP en Jenkins**:
   ```
   Manage Jenkins → Configure System → Email Notification
   ```
   
   Configuración mínima:
   ```
   SMTP Server: smtp.gmail.com (o tu servidor)
   SMTP Port: 587
   Username: tu-correo@gmail.com
   Password: tu-contraseña-de-app
   Use TLS: ✓ (marcado)
   ```

#### Configurar Credenciales (Recomendado)

Si usas Gmail con 2FA:

1. Generar "App Password" en Google:
   - Ir a https://myaccount.google.com/security
   - Buscar "Contraseñas de aplicación"
   - Generar contraseña para Jenkins
   - Usar esa contraseña en la configuración

#### Verificar Configuración SMTP

```groovy
// En Jenkins Console (Script Console):
def proc = "mail -s 'Test' correo@example.com".execute()
proc << "Test message"
proc.waitFor()
```

### 🚀 Crear un Job de Jenkins

#### Opción 1: Pipeline Job (Recomendado)

1. **En Jenkins Dashboard**:
   - Click en "New Item"
   - Nombre: `Amazon-Product-Tests`
   - Seleccionar: "Pipeline"
   - Click OK

2. **Configuración**:
   ```
   Definition: Pipeline script from SCM
   SCM: Git
   Repository URL: https://github.com/tu-usuario/Challenge.git
   Credentials: (si es privado)
   Branch: */main (o tu rama)
   Script Path: Jenkinsfile
   ```

3. **Build Triggers** (Opcional):
   ```
   - Poll SCM: H/30 * * * * (cada 30 minutos)
   - GitHub hook trigger (si usas GitHub)
   ```

4. **Post-build Actions**:
   ✓ (Automático en el Jenkinsfile)

5. **Guardar y ejecutar**

#### Opción 2: Job de Archivo Declarativo

1. **Crear nuevo Job**:
   - Tipo: "Cambiar a Pipeline"
   - Script:
   ```groovy
   @Library('shared-library') _
   
   def buildResult = build(
       job: 'Amazon-Product-Tests',
       parameters: [
           string(name: 'BROWSER', value: 'chrome'),
           booleanParam(name: 'HEADLESS', value: false),
           string(name: 'BASE_URL', value: 'https://www.amazon.com')
       ]
   )
   ```

### 🏃 Ejecutar Tests desde Jenkins

#### Ejecución Manual

1. Click en "Build with Parameters"
2. Llenar los parámetros deseados:
   - Browser: chrome
   - Headless: false
   - Base URL: https://www.amazon.com
   - Test Type: all
   - Email Recipients: tu@correo.com
3. Click "Build"

#### Resultado de la Ejecución

Una vez completado el build:

- ✅ **Reportes visibles en Jenkins UI**:
  - "Pytest HTML Report" tab
  - "Code Coverage Report" tab
  - "Allure Report" tab

- 📧 **Email enviado** (si SEND_EMAIL=true):
  - Status del build
  - Links a los reportes
  - Attachments: report.html y test.log

- 📦 **Artefactos descargables**:
  - Logs
  - Videos (.avi)
  - Screenshots
  - Resultados de Allure

### 📊 Email Enviado

Email con status del build, links a reportes (HTML, Allure, Coverage) y archivos adjuntos (report.html, test.log).

**Troubleshooting Email:**
- **Error "Email not sent"**: Verificar plugin "Email Extension" instalado + SMTP configurado + puertos abiertos
- **Error "Python not found"**: Configurar PATH en Jenkins → Configure System → Global properties