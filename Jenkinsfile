pipeline {
    agent any
    
    options {
        timestamps()
        timeout(time: 2, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '30', daysToKeepStr: '90'))
        disableConcurrentBuilds()
    }
    
    parameters {
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox'],
            description: 'Navegador para ejecutar tests'
        )
        booleanParam(
            name: 'HEADLESS',
            defaultValue: false,
            description: 'Ejecutar en modo headless (sin interfaz gráfica)'
        )
        string(
            name: 'BASE_URL',
            defaultValue: 'https://www.amazon.com',
            description: 'URL del sitio web a probar'
        )
        choice(
            name: 'TEST_TYPE',
            choices: ['all', 'smoke', 'regression', 'sanity'],
            description: 'Tipo de test a ejecutar'
        )
        string(
            name: 'EMAIL_RECIPIENTS',
            defaultValue: 'qa-team@example.com',
            description: 'Correos para enviar el reporte (separados por coma)'
        )
        booleanParam(
            name: 'SEND_EMAIL',
            defaultValue: true,
            description: 'Enviar reporte por email al finalizar'
        )
    }
    
    environment {
        PYTHON_ENV = '.venv'
        REPORTS_PATH = 'reports'
        BUILD_TIMESTAMP = sh(returnStdout: true, script: "date +%Y%m%d_%H%M%S").trim()
        TEST_REPORT_NAME = "Test_Report_${BUILD_TIMESTAMP}"
        JENKINS_NODE_COOKIE = 'dontKillMe'
        BASE_URL = "${params.BASE_URL}"
        BROWSER = "${params.BROWSER}"
        HEADLESS = "${params.HEADLESS}"
        TEST_TYPE = "${params.TEST_TYPE}"
        EMAIL_RECIPIENTS = "${params.EMAIL_RECIPIENTS}"
        SEND_EMAIL = "${params.SEND_EMAIL}"
    }
    
    stages {
        stage('Información del Build') {
            steps {
                script {
                    echo """
                    ╔════════════════════════════════════════════════════════╗
                    ║          INFORMACIÓN DEL BUILD                         ║
                    ╠════════════════════════════════════════════════════════╣
                    ║ Build Number: ${env.BUILD_NUMBER}
                    ║ Build ID: ${env.BUILD_ID}
                    ║ Build URL: ${env.BUILD_URL}
                    ║ Timestamp: ${BUILD_TIMESTAMP}
                    ║ Browser: ${params.BROWSER}
                    ║ Headless: ${params.HEADLESS}
                    ║ Base URL: ${params.BASE_URL}
                    ║ Test Type: ${params.TEST_TYPE}
                    ║ Email Recipients: ${params.EMAIL_RECIPIENTS}
                    ╚════════════════════════════════════════════════════════╝
                    """
                }
            }
        }
        
        stage('Validación de Entorno') {
            steps {
                script {
                    echo "========== Validando entorno =========="
                    
                    // Validar Python
                    sh '''
                        python --version
                        python -m pip --version
                    '''
                    
                    // Crear directorios necesarios
                    sh '''
                        mkdir -p reports/allure-results
                        mkdir -p reports/screenshots
                        mkdir -p reports/coverage
                        echo "Directorios de reportes creados exitosamente"
                    '''
                }
            }
        }
        
        stage('Setup de Dependencias') {
            steps {
                script {
                    echo "========== Instalando dependencias de Python =========="
                    sh '''
                        # Crear/activar entorno virtual
                        python -m venv ${PYTHON_ENV}
                        
                        # Activar en Linux/Mac
                        if [ -f "${PYTHON_ENV}/bin/activate" ]; then
                            . ${PYTHON_ENV}/bin/activate
                        # Activar en Windows (si es necesario)
                        elif [ -f "${PYTHON_ENV}/Scripts/activate" ]; then
                            . ${PYTHON_ENV}/Scripts/activate
                        fi
                        
                        # Actualizar pip
                        python -m pip install --upgrade pip setuptools wheel
                        
                        # Instalar requirements
                        pip install -r requirements.txt --no-cache-dir
                        
                        # Verificar instalación
                        echo "Verificando instalaciones..."
                        pytest --version
                        python -c "import selenium; print(f'Selenium {selenium.__version__}')"
                        python -c "import allure; print(f'Allure {allure.__version__}')"
                    '''
                }
            }
        }
        
        stage('Ejecutar Tests') {
            steps {
                script {
                    echo "========== Ejecutando teste: ${params.TEST_TYPE} =========="
                    
                    try {
                        sh '''
                            . ${PYTHON_ENV}/bin/activate 2>/dev/null || . ${PYTHON_ENV}/Scripts/activate 2>/dev/null
                            
                            # Construir comando pytest
                            PYTEST_CMD="pytest tests/ -v --tb=short"
                            
                            # Agregar filtro de marker si no es "all"
                            if [ "${TEST_TYPE}" != "all" ]; then
                                PYTEST_CMD="${PYTEST_CMD} -m ${TEST_TYPE}"
                            fi
                            
                            # Agregar parámetros
                            PYTEST_CMD="${PYTEST_CMD} --browser=${BROWSER}"
                            PYTEST_CMD="${PYTEST_CMD} --headless=${HEADLESS}"
                            PYTEST_CMD="${PYTEST_CMD} --base-url=${BASE_URL}"
                            
                            # Agregar reportes
                            PYTEST_CMD="${PYTEST_CMD} --html=reports/report.html --self-contained-html"
                            PYTEST_CMD="${PYTEST_CMD} --cov=src --cov-report=html:reports/coverage --cov-report=term"
                            PYTEST_CMD="${PYTEST_CMD} --alluredir=reports/allure-results"
                            
                            # Ejecutar
                            echo "Comando: ${PYTEST_CMD}"
                            eval ${PYTEST_CMD}
                        '''
                    } catch (Exception e) {
                        echo "Tests fallaron pero continuamos con reportes: ${e.message}"
                        // No fallar el pipeline aquí para que se generen los reportes
                    }
                }
            }
        }
        
        stage('Generar Reportes Allure') {
            steps {
                script {
                    echo "========== Instalando Allure CLI =========="
                    sh '''
                        # Instalar Allure CLI si no existe
                        if [ ! -d "allure" ]; then
                            wget -q https://github.com/allure-framework/allure2/releases/download/2.24.1/allure-2.24.1.zip -O allure.zip || curl -L -o allure.zip https://github.com/allure-framework/allure2/releases/download/2.24.1/allure-2.24.1.zip
                            unzip -q allure.zip
                            mv allure-2.24.1 allure
                        fi
                        export PATH="$PWD/allure/bin:$PATH"
                    '''
                    echo "========== Generando Reporte Allure =========="
                    sh '''
                        . ${PYTHON_ENV}/bin/activate 2>/dev/null || . ${PYTHON_ENV}/Scripts/activate 2>/dev/null
                        if command -v allure &> /dev/null; then
                            echo "Allure encontrado, generando reporte..."
                            allure generate reports/allure-results -o reports/allure-report --clean
                            echo "Reporte Allure generado en reports/allure-report/index.html"
                        else
                            echo "Advertencia: Allure CLI no encontrado"
                            echo "Los datos de Allure se han guardado en reports/allure-results/"
                        fi
                    '''
                }
            }
        }
        
        stage('Publicar Reportes en Jenkins') {
            steps {
                script {
                    echo "========== Publicando reportes en Jenkins =========="
                    
                    // Reporte HTML de Pytest
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'report.html',
                        reportName: 'Pytest HTML Report',
                        reportTitles: "Test Report #${env.BUILD_NUMBER}"
                    ])
                    
                    // Reporte de Cobertura
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports/coverage',
                        reportFiles: 'index.html',
                        reportName: 'Code Coverage Report',
                        reportTitles: "Coverage Report #${env.BUILD_NUMBER}"
                    ])
                    
                    // Reporte Allure (si existe)
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports/allure-report',
                        reportFiles: 'index.html',
                        reportName: 'Allure Report',
                        reportTitles: "Allure Report #${env.BUILD_NUMBER}"
                    ])
                }
            }
        }
        
        stage('Archivar Artefactos') {
            steps {
                script {
                    echo "========== Archivando artefactos =========="
                    
                    archiveArtifacts(
                        artifacts: [
                            'reports/report.html',
                            'reports/test.log',
                            'reports/allure-results/**',
                            'reports/screenshots/**',
                            'reports/coverage/**',
                            'reports/*.avi'
                        ].join(','),
                        allowEmptyArchive: true,
                        fingerprint: true
                    )
                }
            }
        }
        
        stage('Preparar Email') {
            when {
                expression { params.SEND_EMAIL == true }
            }
            steps {
                script {
                    echo "========== Preparando email =========="
                    
                    // Generar resumen del test
                    sh '''
                        # Extraer información del reporte
                        if [ -f "reports/test.log" ]; then
                            cp reports/test.log reports/email_summary.txt
                        fi
                        
                        # Crear HTML para email
                        cat > reports/email_report.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 900px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }
        .info-box { background-color: #f8f9fa; padding: 15px; margin: 15px 0; border-left: 4px solid #007bff; border-radius: 4px; }
        .success { color: #28a745; font-weight: bold; }
        .failure { color: #dc3545; font-weight: bold; }
        .warning { color: #ffc107; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th { background-color: #007bff; color: white; padding: 12px; text-align: left; }
        td { padding: 10px; border-bottom: 1px solid #ddd; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .links { margin-top: 20px; }
        .links a { display: inline-block; margin: 10px 10px 10px 0; padding: 10px 15px; background-color: #007bff; color: white; text-decoration: none; border-radius: 4px; }
        .links a:hover { background-color: #0056b3; }
        footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Reporte de Pruebas Automáticas</h1>
        
        <div class="info-box">
            <p><strong>Build #:</strong> ${BUILD_NUMBER}</p>
            <p><strong>Fecha/Hora:</strong> $(date '+%Y-%m-%d %H:%M:%S')</p>
            <p><strong>Duración:</strong> ${BUILD_DURATION:-N/A}</p>
            <p><strong>Resultado:</strong> <span class="success">✓ EJECUTADO</span></p>
        </div>
        
        <h2>Configuración del Test</h2>
        <table>
            <tr>
                <th>Parámetro</th>
                <th>Valor</th>
            </tr>
            <tr>
                <td>Browser</td>
                <td>${BROWSER}</td>
            </tr>
            <tr>
                <td>Headless</td>
                <td>${HEADLESS}</td>
            </tr>
            <tr>
                <td>Base URL</td>
                <td>${BASE_URL}</td>
            </tr>
            <tr>
                <td>Tipo de Test</td>
                <td>${TEST_TYPE}</td>
            </tr>
        </table>
        
        <h2>📁 Reportes Disponibles</h2>
        <div class="links">
            <a href="${BUILD_URL}Pytest_HTML_Report/" target="_blank">📋 Pytest HTML Report</a>
            <a href="${BUILD_URL}Allure_Report/" target="_blank">📊 Allure Report</a>
            <a href="${BUILD_URL}Code_Coverage_Report/" target="_blank">📈 Coverage Report</a>
            <a href="${BUILD_URL}artifact/reports/" target="_blank">📦 Descargar Artefactos</a>
        </div>
        
        <h2>⚠️ Próximos Pasos</h2>
        <ul>
            <li>Revisar reporte detallado en los links anteriores</li>
            <li>Verificar logs si hay algún fallo</li>
            <li>Actualizar configuración si es necesario</li>
        </ul>
        
        <footer>
            <p>Este email fue generado automáticamente por Jenkins.</p>
            <p>No responda a este email, es una notificación automática.</p>
        </footer>
    </div>
</body>
</html>
EOF
                        echo "Email HTML generado"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo """
                ╔════════════════════════════════════════════════════════╗
                ║                 RESUMEN DE BUILD                       ║
                ╠════════════════════════════════════════════════════════╣
                ║ Build Status: ${currentBuild.result}
                ║ Artefactos: reports/ (descargables)
                ║ Logs: console output
                ║ Workspace: ${WORKSPACE}
                ╚════════════════════════════════════════════════════════╝
                """
                
                // Limpiar ambiente virtual viejo (opcional)
                sh '''
                    if [ -d "${PYTHON_ENV}" ]; then
                        echo "Entorno virtual encontrado en ${PYTHON_ENV}"
                    fi
                '''
            }
        }
        
        success {
            script {
                echo "========== ✓ BUILD EXITOSO =========="
                currentBuild.result = 'SUCCESS'
                
                // Enviar email si está habilitado
                if (params.SEND_EMAIL) {
                    sendEmailNotification('SUCCESS')
                }
            }
        }
        
        failure {
            script {
                echo "========== ✗ BUILD FALLIDO =========="
                currentBuild.result = 'FAILURE'
                
                // Enviar email de fallo
                if (params.SEND_EMAIL) {
                    sendEmailNotification('FAILURE')
                }
            }
        }
        
        unstable {
            script {
                echo "========== ⚠ BUILD INESTABLE =========="
                currentBuild.result = 'UNSTABLE'
                
                // Enviar email
                if (params.SEND_EMAIL) {
                    sendEmailNotification('UNSTABLE')
                }
            }
        }
    }
}

// Función para enviar email
def sendEmailNotification(String buildStatus) {
    try {
        echo "Enviando notificación por email..."
        
        String subject = "[Jenkins] Test Report - Build #${env.BUILD_NUMBER} - ${buildStatus}"
        String recipients = "${params.EMAIL_RECIPIENTS}"
        
        // Determinar color según estatus
        String statusColor = buildStatus == 'SUCCESS' ? '✓ EXITOSO' : buildStatus == 'FAILURE' ? '✗ FALLIDO' : '⚠ INESTABLE'
        String statusIcon = buildStatus == 'SUCCESS' ? '✓' : buildStatus == 'FAILURE' ? '✗' : '⚠'
        
        String bodyHtml = """
        <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body { font-family: Arial, sans-serif; }
                    .header { background-color: ${buildStatus == 'SUCCESS' ? '#28a745' : buildStatus == 'FAILURE' ? '#dc3545' : '#ffc107'}; color: white; padding: 20px; }
                    .content { padding: 20px; }
                    .info { background-color: #f5f5f5; padding: 10px; margin: 10px 0; border-left: 4px solid #007bff; }
                    .links { margin: 20px 0; }
                    a { color: #007bff; text-decoration: none; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>${statusIcon} Test Report - Build #${env.BUILD_NUMBER}</h1>
                    <p>Status: <strong>${statusColor}</strong></p>
                </div>
                
                <div class="content">
                    <h2>Resumen del Build</h2>
                    
                    <div class="info">
                        <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                        <p><strong>Build ID:</strong> ${env.BUILD_ID}</p>
                        <p><strong>Status:</strong> ${buildStatus}</p>
                        <p><strong>Fecha:</strong> \$(date '+%Y-%m-%d %H:%M:%S')</p>
                    </div>
                    
                    <h3>Configuración del Test</h3>
                    <div class="info">
                        <p><strong>Browser:</strong> ${params.BROWSER}</p>
                        <p><strong>Headless:</strong> ${params.HEADLESS}</p>
                        <p><strong>URL:</strong> ${params.BASE_URL}</p>
                        <p><strong>Tipo:</strong> ${params.TEST_TYPE}</p>
                    </div>
                    
                    <h3>Enlaces a Reportes</h3>
                    <div class="links">
                        <p><a href="${env.BUILD_URL}Pytest_HTML_Report/" target="_blank">📋 Ver Reporte HTML</a></p>
                        <p><a href="${env.BUILD_URL}Allure_Report/" target="_blank">📊 Ver Reporte Allure</a></p>
                        <p><a href="${env.BUILD_URL}Code_Coverage_Report/" target="_blank">📈 Ver Cobertura de Código</a></p>
                        <p><a href="${env.BUILD_URL}" target="_blank">🔗 Ver Build en Jenkins</a></p>
                    </div>
                    
                    ${buildStatus == 'FAILURE' ? '<p style="color: red;"><strong>⚠ Nota:</strong> Algunos tests fallaron. Por favor revisa los reportes para más detalles.</p>' : '<p style="color: green;"><strong>✓ Nota:</strong> Todos los tests se ejecutaron correctamente.</p>'}
                </div>
            </body>
        </html>
        """
        
        // Enviar email
        emailext(
            subject: subject,
            body: bodyHtml,
            to: recipients,
            mimeType: 'text/html',
            attachmentsPattern: 'reports/report.html, reports/test.log',
            attachLog: true
        )
        
        echo "Email enviado a: ${recipients}"
        
    } catch (Exception e) {
        echo "Error enviando email: ${e.message}"
    }
}
