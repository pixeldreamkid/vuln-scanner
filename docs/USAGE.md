# Network Vulnerability Scanner - Usage Guide

## Installation

### Option 1: Download Executable (Recommended)

1. Download `VulnerabilityScanner.exe` from the [Releases page](https://github.com/pixeldreamkid/vuln-scanner/releases)
2. Double-click to run (no installation needed)

### Option 2: Install from Source

```bash
# Clone repository
git clone https://github.com/pixeldreamkid/vuln-scanner.git
cd vuln-scanner

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run application
python src/main.py
```

### Option 3: Build Your Own Executable

```bash
# Windows
build_windows.bat

# Linux/macOS
bash build_linux.sh
```

## Getting Started

### 1. Launch the Application

Run `VulnerabilityScanner.exe` (or `python src/main.py` if running from source)

### 2. Configure Your Scan

**Target Input:**
- Single IP: `192.168.1.1`
- Subnet (CIDR): `192.168.1.0/24`
- IP Range: `192.168.1.1-255`

**Scan Types:**
- **Quick Scan**: ~2-5 minutes, scans top 100 common ports
- **Standard Scan**: ~15-30 minutes, scans ports 1-10000
- **Full Scan**: ~1-4 hours, scans all 65535 ports
- **Custom**: Specify exact ports (e.g., `80,443,1000-2000`)

### 3. Run the Scan

1. Click **"Start Scan"** button
2. Monitor progress bar
3. Review results as they appear

### 4. Analyze Results

**Hosts Tab:**
- Lists all discovered hosts
- Shows IP, hostname, status
- Displays open ports and OS

**Click on a host to view:**
- Detailed service information
- Detected vulnerabilities
- CVSS severity scores
- Remediation recommendations

### 5. Export Report

Click **"Export Report"** to save findings:
- **HTML**: Interactive web report
- **JSON**: Machine-readable data
- **CSV**: Spreadsheet format

## Scan Types Explained

### Quick Scan (Recommended for Initial Reconnaissance)

```
Ports: 21,22,23,25,53,80,110,143,443,445,3306,3389,5432,5900,8080,8443
Duration: 2-5 minutes
Use Case: Identify main services, quick assessment
```

**When to use:**
- First-time network scanning
- Quick security assessment
- Identifying critical services

### Standard Scan (Recommended for Regular Audits)

```
Ports: 1-10000
Duration: 15-30 minutes
Use Case: Comprehensive port scan, find less common services
```

**When to use:**
- Regular security audits
- Compliance checks
- Identify all potentially exposed services

### Full Scan (For Thorough Assessments)

```
Ports: 1-65535
Duration: 1-4 hours
Use Case: Complete port enumeration, find all open ports
```

**When to use:**
- Deep security assessment
- Looking for unusual/hidden services
- Post-incident analysis

### Custom Scan (For Targeted Scans)

```
Example: 80,443,3306,5432
Duration: Varies (typically <10 minutes)
Use Case: Test specific services
```

**When to use:**
- Verify specific service patches
- Target known vulnerable ports
- Quick service verification

## Understanding Results

### Severity Levels

| Level | CVSS Score | Description |
|-------|-----------|-------------|
| **Critical** | 9.0-10.0 | Immediate action required |
| **High** | 7.0-8.9 | Apply patches soon |
| **Medium** | 4.0-6.9 | Plan updates |
| **Low** | 0.1-3.9 | Monitor for updates |
| **None** | 0.0 | No known vulnerabilities |

### Color Coding in Reports

- 🔴 **Red**: Critical vulnerability
- 🟠 **Orange**: High/Medium vulnerability
- 🟡 **Yellow**: Medium vulnerability
- 🟢 **Green**: Low/No vulnerability

## Common Vulnerabilities Detected

### 1. Weak SSH Versions
**Issue**: SSH 1.x protocols are vulnerable
**Fix**: Update to SSH 2.0 or later

### 2. Open SMB (Port 445)
**Issue**: File sharing protocol exposed
**Fix**: Restrict access via firewall

### 3. Unencrypted HTTP
**Issue**: Service running without HTTPS
**Fix**: Enable SSL/TLS encryption

### 4. Default Credentials
**Issue**: Using default username/password
**Fix**: Change to strong, unique credentials

### 5. Weak SSL/TLS Ciphers
**Issue**: Outdated or weak encryption
**Fix**: Update TLS configuration

## Tips & Best Practices

### Before Scanning
- ✓ Notify network administrators
- ✓ Have proper authorization
- ✓ Run during off-hours if possible
- ✓ Start with Quick Scan first

### During Scanning
- ✓ Monitor network performance
- ✓ Don't interrupt the scan
- ✓ Keep detailed records
- ✓ Document any issues

### After Scanning
- ✓ Review all findings
- ✓ Prioritize high/critical items
- ✓ Create remediation plan
- ✓ Track fixes over time
- ✓ Export and archive reports

## Troubleshooting

### No Hosts Found

**Problem**: Scan completes but no hosts discovered

**Solutions**:
1. Verify target network is correct
2. Check network connectivity
3. Ensure firewall allows ICMP
4. Try scanning single IP address
5. Run as Administrator

### Scanner Crashes

**Problem**: Application crashes during scan

**Solutions**:
1. Update to latest version
2. Reduce number of ports
3. Increase timeout value
4. Run on Windows 10/11
5. Check available RAM

### Very Slow Scanning

**Problem**: Scan taking longer than expected

**Solutions**:
1. Reduce scan scope
2. Use Quick Scan instead
3. Scan fewer hosts at a time
4. Check network latency
5. Close other bandwidth-heavy apps

### CVE Database Issues

**Problem**: Can't load vulnerability database

**Solutions**:
1. Check internet connection
2. Verify proxy settings
3. Clear cache and restart
4. Update application
5. Check database file permissions

## Advanced Configuration

### Settings File

Edit `config/settings.json` to customize:

```json
{
  "scanner": {
    "timeout": 30,
    "threads": 10,
    "enable_os_detection": true
  },
  "ui": {
    "theme": "dark",
    "window_width": 1400,
    "window_height": 900
  }
}
```

### Nmap Arguments

For custom scans, you can use Nmap arguments:

```
-sS    SYN scan (stealth)
-sV    Service version detection
-O     OS fingerprinting
-A     Aggressive scan (all options)
-Pn    Skip ping (useful if ICMP blocked)
```

## Security Notes

⚠️ **IMPORTANT**

1. **Only scan networks you own or have permission to scan**
2. **Unauthorized network scanning may be illegal**
3. **Use this tool responsibly**
4. **Keep scan reports secure and confidential**
5. **Follow your organization's policies**

## System Requirements

- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 500MB free space
- **Network**: Direct network access to targets
- **Admin**: May need Administrator privileges

## Performance Tuning

### For Faster Scans

1. Reduce ports: Use Quick Scan or Custom
2. Increase threads: Set `threads: 20` in settings
3. Disable OS detection: Set `enable_os_detection: false`
4. Use specific IP ranges: Narrow scope as much as possible

### For More Thorough Scans

1. Use Full Scan for complete coverage
2. Enable all detection options
3. Allow more time: Increase timeout value
4. Run multiple times: Verify findings

## Support & Feedback

- **Issues**: Report on GitHub
- **Questions**: Check documentation
- **Feature Requests**: Submit via GitHub
- **Security**: Report privately if critical

## Version History

### v1.0.0 (Initial Release)
- Network discovery and port scanning
- CVE matching and vulnerability detection
- HTML/JSON/CSV report generation
- Dark/Light theme support
- Multiple scan types

---

**Happy Scanning! Stay Secure!** 🔒
