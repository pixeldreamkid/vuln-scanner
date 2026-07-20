# Contributing to Network Vulnerability Scanner

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Respect privacy and security
- Follow responsible disclosure for security issues

## Getting Started

### 1. Fork the Repository

```bash
git clone https://github.com/YOUR_USERNAME/vuln-scanner.git
cd vuln-scanner
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-fix-name
```

### 3. Set Up Development Environment

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install pytest black flake8
```

## Development Workflow

### Code Style

- Follow PEP 8 guidelines
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings to all functions

### Formatting Code

```bash
# Format code with black
black src/

# Check style with flake8
flake8 src/
```

### Testing

```bash
# Run tests
pytest tests/

# Run specific test
pytest tests/test_scanner.py

# Run with coverage
pytest --cov=src tests/
```

## Areas for Contribution

### 🐛 Bug Fixes
- Check existing issues first
- Create test case that reproduces bug
- Fix the issue
- Ensure tests pass

### ✨ New Features
- Open discussion issue first
- Design the feature
- Implement with tests
- Document changes

### 📚 Documentation
- Fix typos and clarity
- Add examples
- Update API documentation
- Improve user guides

### 🔍 Vulnerability Patterns
- Add new CVE patterns to database
- Include CVSS scores
- Provide remediation guidance
- Add test cases

### 🚀 Performance
- Profile code to identify bottlenecks
- Optimize scanning algorithms
- Improve UI responsiveness
- Document improvements

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation
- **style**: Code style (formatting, missing semicolons, etc.)
- **refactor**: Code refactoring
- **perf**: Performance improvement
- **test**: Test addition or modification
- **chore**: Build, dependencies, etc.

### Examples

```
feat(scanner): add UDP scanning support

Implement UDP port scanning capability using Scapy.
Adds new scan option for UDP ports.

Fixes #123
```

```
fix(ui): prevent crash when target is empty

Add input validation in scan dialog to check
for empty target field before starting scan.

Closes #456
```

## Pull Request Process

### 1. Create Pull Request

```bash
git push origin feature/your-feature-name
```

### 2. PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123

## Testing
Describe testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for clarity
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
- [ ] No breaking changes
```

### 3. Code Review

- Maintainers will review your PR
- Respond to feedback constructively
- Make requested changes
- Re-request review when ready

### 4. Merge

Once approved, your PR will be merged!

## Adding Vulnerability Patterns

### 1. Identify Vulnerability

Document:
- CVE ID
- Affected software/versions
- CVSS score
- Description
- Remediation

### 2. Add to Database

Update `src/vulnerabilities/vulnerability_db.py`:

```python
self.vulnerabilities['CVE-XXXX-XXXXX'] = {
    'name': 'Vulnerability Name',
    'description': 'Detailed description',
    'affected': ['software 1.0', 'software 2.0'],
    'cvss': 7.5,
    'remediation': 'How to fix it'
}
```

### 3. Add Detection Logic

Update `src/vulnerabilities/cve_checker.py`:

```python
self.known_exploits['SoftwareName'] = {
    '1.0-1.5': ['CVE-XXXX-XXXXX'],
    '2.0': ['CVE-YYYY-YYYYY'],
}
```

### 4. Test Addition

Create test in `tests/test_vulnerabilities.py`:

```python
def test_detect_cve_xxxx_xxxxx():
    checker = CVEChecker()
    analysis = checker.analyze_service('Software', '1.0')
    assert 'CVE-XXXX-XXXXX' in [v['id'] for v in analysis['vulnerabilities']]
```

## Reporting Security Issues

⚠️ **Do not open public issues for security vulnerabilities!**

Instead:

1. Email: security@example.com
2. Include details of vulnerability
3. Allow time for fix before disclosure
4. Follow responsible disclosure practices

## Questions?

- Check documentation in `docs/`
- Review existing issues and discussions
- Open a discussion issue
- Email maintainers

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributors page

---

Thank you for making Network Vulnerability Scanner better! 🎉
