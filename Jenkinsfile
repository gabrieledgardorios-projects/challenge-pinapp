pipeline {
    agent any
    
    options {
        timestamps()
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    
    parameters {
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Navegador para ejecutar tests')
        booleanParam(name: 'HEADLESS', defaultValue: true, description: 'Ejecutar en modo headless')
        string(name: 'BASE_URL', defaultValue: 'https://www.example.com', description: 'URL del sitio web a probar')
        choice(name: 'TEST_TYPE', choices: ['all', 'smoke', 'regression', 'sanity'], description: 'Tipo de test a ejecutar')
    }
    
    environment {
        PYTHON_ENV = '.venv'
        REPORTS_PATH = 'reports'
    }
    
    stages {
        stage('Preparación') {
            steps {
                script {
                    echo "========== Preparando ambiente =========="
                    echo "Browser: ${params.BROWSER}"
                    echo "Headless: ${params.HEADLESS}"
                    echo "Base URL: ${params.BASE_URL}"
                    echo "Test Type: ${params.TEST_TYPE}"
                }
            }
        }
        
        stage('Setup Python') {
            steps {
                script {
                    echo "========== Instalando dependencias de Python =========="
                    bat '''
                        python -m venv %PYTHON_ENV%
                        call %PYTHON_ENV%\\Scripts\\activate.bat
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }
        
        stage('Ejecutar Tests') {
            steps {
                script {
                    echo "========== Ejecutando tests =========="
                    bat '''
                        call %PYTHON_ENV%\\Scripts\\activate.bat
                        
                        if "%TEST_TYPE%"=="all" (
                            pytest tests/ --browser=%BROWSER% --headless=%HEADLESS% --base-url=%BASE_URL%
                        ) else (
                            pytest tests/ -m %TEST_TYPE% --browser=%BROWSER% --headless=%HEADLESS% --base-url=%BASE_URL%
                        )
                    '''
                }
            }
        }
        
        stage('Generar Reportes HTML') {
            steps {
                script {
                    echo "========== Generando reportes HTML =========="
                    publishHTML([
                        reportDir: 'reports',
                        reportFiles: 'report.html',
                        reportName: 'Test Report'
                    ])
                }
            }
        }
        
        stage('Generar Reportes Allure') {
            steps {
                script {
                    echo "========== Generando reportes Allure =========="
                    bat '''
                        call %PYTHON_ENV%\\Scripts\\activate.bat
                        allure generate reports/allure-results -o reports/allure-report --clean
                    '''
                    publishHTML([
                        reportDir: 'reports/allure-report',
                        reportFiles: 'index.html',
                        reportName: 'Allure Report'
                    ])
                }
            }
        }
        
        stage('Reporte de Cobertura') {
            steps {
                script {
                    echo "========== Publicando cobertura =========="
                    publishHTML([
                        reportDir: 'reports/coverage',
                        reportFiles: 'index.html',
                        reportName: 'Code Coverage Report'
                    ])
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "========== Limpiando =========="
                // Guardar logs
                archiveArtifacts artifacts: 'reports/test.log', allowEmptyArchive: true
                
                // Guardar resultados de Allure
                archiveArtifacts artifacts: 'reports/allure-results/**', allowEmptyArchive: true
                
                // Guardar screenshots de errores
                archiveArtifacts artifacts: 'reports/screenshots/**', allowEmptyArchive: true
            }
        }
        
        success {
            script {
                echo "========== Tests ejecutados exitosamente =========="
            }
        }
        
        failure {
            script {
                echo "========== Tests fallaron =========="
            }
        }
        
        unstable {
            script {
                echo "========== Algunos tests fallaron =========="
            }
        }
    }
}
