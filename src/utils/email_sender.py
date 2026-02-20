"""
Email Sender - Envía reportes de pruebas por correo electrónico
"""

import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from datetime import datetime
from pathlib import Path
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailSender:
    """Clase para enviar reportes de pruebas por email"""
    
    def __init__(self, sender_email: str = None, sender_password: str = None, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        """
        Inicializar el enviador de email
        
        Args:
            sender_email: Email del remitente (si None, usa variable de entorno SENDER_EMAIL)
            sender_password: Contraseña del email (si None, usa variable de entorno SENDER_PASSWORD)
            smtp_server: Servidor SMTP (default: Gmail)
            smtp_port: Puerto SMTP (default: 587)
        """
        self.sender_email = sender_email or os.getenv("SENDER_EMAIL", "test-jenkins@gmail.com")
        self.sender_password = sender_password or os.getenv("SENDER_PASSWORD", "")
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_test_report(self, recipients: list, test_results: dict, report_path: str = "reports"):
        """
        Envía reporte de pruebas por email
        
        Args:
            recipients: Lista de emails destinatarios ["email1@example.com", "email2@example.com"]
            test_results: Diccionario con resultados de pruebas
            report_path: Ruta al directorio de reportes
            
        Returns:
            bool: True si se envió exitosamente, False si falló
        """
        try:
            logger.info(f"Preparando email para: {', '.join(recipients)}")
            
            # Crear mensaje
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = ", ".join(recipients)
            message["Date"] = formatdate(localtime=True)
            message["Subject"] = self._create_subject(test_results)
            
            # Crear cuerpo del email
            body = self._create_email_body(test_results)
            message.attach(MIMEText(body, "html"))
            
            # Adjuntar reportes
            self._attach_reports(message, report_path)
            
            # Enviar email
            self._send_smtp(message, recipients)
            
            logger.info("✅ Email enviado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error al enviar email: {str(e)}")
            return False
    
    def _create_subject(self, test_results: dict) -> str:
        """Crear asunto del email"""
        status = "✅ PASS" if test_results.get("passed", 0) > 0 else "❌ FAIL"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        return f"[{status}] Reporte de Pruebas - {timestamp}"
    
    def _create_email_body(self, test_results: dict) -> str:
        """Crear cuerpo del email en HTML"""
        passed = test_results.get("passed", 0)
        failed = test_results.get("failed", 0)
        skipped = test_results.get("skipped", 0)
        browser = test_results.get("browser", "chrome")
        headless = test_results.get("headless", False)
        base_url = test_results.get("base_url", "https://www.amazon.com")
        
        total = passed + failed + skipped
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; }}
                h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
                .summary {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .metric {{ display: inline-block; margin-right: 30px; }}
                .metric-value {{ font-size: 24px; font-weight: bold; }}
                .metric-label {{ color: #666; font-size: 12px; }}
                .passed {{ color: #28a745; }}
                .failed {{ color: #dc3545; }}
                .skipped {{ color: #ffc107; }}
                .config {{ background-color: #e9ecef; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .config-item {{ margin: 5px 0; }}
                .footer {{ color: #666; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Reporte de Pruebas Automatizadas</h1>
                
                <div class="summary">
                    <h2>📈 Resumen de Resultados</h2>
                    <div class="metric">
                        <div class="metric-value passed">{passed}</div>
                        <div class="metric-label">Sesiones Exitosas</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value failed">{failed}</div>
                        <div class="metric-label">Fallos</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value skipped">{skipped}</div>
                        <div class="metric-label">Omitidas</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{pass_rate:.1f}%</div>
                        <div class="metric-label">Tasa de Éxito</div>
                    </div>
                </div>
                
                <div class="config">
                    <h2>⚙️ Configuración de Pruebas</h2>
                    <div class="config-item"><strong>Navegador:</strong> {browser}</div>
                    <div class="config-item"><strong>Modo Headless:</strong> {'Sí' if headless else 'No'}</div>
                    <div class="config-item"><strong>URL Base:</strong> {base_url}</div>
                    <div class="config-item"><strong>Fecha/Hora:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                </div>
                
                <p>Consulta los reportes adjuntos para más detalles.</p>
                
                <div class="footer">
                    <p>Este es un correo automático generado por el sistema de pruebas automatizadas de Amazon.</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def _attach_reports(self, message: MIMEMultipart, report_path: str):
        """Adjuntar archivos de reporte"""
        if not os.path.exists(report_path):
            logger.warning(f"Directorio de reportes no encontrado: {report_path}")
            return
        
        # Adjuntar HTML report
        html_report = os.path.join(report_path, "report.html")
        if os.path.exists(html_report):
            try:
                with open(html_report, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    part.add_header("Content-Disposition", f"attachment; filename= report.html")
                    message.attach(part)
                    logger.info("✓ Reporte HTML adjuntado")
            except Exception as e:
                logger.warning(f"No se pudo adjuntar report.html: {e}")
        
        # Crear un archivo ZIP con los reportes de Allure
        self._attach_allure_report(message, report_path)
    
    def _attach_allure_report(self, message: MIMEMultipart, report_path: str):
        """Crear y adjuntar un ZIP con el reporte de Allure"""
        try:
            allure_results = os.path.join(report_path, "allure-results")
            if os.path.exists(allure_results):
                # Crear ZIP de los resultados
                zip_path = os.path.join(report_path, "allure-results.zip")
                shutil.make_archive(
                    os.path.join(report_path, "allure-results"),
                    "zip",
                    allure_results
                )
                
                if os.path.exists(zip_path):
                    with open(zip_path, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                        part.add_header("Content-Disposition", f"attachment; filename= allure-results.zip")
                        message.attach(part)
                        logger.info("✓ Reporte Allure adjuntado (ZIP)")
        except Exception as e:
            logger.warning(f"No se pudo adjuntar reporte Allure: {e}")
    
    def _send_smtp(self, message: MIMEMultipart, recipients: list):
        """Enviar mensaje via SMTP"""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipients, message.as_string())
                logger.info(f"✓ Conexión SMTP exitosa - Email enviado a {len(recipients)} destinatario(s)")
        except smtplib.SMTPAuthenticationError:
            logger.error("❌ Error de autenticación SMTP. Verifica tu email y contraseña")
            raise
        except smtplib.SMTPException as e:
            logger.error(f"❌ Error SMTP: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"❌ Error al enviar email: {str(e)}")
            raise


def send_test_report_email(
    recipients: str,
    test_results: dict,
    report_path: str = "reports",
    sender_email: str = None,
    sender_password: str = None
):
    """
    Función de utilidad para enviar reportes de pruebas
    
    Args:
        recipients: String de emails separados por coma
        test_results: Diccionario con resultados
        report_path: Ruta al directorio de reportes
        sender_email: Email del remitente
        sender_password: Contraseña del email
    """
    # Parsear destinatarios
    recipient_list = [email.strip() for email in recipients.split(",") if email.strip()]
    
    if not recipient_list:
        logger.warning("No hay destinatarios válidos")
        return False
    
    # Crear enviador y enviar
    sender = EmailSender(sender_email, sender_password)
    return sender.send_test_report(recipient_list, test_results, report_path)


if __name__ == "__main__":
    # Ejemplo de uso
    test_results = {
        "passed": 5,
        "failed": 1,
        "skipped": 2,
        "browser": "chrome",
        "headless": False,
        "base_url": "https://www.amazon.com"
    }
    
    send_test_report_email(
        recipients="test@example.com",
        test_results=test_results,
        report_path="reports"
    )
