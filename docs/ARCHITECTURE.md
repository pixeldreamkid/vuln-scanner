# Network Vulnerability Scanner - Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (PyQt6)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Main Window  │  │ Scan Dialog  │  │ Results Viewer  │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    Application Logic                        │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │   Scanner    │  │ CVE Checker  │  │    Reporter     │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌───────────────────────���──▼──────────────────────────────────┐
│                     Backend Services                        │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │   Network    │  │ Vulnerability│  │   Data Export   │   │
│  │   Module     │  │   Database   │  │    Services     │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  External Libraries                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │  Nmap (C++)  │  │   Python-    │  │  Requests/SSL   │   │
│  │              │  │   Nmap       │  │                 │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Module Breakdown

### 1. UI Module (`src/ui/`)

**Responsibility**: User interface and presentation

#### Components:

- **main_window.py**: Main application window
  - Menu bar with File, Scan, Tools, Help menus
  - Toolbar with Start/Stop/Export buttons
  - Progress bar for scan feedback
  - Tab widget for results display
  - Threading for non-blocking scans

- **scan_dialog.py**: Scan configuration dialog
  - Target input validation
  - Scan type selection (Quick, Standard, Full, Custom)
  - Port range specification
  - Timeout configuration
  - Pre-configured scan presets

- **results_viewer.py**: Results display widget
  - Hosts table with sorting/filtering
  - Host details panel
  - Service enumeration display
  - Vulnerability summary
  - CVSS severity highlighting

- **styles.py**: UI theming
  - Dark theme (default)
  - Light theme
  - Color schemes for severity levels
  - Responsive layout styling

### 2. Network Module (`src/network/`)

**Responsibility**: Network scanning and host discovery

#### Components:

- **scanner.py**: Main network scanner
  - Nmap integration
  - Multi-threaded scanning
  - Progress tracking
  - Result parsing and normalization
  - Port state detection
  - Service banner grabbing
  - OS fingerprinting
  - MAC address resolution

**Key Methods**:
```python
scan_network(target, ports, arguments)
_parse_results()
_extract_ports(host)
_extract_services(host)
_get_os_info(host)
```

### 3. Vulnerabilities Module (`src/vulnerabilities/`)

**Responsibility**: Vulnerability detection and CVE matching

#### Components:

- **vulnerability_db.py**: CVE database management
  - SQLite database or JSON cache
  - Known vulnerability patterns
  - Default credentials database
  - CVE query and search
  - CVSS scoring
  - Severity classification

- **cve_checker.py**: CVE matching engine
  - Service-to-CVE matching
  - Version pattern matching
  - Known exploit detection
  - Risk scoring calculation
  - Remediation recommendations
  - Multiple service analysis

**Key Methods**:
```python
analyze_service(service_name, version)
check_multiple_services(services)
_check_known_exploits(service_name, version)
_generate_recommendation(findings)
```

### 4. Reporting Module (`src/reporting/`)

**Responsibility**: Report generation and export

#### Components:

- **report_generator.py**: Multi-format report generation
  - HTML report generation with styling
  - JSON export for programmatic access
  - CSV export for spreadsheet analysis
  - PDF support (future)
  - Summary statistics
  - Timestamp tracking
  - Vulnerability details per host

**Supported Formats**:
- HTML: Interactive web report
- JSON: Machine-readable data export
- CSV: Spreadsheet-compatible format

### 5. Configuration Module (`src/config/`)

**Responsibility**: Application settings and configuration

#### Components:

- **settings.py**: Settings manager
  - Default configuration
  - File-based persistence
  - Nested key access (dot notation)
  - Type-safe getters/setters
  - User overrides

**Configuration Areas**:
- Scanner: Timeouts, threads, detection flags
- UI: Theme, window size, fonts
- Export: Formats, output directory
- Network: Default subnets, common ports

### 6. Utilities Module (`src/utils/`)

**Responsibility**: Common utility functions

#### Components:

- **validators.py**: Input validation
  - IP address validation
  - Subnet validation (CIDR)
  - Port range validation
  - Hostname validation
  - Target range parsing

- **helpers.py**: Utility functions
  - IP address conversion
  - Byte formatting
  - CVSS color mapping
  - Severity classification
  - Port-to-service mapping
  - MAC vendor lookup

