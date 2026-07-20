"""
Network Vulnerability Scanner - Main Application Entry Point
Windows-based executable for network reconnaissance and vulnerability detection
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication
from ui.main_window import ScannerWindow
from config.settings import AppSettings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vuln_scanner.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Initialize and run the application"""
    try:
        logger.info("Starting Network Vulnerability Scanner")
        
        # Initialize application
        app = QApplication(sys.argv)
        app.setApplicationName("Network Vulnerability Scanner")
        app.setApplicationVersion("1.0.0")
        
        # Load settings
        settings = AppSettings()
        settings.load()
        
        # Create and show main window
        window = ScannerWindow(settings)
        window.show()
        
        logger.info("Application window displayed successfully")
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Fatal error starting application: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
