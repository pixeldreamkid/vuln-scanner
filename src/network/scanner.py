"""Network scanner - main scanning engine"""

import nmap
import threading
import logging
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket

logger = logging.getLogger(__name__)


class NetworkScanner:
    """Main network scanner using nmap"""
    
    def __init__(self, timeout=30):
        self.nm = nmap.PortScanner()
        self.timeout = timeout
        self.is_scanning = False
        self.scan_progress = 0
        self.progress_callback = None
        
    def set_progress_callback(self, callback):
        """Set callback for progress updates"""
        self.progress_callback = callback
    
    def update_progress(self, current, total, status=""):
        """Update scan progress"""
        self.scan_progress = (current / total * 100) if total > 0 else 0
        if self.progress_callback:
            self.progress_callback(self.scan_progress, status)
    
    def scan_network(self, target, ports="1-1000", arguments="-sS -sV", scan_type="Standard") -> Dict:
        """
        Scan network for active hosts and open ports
        
        Args:
            target: Target IP/subnet (e.g., '192.168.1.0/24' or '192.168.1.1-255')
            ports: Port specification (e.g., '80,443,1-1000')
            arguments: Nmap arguments
            scan_type: Type of scan (Quick, Standard, Full, Custom)
        
        Returns:
            Dictionary with scan results
        """
        try:
            self.is_scanning = True
            logger.info(f"Starting {scan_type} scan on {target}")
            self.update_progress(0, 100, "Initializing scan...")
            
            # Build scan command
            scan_args = f"-sS {arguments}"
            if ports:
                scan_args += f" -p {ports}"
            
            logger.debug(f"Scan arguments: {scan_args}")
            
            # Run scan
            self.nm.scan(
                hosts=target,
                arguments=scan_args,
                sudo=False,
                timeout=self.timeout
            )
            
            self.update_progress(50, 100, "Processing results...")
            results = self._parse_results()
            
            self.update_progress(100, 100, "Scan complete")
            logger.info(f"Scan completed. Found {len(results['hosts'])} hosts")
            
            return {
                'success': True,
                'hosts': results['hosts'],
                'summary': results['summary'],
                'timestamp': results['timestamp']
            }
            
        except Exception as e:
            logger.error(f"Scan error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'hosts': [],
                'summary': {}
            }
        finally:
            self.is_scanning = False
    
    def _parse_results(self) -> Dict:
        """Parse nmap scan results"""
        from datetime import datetime
        hosts_data = {}
        
        for host in self.nm.all_hosts():
            if self.nm[host].state() == 'up':
                host_data = {
                    'ip': host,
                    'status': self.nm[host].state(),
                    'hostname': self._get_hostname(host),
                    'mac': self._get_mac(host),
                    'os': self._get_os_info(host),
                    'ports': self._extract_ports(host),
                    'services': self._extract_services(host),
                }
                hosts_data[host] = host_data
        
        return {
            'hosts': hosts_data,
            'summary': {
                'total_hosts': len(self.nm.all_hosts()),
                'active_hosts': len(hosts_data),
                'total_ports': sum(len(h['ports']) for h in hosts_data.values()),
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_hostname(self, host: str) -> str:
        """Get hostname for IP"""
        try:
            return socket.gethostbyaddr(host)[0]
        except:
            return "Unknown"
    
    def _get_mac(self, host: str) -> str:
        """Get MAC address for host"""
        try:
            if 'MAC' in self.nm[host]['addresses']:
                return self.nm[host]['addresses']['MAC']
        except:
            pass
        return "Unknown"
    
    def _get_os_info(self, host: str) -> Dict:
        """Extract OS information"""
        os_info = {
            'name': 'Unknown',
            'accuracy': 0,
            'cpe': []
        }
        
        try:
            if 'osmatch' in self.nm[host]:
                matches = self.nm[host]['osmatch']
                if matches:
                    os_info['name'] = matches[0]['name']
                    os_info['accuracy'] = int(matches[0]['accuracy'])
                    if 'cpe' in matches[0]:
                        os_info['cpe'] = matches[0]['cpe']
        except:
            pass
        
        return os_info
    
    def _extract_ports(self, host: str) -> List[Dict]:
        """Extract open ports"""
        ports = []
        try:
            for proto in self.nm[host].all_protocols():
                for port in self.nm[host][proto].keys():
                    state = self.nm[host][proto][port]['state']
                    if state == 'open':
                        ports.append({
                            'port': port,
                            'protocol': proto,
                            'state': state
                        })
        except:
            pass
        return sorted(ports, key=lambda x: x['port'])
    
    def _extract_services(self, host: str) -> List[Dict]:
        """Extract service information"""
        services = []
        try:
            for proto in self.nm[host].all_protocols():
                for port in self.nm[host][proto].keys():
                    if self.nm[host][proto][port]['state'] == 'open':
                        service_info = {
                            'port': port,
                            'protocol': proto,
                            'name': self.nm[host][proto][port].get('name', 'Unknown'),
                            'product': self.nm[host][proto][port].get('product', ''),
                            'version': self.nm[host][proto][port].get('version', ''),
                            'extrainfo': self.nm[host][proto][port].get('extrainfo', ''),
                        }
                        services.append(service_info)
        except:
            pass
        return services
    
    def stop_scan(self):
        """Stop current scan"""
        self.is_scanning = False
        logger.info("Scan stopped by user")
