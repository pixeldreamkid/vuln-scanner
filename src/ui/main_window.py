"""Main application window"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QProgressBar, QStatusBar, QMenuBar, QMenu
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
import logging
from ui.scan_dialog import ScanDialog
from ui.results_viewer import ResultsViewer
from ui.styles import get_theme_stylesheet
from network.scanner import NetworkScanner
from vulnerabilities.cve_checker import CVEChecker
from vulnerabilities.vulnerability_db import VulnerabilityDatabase

logger = logging.getLogger(__name__)


class ScanThread(QThread):
    """Worker thread for scanning"""
    progress = pyqtSignal(float, str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, scanner, target, ports, arguments):
        super().__init__()
        self.scanner = scanner
        self.target = target
        self.ports = ports
        self.arguments = arguments
    
    def run(self):
        try:
            def progress_callback(value, status):
                self.progress.emit(value, status)
            
            self.scanner.set_progress_callback(progress_callback)
            results = self.scanner.scan_network(
                self.target,
                self.ports,
                self.arguments
            )
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))


class ScannerWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.scanner = NetworkScanner()
        self.vuln_db = VulnerabilityDatabase()
        self.cve_checker = CVEChecker(self.vuln_db)
        self.scan_thread = None
        self.current_results = None
        
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        """Initialize UI components"""
        self.setWindowTitle("Network Vulnerability Scanner")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Create header
        header_layout = QHBoxLayout()
        title = QLabel("Network Vulnerability Scanner")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Create toolbar
        toolbar_layout = QHBoxLayout()
        
        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.start_scan)
        toolbar_layout.addWidget(self.scan_button)
        
        self.stop_button = QPushButton("Stop Scan")
        self.stop_button.clicked.connect(self.stop_scan)
        self.stop_button.setEnabled(False)
        toolbar_layout.addWidget(self.stop_button)
        
        self.export_button = QPushButton("Export Report")
        self.export_button.clicked.connect(self.export_report)
        toolbar_layout.addWidget(self.export_button)
        
        toolbar_layout.addStretch()
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(300)
        toolbar_layout.addWidget(self.progress_bar)
        
        # Create tabs for results
        self.tabs = QTabWidget()
        self.results_viewer = ResultsViewer()
        self.tabs.addTab(self.results_viewer, "Scan Results")
        
        # Assemble layout
        main_layout.addLayout(header_layout)
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self.tabs)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.statusBar().showMessage("Ready")
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Scan", self.start_scan)
        file_menu.addAction("Export Report", self.export_report)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        # Scan menu
        scan_menu = menubar.addMenu("Scan")
        scan_menu.addAction("Quick Scan", lambda: self.start_scan('quick'))
        scan_menu.addAction("Standard Scan", lambda: self.start_scan('standard'))
        scan_menu.addAction("Full Scan", lambda: self.start_scan('full'))
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction("Settings", self.open_settings)
        tools_menu.addAction("CVE Database", self.manage_cve_db)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self.show_about)
        help_menu.addAction("Documentation", self.show_docs)
    
    def apply_theme(self):
        """Apply theme stylesheet"""
        theme = self.settings.get('ui.theme', 'dark')
        self.setStyleSheet(get_theme_stylesheet(theme))
    
    def start_scan(self, scan_type='custom'):
        """Start network scan"""
        dialog = ScanDialog(self.settings, scan_type)
        if dialog.exec():
            target, ports, arguments = dialog.get_scan_parameters()
            self._execute_scan(target, ports, arguments)
    
    def _execute_scan(self, target, ports, arguments):
        """Execute the scan"""
        logger.info(f"Starting scan on target: {target}")
        
        self.scan_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setValue(0)
        self.statusBar().showMessage("Scanning...")
        
        # Create and start scan thread
        self.scan_thread = ScanThread(self.scanner, target, ports, arguments)
        self.scan_thread.progress.connect(self.update_progress)
        self.scan_thread.finished.connect(self.scan_finished)
        self.scan_thread.error.connect(self.scan_error)
        self.scan_thread.start()
    
    def update_progress(self, value, status):
        """Update progress bar"""
        self.progress_bar.setValue(int(value))
        self.statusBar().showMessage(status)
    
    def scan_finished(self, results):
        """Handle scan completion"""
        logger.info("Scan completed")
        self.current_results = results
        
        if results['success']:
            # Analyze results for vulnerabilities
            self.analyze_results(results)
            self.results_viewer.display_results(results)
            self.statusBar().showMessage("Scan complete")
        else:
            self.statusBar().showMessage(f"Scan failed: {results.get('error', 'Unknown error')}")
        
        self.scan_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setValue(100)
    
    def scan_error(self, error_msg):
        """Handle scan error"""
        logger.error(f"Scan error: {error_msg}")
        self.statusBar().showMessage(f"Error: {error_msg}")
        self.scan_button.setEnabled(True)
        self.stop_button.setEnabled(False)
    
    def stop_scan(self):
        """Stop current scan"""
        logger.info("Stopping scan")
        self.scanner.stop_scan()
        if self.scan_thread:
            self.scan_thread.quit()
            self.scan_thread.wait()
        self.scan_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.statusBar().showMessage("Scan stopped")
    
    def analyze_results(self, results):
        """Analyze scan results for vulnerabilities"""
        if results['success']:
            for host_ip, host_data in results['hosts'].items():
                for service in host_data.get('services', []):
                    analysis = self.cve_checker.analyze_service(
                        service.get('name'),
                        service.get('version')
                    )
                    # Store analysis results
                    if 'vulnerabilities' not in host_data:
                        host_data['vulnerabilities'] = {}
                    host_data['vulnerabilities'][f"{service['port']}/{service['protocol']}"] = analysis
    
    def export_report(self):
        """Export scan results as report"""
        if not self.current_results:
            self.statusBar().showMessage("No results to export")
            return
        
        from reporting.report_generator import ReportGenerator
        
        generator = ReportGenerator()
        report_path = generator.generate_html_report(self.current_results)
        
        logger.info(f"Report exported to: {report_path}")
        self.statusBar().showMessage(f"Report exported to: {report_path}")
    
    def open_settings(self):
        """Open settings dialog"""
        self.statusBar().showMessage("Settings not yet implemented")
    
    def manage_cve_db(self):
        """Manage CVE database"""
        self.statusBar().showMessage("CVE database manager not yet implemented")
    
    def show_about(self):
        """Show about dialog"""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "About Network Vulnerability Scanner",
            "Network Vulnerability Scanner v1.0.0\n\n"
            "A comprehensive Windows-based network reconnaissance and vulnerability detection tool.\n\n"
            "© 2026 - All Rights Reserved"
        )
    
    def show_docs(self):
        """Show documentation"""
        self.statusBar().showMessage("See README.md for documentation")
    
    def closeEvent(self, event):
        """Handle application close"""
        if self.scan_thread and self.scan_thread.isRunning():
            self.stop_scan()
        event.accept()
