# Network Vulnerability Scanner - README

## ⚠️ Legal Disclaimer

**ONLY scan networks you own or have explicit written permission to scan.** Unauthorized network scanning may violate laws including the Computer Fraud and Abuse Act (CFAA). Always ensure you have proper authorization before scanning any network.

## Overview

Network Vulnerability Scanner is a comprehensive Windows-based application for network reconnaissance and security vulnerability detection. It provides automated network discovery, port scanning, service detection, and CVE matching to help identify security weaknesses in your network infrastructure.

## Key Features

### 🔍 Network Discovery
- ARP and ICMP scanning for host discovery
- MAC address and hostname resolution
- OS fingerprinting
- Network subnet scanning

### 🔓 Port Scanning
- Multi-threaded TCP/UDP port scanning
- Service version detection
- Banner grabbing
- Protocol identification
- State analysis (open/closed/filtered)

### 🚨 Vulnerability Detection
- CVE database matching (20,000+ entries)
- CVSS severity scoring
- Known exploit detection
- Default credential checking
- SSL/TLS weakness detection

### 📊 Reporting & Export
- Interactive HTML reports
- JSON data export
- CSV spreadsheet export
- Risk scoring and prioritization
- Remediation recommendations

### 🎨 Professional UI
- Modern PyQt6 interface
- Dark/Light theme support
- Real-time progress tracking
- Sortable results tables
- Detailed vulnerability information

## System Requirements

| Component | Requirement |
|-----------|-------------|
| OS | Windows 10/11 (64-bit) |
| RAM | 4GB minimum, 8GB recommended |
| Disk Space | 500MB free space |
| Python | 3.10+ (if running from source) |
| Network | Direct network access to targets |
| Privileges | Administrator (recommended) |

## Installation

### Option 1: Windows Executable (Recommended)

```bash
# Download VulnerabilityScanner.exe from releases
# Double-click to run
VulnerabilityScanner.exe
```

No installation or dependencies required!

### Option 2: Python Source

```bash
# Clone repository
git clone https://github.com/pixeldreamkid/vuln-scanner.git
cd vuln-scanner

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python src/main.py
```

### Option 3: Build Executable from Source

```bash
# Windows
build_windows.bat

# Linux/macOS (for reference)
bash build_linux.sh
```

## Quick Start

### Basic Scan

```
1. Launch: VulnerabilityScanner.exe
2. Enter Target: 192.168.1.0/24
3. Select: Quick Scan
4. Click: Start Scan
5. Review: Results in real-time
6. Export: HTML Report
```

### Target Input Formats

```
Single IP:        192.168.1.1
Subnet (CIDR):    192.168.1.0/24
IP Range:         192.168.1.1-255
Hostname:         example.com (if resolvable)
```

## Scan Types

### Quick Scan ⚡
```
Duration: 2-5 minutes
Ports: 21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 5900, 8080, 8443
Use: Initial reconnaissance, quick assessment
```

### Standard Scan ⏱️
```
Duration: 15-30 minutes
Ports: 1-10000
Use: Regular security audits, comprehensive assessment
```

### Full Scan 🔍
```
Duration: 1-4 hours
Ports: 1-65535 (all ports)
Use: Deep security assessment, complete enumeration
```

### Custom Scan 🎯
```
Duration: Variable (typically <10 minutes)
Ports: User-specified (e.g., 80,443,3306,5432)
Use: Targeted testing, specific service verification
```

## Understanding Results

### Severity Classification

| Level | CVSS | Color | Action |
|-------|------|-------|--------|
| **Critical** | 9.0-10.0 | 🔴 Red | Immediate action |
| **High** | 7.0-8.9 | 🟠 Orange | Apply patches soon |
| **Medium** | 4.0-6.9 | 🟡 Yellow | Plan updates |
| **Low** | 0.1-3.9 | 🟢 Green | Monitor |

### Report Elements