- **logger.py**: Logging configuration
  - File and console logging
  - Structured formatting
  - Debug and error levels

## Data Flow

### Scan Workflow

```
1. User Input
   ↓
2. Validate Target & Options
   ↓
3. Create ScanThread
   ↓
4. Run Nmap Scan
   ↓
5. Parse Results
   ↓
6. Analyze for Vulnerabilities
   ↓
7. Display Results
   ↓
8. Generate Reports (on export)
```

### Vulnerability Detection Workflow

```
1. Detected Service + Version
   ↓
2. Query Vulnerability Database
   ↓
3. Match Against CVE Patterns
   ↓
4. Calculate Risk Score
   ↓
5. Generate Recommendations
   ↓
6. Display in UI
```

## Threading Model

### Main Thread
- UI event handling
- User interactions
- Display updates

### Scan Thread (QThread)
- Network scanning (blocking operation)
- Nmap execution
- Result parsing
- Progress callbacks to main thread

**Thread Safety**:
- Signals/slots for thread communication
- No direct thread variable access
- Progress callbacks via Qt signals

## Database Design

### Vulnerability Database (JSON)

```json
{
  "CVE-2014-0160": {
    "name": "Heartbleed",
    "description": "...",
    "cvss": 7.5,
    "affected": ["OpenSSL 1.0.1"],
    "remediation": "..."
  }
}
```

### Default Credentials Database

```python
{
  "ftp": [("anonymous", "anonymous"), ...],
  "ssh": [("root", "root"), ...],
  "mysql": [("root", ""), ...]
}
```

## Performance Considerations

### Optimization Strategies

1. **Nmap Arguments**: Use `-sS` (SYN scan) for speed
2. **Threading**: Process multiple ports simultaneously
3. **Timeouts**: Balance between speed and accuracy
4. **Port Selection**: Quick scan uses top 100 ports
5. **Result Caching**: Store parsed results in memory

### Scalability

- **Small Networks** (10-50 hosts): 5-30 minutes
- **Medium Networks** (50-200 hosts): 30 minutes - 2 hours
- **Large Networks** (200+ hosts): 2-8+ hours

## Security Considerations

### Input Validation
- All user input validated before use
- IP/subnet format checking
- Port range bounds checking
- Filename sanitization

### Data Protection
- Reports stored locally
- No data transmission to external servers
- Sensitive info in reports clearly marked
- Logs contain only non-sensitive info

### Nmap Execution
- No command injection possible
- Safe argument handling
- No shell execution
- Process isolation

## Extension Points

### Adding New Scan Types

1. Add to `SCAN_PRESETS` in `scan_dialog.py`
2. Update scan arguments if needed
3. Update documentation

### Adding New Vulnerability Checks

1. Add pattern to `vulnerability_db.py`
2. Implement check in `cve_checker.py`
3. Add to severity classification
4. Update documentation

### Adding Export Formats

1. Add method to `report_generator.py`
2. Implement format-specific logic
3. Add to export dialog
4. Update documentation

## Error Handling

### Scan Errors
- Network unreachable → Display error message
- Invalid target → Validation catches before scan
- Scan timeout → User can increase timeout
- Nmap not found → Display clear error

### Database Errors
- Missing CVE database → Create default
- Corrupted database → Clear and reinitialize
- Update failures → Use cached data

### UI Errors
- Dialog cancellation → Graceful exit
- Report generation failure → Display error
- Theme loading failure → Use default theme

## Testing Strategy

### Unit Tests
- Input validation functions
- Helper utility functions
- CVE matching logic

### Integration Tests
- Scanner + result parsing
- Vulnerability + recommendation generation
- Report generation

### UI Tests
- Dialog input handling
- Results display
- Theme application

## Future Enhancements

1. **Agent-based scanning**: Multiple scanner agents
2. **Scheduled scans**: Automated periodic scanning
3. **Trend tracking**: Historical vulnerability trends
4. **Remediation tracking**: Track patch progress
5. **Multi-protocol support**: SSH, HTTP, custom probes
6. **Advanced filtering**: Complex result queries
7. **Integration APIs**: Webhook support, API access
8. **Machine learning**: Anomaly detection

---

**Version**: 1.0.0  
**Last Updated**: 2026-07-20
