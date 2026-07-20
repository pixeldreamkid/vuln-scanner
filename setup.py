"""Setup script for packaging"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vuln-scanner',
    version='1.0.0',
    author='pixeldreamkid',
    description='Network Vulnerability Scanner - Windows Desktop Application',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pixeldreamkid/vuln-scanner',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Topic :: System :: Networking',
        'Topic :: Security',
    ],
    python_requires='>=3.10',
    install_requires=[
        'python-nmap>=0.0.1',
        'nmap>=3.0.0',
        'PyQt6>=6.6.1',
        'requests>=2.31.0',
        'paramiko>=3.3.1',
        'cryptography>=41.0.7',
        'beautifulsoup4>=4.12.2',
        'scapy>=2.5.0',
        'pyyaml>=6.0.1',
    ],
    entry_points={
        'console_scripts': [
            'vuln-scanner=src.main:main',
        ],
    },
)
