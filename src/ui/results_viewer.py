"""Results viewer widget"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QSplitter, QTextEdit, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush
from utils.helpers import get_severity_label, calculate_cvss_color, port_to_service


class ResultsViewer(QWidget):
    """Display scan results"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.current_results = None
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Summary
        summary_layout = QHBoxLayout()
        self.summary_label = QLabel("No scan results yet")
        summary_layout.addWidget(self.summary_label)
        summary_layout.addStretch()
        layout.addLayout(summary_layout)
        
        # Splitter for hosts and details
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Hosts table
        self.hosts_table = QTableWidget()
        self.hosts_table.setColumnCount(5)
        self.hosts_table.setHorizontalHeaderLabels(
            ['IP Address', 'Hostname', 'Status', 'Open Ports', 'OS']
        )
        self.hosts_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.hosts_table.itemSelectionChanged.connect(self.on_host_selected)
        splitter.addWidget(self.hosts_table)
        
        # Details panel
        details_layout = QVBoxLayout()
        details_label = QLabel("Host Details")
        details_layout.addWidget(details_label)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        details_layout.addWidget(self.details_text)
        
        details_widget = QWidget()
        details_widget.setLayout(details_layout)
        splitter.addWidget(details_widget)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
        self.setLayout(layout)
    
    def display_results(self, results):
        """Display scan results"""
        self.current_results = results
        
        if not results['success']:
            self.summary_label.setText(f"Scan failed: {results.get('error', 'Unknown error')}")
            return
        
        # Update summary
        summary = results['summary']
        self.summary_label.setText(
            f"Found {summary['active_hosts']} active hosts, "
            f"{summary['total_ports']} open ports"
        )
        
        # Populate hosts table
        hosts = results['hosts']
        self.hosts_table.setRowCount(len(hosts))
        
        for row, (host_ip, host_data) in enumerate(hosts.items()):
            # IP Address
            ip_item = QTableWidgetItem(host_ip)
            self.hosts_table.setItem(row, 0, ip_item)
            
            # Hostname
            hostname_item = QTableWidgetItem(host_data.get('hostname', 'Unknown'))
            self.hosts_table.setItem(row, 1, hostname_item)
            
            # Status
            status_item = QTableWidgetItem(host_data.get('status', 'Unknown'))
            self.hosts_table.setItem(row, 2, status_item)
            
            # Open Ports
            ports = host_data.get('ports', [])
            open_ports_str = ', '.join(str(p['port']) for p in ports)
            ports_item = QTableWidgetItem(open_ports_str or 'None')
            self.hosts_table.setItem(row, 3, ports_item)
            
            # OS
            os_name = host_data.get('os', {}).get('name', 'Unknown')
            os_item = QTableWidgetItem(os_name)
            self.hosts_table.setItem(row, 4, os_item)
    
    def on_host_selected(self):
        """Handle host selection"""
        selected_rows = self.hosts_table.selectedIndexes()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        ip_item = self.hosts_table.item(row, 0)
        host_ip = ip_item.text()
        
        if host_ip in self.current_results['hosts']:
            host_data = self.current_results['hosts'][host_ip]
            self.display_host_details(host_data)
    
    def display_host_details(self, host_data):
        """Display details for selected host"""
        details = f"""IP Address: {host_data.get('ip', 'N/A')}
Hostname: {host_data.get('hostname', 'Unknown')}
MAC Address: {host_data.get('mac', 'Unknown')}
Status: {host_data.get('status', 'Unknown')}

Operating System:
  Name: {host_data.get('os', {}).get('name', 'Unknown')}
  Accuracy: {host_data.get('os', {}).get('accuracy', 0)}%

Open Ports and Services:
"""
        
        for service in host_data.get('services', []):
            details += f"\n  {service['port']}/{service['protocol']}: {service['name']}"
            if service['product']:
                details += f" ({service['product']} {service['version']})".strip()
        
        # Add vulnerabilities if detected
        vulns = host_data.get('vulnerabilities', {})
        if vulns:
            details += "\n\nDetected Vulnerabilities:\n"
            for port_proto, vuln_analysis in vulns.items():
                if vuln_analysis['vulnerabilities']:
                    details += f"\n  Port {port_proto}:\n"
                    for vuln in vuln_analysis['vulnerabilities']:
                        cvss = vuln.get('cvss', 0)
                        severity = get_severity_label(cvss)
                        details += f"    - {vuln.get('name', 'Unknown')}: {severity} (CVSS: {cvss})\n"
                        details += f"      Recommendation: {vuln_analysis.get('recommendation', 'N/A')}\n"
        
        self.details_text.setText(details)