**Hosts Discovered**
- IP address and hostname
- Network status
- Open ports list
- Detected OS

**Services Identified**
- Port number and protocol
- Service name
- Product and version
- Additional info

**Vulnerabilities Found**
- CVE identifier
- Vulnerability name
- CVSS severity score
- Impact description
- Remediation steps

## Common Vulnerabilities

### 1. Weak SSH Versions
```
Issue: SSH 1.x protocol vulnerable to attacks
Fix: Upgrade to SSH 2.0+
Severity: High
```

### 2. Open SMB Port (445)
```
Issue: File sharing exposed to network
Fix: Restrict via firewall, disable if unused
Severity: High
```

### 3. HTTP Without HTTPS
```
Issue: Unencrypted data transmission
Fix: Enable SSL/TLS encryption
Severity: Medium
```

### 4. Default Credentials
```
Issue: Using manufacturer defaults
Fix: Change to strong, unique credentials
Severity: Critical
```

### 5. Weak TLS Configuration
```
Issue: Outdated or weak ciphers
Fix: Update TLS version, enable strong ciphers
Severity: Medium-High
```

## Best Practices

### Before Scanning
- ✅ Obtain written authorization
- ✅ Notify network administrators
- ✅ Schedule during maintenance window
- ✅ Start with Quick Scan
- ✅ Document scope and objectives

### During Scanning
- ✅ Monitor scan progress
- ✅ Note any network issues
- ✅ Avoid interrupting scan
- ✅ Keep system resources available

### After Scanning
- ✅ Review all findings carefully
- ✅ Prioritize by severity
- ✅ Create remediation plan
- ✅ Track fixes over time
- ✅ Archive reports securely

## Troubleshooting

### No Hosts Discovered

**Problem**: Scan completes without finding any hosts

**Solutions**:
1. Verify target network address is correct
2. Check network connectivity
3. Ensure ICMP (ping) is allowed
4. Try scanning a single known IP
5. Run as Administrator
6. Check firewall configuration

### Slow Scanning Speed

**Problem**: Scan takes much longer than expected

**Solutions**:
1. Reduce port range (use Quick Scan)
2. Increase timeout in settings
3. Reduce number of concurrent threads
4. Scan smaller subnet ranges
5. Check network latency
6. Close bandwidth-heavy applications

### Service Detection Issues

**Problem**: Service names/versions not detected

**Solutions**:
1. Run as Administrator
2. Ensure nmap installed correctly
3. Increase scan timeout
4. Use Standard or Full scan
5. Check if services are responding

### CVE Database Problems

**Problem**: Can't load vulnerability database

**Solutions**:
1. Check internet connection
2. Verify proxy settings if behind firewall
3. Clear cache and restart
4. Update application to latest version
5. Check file permissions
6. Manually update database

## Advanced Usage

### Custom Configuration

Edit `config/settings.json`:

```json
{
  "scanner": {
    "timeout": 30,
    "threads": 10,
    "enable_os_detection": true,
    "enable_version_detection": true
  },
  "ui": {
    "theme": "dark",
    "window_width": 1400,
    "window_height": 900,
    "font_size": 10
  }
}
```

### Command Line (Source Only)

```bash
python src/main.py
```

### Integration with Scripts

Import and use programmatically:

```python
from network.scanner import NetworkScanner
from vulnerabilities.cve_checker import CVEChecker

scanner = NetworkScanner()
results = scanner.scan_network("192.168.1.0/24", "1-1000")

checker = CVEChecker()
for host_ip, host_data in results['hosts'].items():
    for service in host_data['services']:
        analysis = checker.analyze_service(
            service['name'],
            service['version']
        )
        print(analysis)
```

## Report Formats

### HTML Report
- Interactive web format
- Sortable tables
- Color-coded severity
- Professional styling
- Print-friendly

### JSON Export
- Machine-readable format
- Complete data export
- Programmatic access
- Third-party integration

