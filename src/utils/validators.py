"""Input validation utilities"""

import re
import ipaddress
from typing import Tuple, List


def validate_ip_address(ip: str) -> bool:
    """Validate single IP address"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_subnet(subnet: str) -> bool:
    """Validate CIDR notation subnet"""
    try:
        ipaddress.ip_network(subnet, strict=False)
        return True
    except ValueError:
        return False


def validate_port(port: int) -> bool:
    """Validate port number"""
    return isinstance(port, int) and 1 <= port <= 65535


def validate_port_range(port_range: str) -> Tuple[bool, str]:
    """Validate port range string (e.g., '80,443,1000-2000')"""
    try:
        ports = set()
        for part in port_range.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                if start > end or start < 1 or end > 65535:
                    return False, f"Invalid port range: {part}"
                ports.update(range(start, end + 1))
            else:
                port = int(part)
                if not validate_port(port):
                    return False, f"Invalid port: {port}"
                ports.add(port)
        
        return True, sorted(list(ports))
    except ValueError:
        return False, "Invalid port format"


def validate_hostname(hostname: str) -> bool:
    """Validate hostname"""
    pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$'
    return len(hostname) <= 255 and re.match(pattern, hostname) is not None


def parse_target_range(target: str) -> Tuple[bool, List[str]]:
    """
    Parse target range (subnet or IP range)
    Returns: (success, list_of_ips or error_message)
    """
    try:
        # Try CIDR notation
        if '/' in target:
            network = ipaddress.ip_network(target, strict=False)
            return True, [str(ip) for ip in network.hosts()]
        
        # Try IP range notation (e.g., 192.168.1.1-10)
        elif '-' in target:
            parts = target.rsplit('.', 1)
            if len(parts) == 2:
                base = parts[0]
                range_part = parts[1]
                
                if '-' in range_part:
                    start, end = map(int, range_part.split('-'))
                    ips = [f"{base}.{i}" for i in range(start, end + 1)]
                    return True, ips
        
        # Single IP
        elif validate_ip_address(target):
            return True, [target]
        
        return False, ["Invalid target format"]
    
    except Exception as e:
        return False, [str(e)]
