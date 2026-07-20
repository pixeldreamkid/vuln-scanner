"""Report generation"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict


class ReportGenerator:
    """Generate scan reports in various formats"""
    
    def __init__(self, output_dir='reports'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_html_report(self, results: Dict) -> str:
        """Generate HTML report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"scan_report_{timestamp}.html"
        filepath = self.output_dir / filename
        
        html_content = self._build_html(results)
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def _build_html(self, results: Dict) -> str:
        """Build HTML report content"""
        timestamp = results.get('timestamp', datetime.now().isoformat())
        summary = results.get('summary', {})
        hosts = results.get('hosts', {})
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Network Vulnerability Scan Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #0d47a1;
            border-bottom: 2px solid #0d47a1;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #0d47a1;
            margin-top: 30px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 20px 0;
        }}
        .summary-box {{
            background-color: #f9f9f9;
            padding: 15px;
            border-left: 4px solid #0d47a1;
            border-radius: 4px;
        }}
        .summary-box h3 {{
            margin-top: 0;
            color: #0d47a1;
        }}
        .summary-box .value {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th {{
            background-color: #0d47a1;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .severity-critical {{
            background-color: #ffebee;
            color: #c62828;
            font-weight: bold;
        }}
        .severity-high {{
            background-color: #fff3e0;
            color: #e65100;
            font-weight: bold;
        }}
        .severity-medium {{
            background-color: #fffde7;
            color: #f57f17;
            font-weight: bold;
        }}
        .severity-low {{
            background-color: #e8f5e9;
            color: #2e7d32;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Network Vulnerability Scan Report</h1>
        
        <div class="summary">
            <div class="summary-box">
                <h3>Active Hosts</h3>
                <div class="value">{summary.get('active_hosts', 0)}</div>
            </div>
            <div class="summary-box">
                <h3>Open Ports</h3>
                <div class="value">{summary.get('total_ports', 0)}</div>
            </div>
            <div class="summary-box">
                <h3>Scan Time</h3>
                <div class="value">{timestamp}</div>
            </div>
        </div>
        
        <h2>Hosts Discovered</h2>
        <table>
            <thead>
                <tr>
                    <th>IP Address</th>
                    <th>Hostname</th>
                    <th>Status</th>
                    <th>Open Ports</th>
                    <th>Operating System</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for host_ip, host_data in hosts.items():
            ports = ', '.join(str(p['port']) for p in host_data.get('ports', []))
            os_name = host_data.get('os', {}).get('name', 'Unknown')
            hostname = host_data.get('hostname', 'Unknown')
            status = host_data.get('status', 'Unknown')
            
            html += f"""
                <tr>
                    <td>{host_ip}</td>
                    <td>{hostname}</td>
                    <td>{status}</td>
                    <td>{ports or 'None'}</td>
                    <td>{os_name}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
        
        <div class="footer">
            <p>Report generated by Network Vulnerability Scanner v1.0.0</p>
            <p>This report contains sensitive security information. Handle with care.</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def generate_json_report(self, results: Dict) -> str:
        """Generate JSON report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"scan_report_{timestamp}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        return str(filepath)