### CSV Export
- Spreadsheet format
- Excel compatible
- Easy analysis
- Data manipulation

## Performance Metrics

### Scan Duration by Network Size

```
Small (10 hosts):      5-15 minutes
Medium (50 hosts):     15-45 minutes
Large (200 hosts):     1-4 hours
XL (1000 hosts):       4-12 hours
```

### Scan Duration by Type

```
Quick:     2-5 min   (top 100 ports)
Standard:  15-30 min (ports 1-10000)
Full:      1-4 hours (all 65535 ports)
Custom:    Variable  (depends on ports)
```

## FAQ

**Q: Do I need Nmap installed separately?**
A: No, it's included in the executable. For source installation, install via `pip install python-nmap`.

**Q: Can I scan across the internet?**
A: Yes, but only if you have authorization. You can specify any routable IP address or range.

**Q: Does it support IPv6?**
A: Current version supports IPv4. IPv6 support coming in v2.0.

**Q: How often is the CVE database updated?**
A: Automatically weekly if auto-update is enabled. Manual updates available in Tools menu.

**Q: Can I schedule automatic scans?**
A: Future version. Currently, manual scanning only.

**Q: What's the maximum network size I can scan?**
A: Limited mainly by time and network bandwidth. 1000+ host scans feasible with Full scan.

**Q: Does it impact network performance?**
A: Scans use minimal bandwidth. SYN scan doesn't complete connections. Adjust threads in settings if needed.

**Q: Is my data secure?**
A: All data stored locally. No external uploads. Reports are your responsibility to secure.

## Security Notes

⚠️ **Important**

- **Legal**: Unauthorized scanning may violate CFAA and other laws
- **Ethical**: Always obtain written permission
- **Safety**: Test in isolated environment first
- **Confidentiality**: Reports contain sensitive data
- **Compliance**: Follow organizational policies

## Support

- **Documentation**: See `docs/USAGE.md`
- **Architecture**: See `docs/ARCHITECTURE.md`
- **Issues**: Report on GitHub Issues
- **Feature Requests**: GitHub Discussions
- **Security Issues**: Report privately

## Contributing

Contributions welcome! Areas needed:

- Vulnerability pattern additions
- UI/UX improvements
- Performance optimization
- Bug fixes
- Documentation
- Testing

See CONTRIBUTING.md for guidelines.

## License

MIT License - See LICENSE file

## Changelog

### v1.0.0 (2026-07-20)

✅ **Features**
- Network discovery and host enumeration
- Multi-threaded port scanning
- Service detection and versioning
- CVE matching and risk scoring
- Multiple report formats (HTML/JSON/CSV)
- Dark/Light theme support
- Quick/Standard/Full/Custom scan types

✅ **UI**
- Modern PyQt6 interface
- Real-time progress tracking
- Interactive results display
- Detailed vulnerability information
- Menu-driven access

✅ **Reports**
- HTML reports with statistics
- JSON data export
- CSV spreadsheet export
- CVSS severity highlighting
- Remediation recommendations

## Roadmap

**v1.1.0 (Q3 2026)**
- Scheduled scanning
- IPv6 support
- Enhanced filtering
- History tracking

**v2.0.0 (Q4 2026)**
- Agent-based scanning
- Trend analysis
- API support
- Machine learning anomaly detection

## Credits

- **Nmap**: Network mapping and port scanning
- **PyQt6**: Cross-platform GUI toolkit
- **NVD**: National Vulnerability Database
- **CVSS**: Common Vulnerability Scoring System

---

**Version**: 1.0.0  
**Last Updated**: 2026-07-20  
**Author**: pixeldreamkid  
**License**: MIT

---

**Questions?** Check the documentation or open an issue on GitHub.

**Found a security issue?** Report it privately to maintain responsible disclosure.

**Happy Scanning! Stay Secure! 🔒**
