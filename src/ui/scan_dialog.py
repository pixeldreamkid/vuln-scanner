"""Scan configuration dialog"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QSpinBox, QPushButton, QGroupBox, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt
from utils.validators import validate_subnet, validate_ip_address, parse_target_range


class ScanDialog(QDialog):
    """Dialog for configuring scan parameters"""
    
    SCAN_PRESETS = {
        'quick': {'ports': '21,22,23,25,53,80,110,143,443,445,3306,3389,5432,5900,8080,8443', 'name': 'Quick Scan'},
        'standard': {'ports': '1-10000', 'name': 'Standard Scan'},
        'full': {'ports': '1-65535', 'name': 'Full Scan'},
    }
    
    def __init__(self, settings, scan_type='custom', parent=None):
        super().__init__(parent)
        self.settings = settings
        self.scan_type = scan_type
        self.target = None
        self.ports = None
        self.arguments = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog UI"""
        self.setWindowTitle("Configure Scan")
        self.setGeometry(200, 200, 500, 400)
        
        layout = QVBoxLayout()
        
        # Target group
        target_group = QGroupBox("Target")
        target_layout = QVBoxLayout()
        
        target_label = QLabel("Target (IP, subnet, or range):")
        target_layout.addWidget(target_label)
        
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("e.g., 192.168.1.0/24 or 192.168.1.1-255")
        self.target_input.setText(self.settings.get('network.default_subnet', '192.168.1.0/24'))
        target_layout.addWidget(self.target_input)
        
        target_group.setLayout(target_layout)
        layout.addWidget(target_group)
        
        # Scan type group
        scan_type_group = QGroupBox("Scan Type")
        scan_type_layout = QVBoxLayout()
        
        self.scan_type_group = QButtonGroup()
        
        scan_types = [
            ('quick', 'Quick Scan (Top 100 ports)'),
            ('standard', 'Standard Scan (Ports 1-10000)'),
            ('full', 'Full Scan (All ports)'),
            ('custom', 'Custom (Specify ports)')
        ]
        
        for i, (value, label) in enumerate(scan_types):
            radio = QRadioButton(label)
            if value == self.scan_type:
                radio.setChecked(True)
            radio.toggled.connect(self.on_scan_type_changed)
            self.scan_type_group.addButton(radio, i)
            self.scan_type_group.setId(radio, value)
            scan_type_layout.addWidget(radio)
        
        scan_type_group.setLayout(scan_type_layout)
        layout.addWidget(scan_type_group)
        
        # Custom ports
        ports_label = QLabel("Custom Ports:")
        layout.addWidget(ports_label)
        
        self.ports_input = QLineEdit()
        self.ports_input.setPlaceholderText("e.g., 80,443,1000-2000")
        self.ports_input.setEnabled(False)
        layout.addWidget(self.ports_input)
        
        # Scan options
        options_group = QGroupBox("Scan Options")
        options_layout = QVBoxLayout()
        
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("Timeout (seconds):"))
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setMinimum(10)
        self.timeout_spin.setMaximum(300)
        self.timeout_spin.setValue(self.settings.get('scanner.timeout', 30))
        timeout_layout.addWidget(self.timeout_spin)
        timeout_layout.addStretch()
        options_layout.addLayout(timeout_layout)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start Scan")
        self.start_button.clicked.connect(self.accept)
        button_layout.addWidget(self.start_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def on_scan_type_changed(self):
        """Handle scan type change"""
        sender = self.sender()
        if sender.isChecked():
            scan_type = sender.text()
            if 'Custom' in scan_type:
                self.ports_input.setEnabled(True)
            else:
                self.ports_input.setEnabled(False)
    
    def get_scan_parameters(self):
        """Get configured scan parameters"""
        target = self.target_input.text().strip()
        
        # Validate target
        if not target:
            raise ValueError("Target is required")
        
        # Determine ports
        checked_button = None
        for button in self.scan_type_group.buttons():
            if button.isChecked():
                checked_button = button.text()
                break
        
        if 'Quick' in checked_button:
            ports = self.SCAN_PRESETS['quick']['ports']
        elif 'Standard' in checked_button:
            ports = self.SCAN_PRESETS['standard']['ports']
        elif 'Full' in checked_button:
            ports = self.SCAN_PRESETS['full']['ports']
        else:  # Custom
            ports = self.ports_input.text().strip()
            if not ports:
                raise ValueError("Ports required for custom scan")
        
        # Nmap arguments
        arguments = "-sS -sV -O"
        
        return target, ports, arguments
