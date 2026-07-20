"""CVE matching and analysis engine"""

import logging
from typing import Dict, List
from vulnerabilities.vulnerability_db import VulnerabilityDatabase

logger = logging.getLogger(__name__)


class CVEChecker:
    """Check and match services against known CVEs"""
    
    def __init__(self, vuln_db: VulnerabilityDatabase = None):
        self.vuln_db = vuln_db or VulnerabilityDatabase()
        self.known_exploits = self._load_exploit_patterns()
    
    def _load_exploit_patterns(self) -> Dict:
        """Load known exploit patterns"""
        return {
            'Apache': {
                '1.x': ['CVE-2002-0392', 'CVE-2005-3352'],
                '2.0-2.4.1': ['CVE-2010-0408'],
            },
            'OpenSSL': {
                '0.9.8': ['CVE-2014-0160'],  # Heartbleed
                '1.0.1': ['CVE-2014-0160'],
            },
            'PHP': {
                '5.0-5.3': ['CVE-2011-4885'],
            },
            'Tomcat': {
                '5.x': ['CVE-2009-3548'],
                '6.x': ['CVE-2009-3548'],
            }
        }
    
    def analyze_service(self, service_name: str, version: str = None) -> Dict:
        """
        Analyze service for vulnerabilities
        
        Returns:
            Dictionary with vulnerability findings
        """
        findings = {
            'service': service_name,
            'version': version,
            'vulnerabilities': [],
            'risk_score': 0,
            'recommendation': ''
        }
        
        # Check database for vulnerabilities
        db_vulns = self.vuln_db.check_service_vulnerability(service_name, version)
        findings['vulnerabilities'].extend(db_vulns)
        
        # Check for known exploits
        exploit_vulns = self._check_known_exploits(service_name, version)
        findings['vulnerabilities'].extend(exploit_vulns)
        
        # Calculate risk score
        if findings['vulnerabilities']:
            cvss_scores = [v.get('cvss', 5) for v in findings['vulnerabilities']]
            findings['risk_score'] = max(cvss_scores) if cvss_scores else 0
        
        # Generate recommendation
        findings['recommendation'] = self._generate_recommendation(findings)
        
        return findings
    
    def _check_known_exploits(self, service_name: str, version: str = None) -> List[Dict]:
        """Check against known exploit patterns"""
        exploits = []
        
        if service_name not in self.known_exploits:
            return exploits
        
        service_exploits = self.known_exploits[service_name]
        
        if version:
            for version_pattern, cves in service_exploits.items():
                if self._version_matches(version, version_pattern):
                    for cve in cves:
                        cve_data = self.vuln_db.query_cve(cve)
                        if cve_data:
                            exploits.append({
                                'id': cve,
                                **cve_data
                            })
        
        return exploits
    
    def _version_matches(self, version: str, pattern: str) -> bool:
        """Check if version matches pattern"""
        # Simple pattern matching
        if 'x' in pattern:
            # Pattern like "1.x" or "5.0-5.3"
            base = pattern.split('.')[0]
            return version.startswith(base)
        elif '-' in pattern:
            # Range like "5.0-5.3"
            parts = pattern.split('-')
            return parts[0] <= version <= parts[1]
        else:
            return version == pattern
    
    def _generate_recommendation(self, findings: Dict) -> str:
        """Generate remediation recommendation"""
        if not findings['vulnerabilities']:
            return "No known vulnerabilities detected. Monitor for updates."
        
        risk_level = self._get_risk_level(findings['risk_score'])
        
        if risk_level == 'Critical':
            return "URGENT: Apply security patches immediately. Consider disabling this service if patches are unavailable."
        elif risk_level == 'High':
            return "Apply available security updates as soon as possible. Restrict access if feasible."
        elif risk_level == 'Medium':
            return "Plan to apply available updates. Implement network segmentation if possible."
        else:
            return "Monitor for updates. No immediate action required."
    
    def _get_risk_level(self, cvss_score: float) -> str:
        """Get risk level from CVSS score"""
        if cvss_score >= 9.0:
            return 'Critical'
        elif cvss_score >= 7.0:
            return 'High'
        elif cvss_score >= 4.0:
            return 'Medium'
        else:
            return 'Low'
    
    def check_multiple_services(self, services: List[Dict]) -> List[Dict]:
        """Analyze multiple services"""
        results = []
        for service in services:
            analysis = self.analyze_service(
                service.get('name'),
                service.get('version')
            )
            results.append(analysis)
        return results
