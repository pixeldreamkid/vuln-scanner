"""Configuration and settings management"""

import json
import os
from pathlib import Path


class AppSettings:
    """Application settings manager"""
    
    DEFAULT_SETTINGS = {
        'scanner': {
            'timeout': 30,
            'threads': 10,
            'max_ports': 65535,
            'enable_os_detection': True,
            'enable_version_detection': True,
        },
        'cve_database': {
            'auto_update': True,
            'update_interval': 7,  # days
            'cache_path': 'data/cve_cache.json',
        },
        'ui': {
            'theme': 'dark',
            'font_size': 10,
            'window_width': 1400,
            'window_height': 900,
        },
        'export': {
            'default_format': 'html',
            'include_remediation': True,
            'output_directory': 'reports',
        },
        'network': {
            'default_subnet': '192.168.1.0/24',
            'common_ports': '21,22,23,25,53,80,110,143,443,445,3306,3389,5432,5900,8080,8443',
        }
    }
    
    def __init__(self, config_path='config/settings.json'):
        self.config_path = Path(config_path)
        self.settings = self.DEFAULT_SETTINGS.copy()
        
    def load(self):
        """Load settings from file"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    self.settings.update(json.load(f))
            except Exception as e:
                print(f"Error loading settings: {e}, using defaults")
        else:
            self.save()
    
    def save(self):
        """Save settings to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def get(self, key, default=None):
        """Get setting value"""
        keys = key.split('.')
        value = self.settings
        for k in keys:
            value = value.get(k, {})
        return value if value else default
    
    def set(self, key, value):
        """Set setting value"""
        keys = key.split('.')
        settings = self.settings
        for k in keys[:-1]:
            settings = settings.setdefault(k, {})
        settings[keys[-1]] = value
        self.save()
