"""
Script para enviar reporte de pruebas por email después de la ejecución
Se ejecuta como post-build action desde Jenkins
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.utils.email_sender import send_test_report_email

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_pytest_report(report_path: str = "reports") -> dict:
    """
    Parsea el reporte de pytest para extraer resultados
    
    Args:
        report_path: Ruta al directorio de reportes
        
    Returns:
        dict: Diccionario con los resultados
    """
    results = {
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "browser": os.getenv("BROWSER", "chrome"),
        "headless": os.getenv("HEADLESS", "false").lower() == "true",
        "base_url": os.getenv("BASE_URL", "https://www.amazon.com")
    }
    
    # Intentar leer el log de pytest
    log_file = os.path.join(report_path, "test.log")
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read()
                # Buscar patrones en el log
                if "passed" in content.lower():
                    results["passed"] += content.lower().count("passed")
                if "failed" in content.lower():
                    results["failed"] += content.lower().count("failed")
                if "skipped" in content.lower():
                    results["skipped"] += content.lower().count("skipped")
        except Exception as e:
            logger.warning(f"No se pudo leer el log de pruebas: {e}")
    
    # Si no hay resultados en el log, intentar leer desde allure-results
    if results["passed"] == 0 and results["failed"] == 0:
        allure_results = os.path.join(report_path, "allure-results")
        if os.path.exists(allure_results):
            json_files = list(Path(allure_results).glob("*-result.json"))
            results["passed"] = len([f for f in json_files if "result.json" in str(f)])
    
    logger.info(f"Resultados parseados: {results}")
    return results


def main():
    """Función principal"""
    
    # Obtener parámetros de Jenkins
    send_email = os.getenv("SEND_EMAIL", "false").lower() == "true"
    email_recipients = os.getenv("EMAIL_RECIPIENTS", "")
    
    logger.info("=" * 60)
    logger.info("ENVIANDO REPORTE DE PRUEBAS POR EMAIL")
    logger.info("=" * 60)
    logger.info(f"Enviar Email: {send_email}")
    logger.info(f"Destinatarios: {email_recipients}")
    
    # Si no está habilitado el envío de email, salir
    if not send_email or not email_recipients:
        logger.info("Envío de email deshabilitado - Saltando este paso")
        return 0
    
    try:
        # Parsear resultados de las pruebas
        test_results = parse_pytest_report()
        
        # Enviar email
        success = send_test_report_email(
            recipients=email_recipients,
            test_results=test_results,
            report_path="reports"
        )
        
        if success:
            logger.info("✅ Reporte enviado exitosamente")
            return 0
        else:
            logger.error("❌ Fallo al enviar reporte")
            return 1
            
    except Exception as e:
        logger.error(f"❌ Error durante el envío de email: {str(e)}")
        logger.error("Nota: Asegúrate de configurar las variables de entorno:")
        logger.error("  - SENDER_EMAIL: email del remitente")
        logger.error("  - SENDER_PASSWORD: contraseña de la aplicación (no contraseña normal)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
