"""Helper utility functions"""

import socket
import struct
from typing import Dict, List
import subprocess
import platform


def ip_to_int(ip: str) -> int:
    """Convert IP address to integer"""
    return struct.unpack(">L", socket.inet_aton(ip))[0]


def int_to_ip(ip_int: int) -> str:
    """Convert integer to IP address"""
    return socket.inet_ntoa(struct.pack(">L", ip_int))


def get_local_ips() -> List[str]:
    """Get list of local IP addresses"""
    ips = []
    try:
        hostname = socket.gethostname()
        ips = socket.gethostbyname_ex(hostname)[2]
    except Exception:
        pass
    return ips


def get_default_gateway() -> str:
    """Get default gateway IP"""
    try:
        if platform.system() == 'Windows':
            result = subprocess.run(
                ['ipconfig'],
                capture_output=True,
                text=True
            )
            for line in result.stdout.split('\n'):
                if 'Default Gateway' in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        return parts[1].strip()
        else:
            result = subprocess.run(
                ['route', '-n'],
                capture_output=True,
                text=True
            )
            for line in result.stdout.split('\n'):
                if line.startswith('0.0.0.0'):
                    return line.split()[2]
    except Exception:
        pass
    return None


def format_bytes(bytes_val: int) -> str:
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} PB"


def calculate_cvss_color(cvss_score: float) -> str:
    """Return color based on CVSS score"""
    if cvss_score < 3.9:
        return "#00AA00"  # Green - Low
    elif cvss_score < 6.9:
        return "#FFAA00"  # Orange - Medium
    elif cvss_score < 8.9:
        return "#FF5500"  # Red-orange - High
    else:
        return "#FF0000"  # Red - Critical


def get_severity_label(cvss_score: float) -> str:
    """Get severity label from CVSS score"""
    if cvss_score == 0:
        return "None"
    elif cvss_score < 3.9:
        return "Low"
    elif cvss_score < 6.9:
        return "Medium"
    elif cvss_score < 8.9:
        return "High"
    else:
        return "Critical"


def port_to_service(port: int) -> str:
    """Get common service name for port"""
    common_ports = {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        445: 'SMB',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        5900: 'VNC',
        8080: 'HTTP-Alt',
        8443: 'HTTPS-Alt',
    }
    return common_ports.get(port, 'Unknown')


def mac_to_vendor(mac: str) -> str:
    """Lookup MAC vendor (simplified)"""
    # This would normally query a MAC vendor database
    # For now, return the MAC as-is
    return mac.upper()
