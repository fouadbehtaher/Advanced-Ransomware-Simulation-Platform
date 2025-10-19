# Contributing to ARSP

Thank you for your interest in contributing to the Advanced Ransomware Simulation Platform!

## Code of Conduct

### Ethical Guidelines

This project is designed for **legitimate security research and testing only**. By contributing, you agree to:

- Use the platform only for authorized security testing
- Never contribute malicious code or techniques intended for illegal use
- Follow responsible disclosure practices
- Respect privacy and security of others
- Comply with all applicable laws and regulations

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Any relevant logs or screenshots

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Potential implementation approach
   - Any security considerations

### Pull Requests

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed
   - Ensure all tests pass

4. **Commit your changes**
   ```bash
   git commit -m "Add feature: description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide clear description of changes
   - Reference any related issues
   - Ensure CI checks pass

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/Advanced-Ransomware-Simulation-Platform.git
cd Advanced-Ransomware-Simulation-Platform

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .
pip install -r requirements.txt

# Run tests
pytest

# Run linters
flake8 src/
pylint src/
black --check src/
mypy src/
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all public functions/classes
- Keep functions focused and modular
- Maximum line length: 100 characters

### Example

```python
def example_function(param: str, optional: Optional[int] = None) -> Dict[str, Any]:
    """
    Brief description of function.
    
    Args:
        param: Description of param
        optional: Description of optional parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When validation fails
    """
    # Implementation
    pass
```

## Testing Guidelines

- Write tests for all new functionality
- Maintain or improve code coverage
- Use descriptive test names
- Include both positive and negative test cases

```python
def test_feature_success_case():
    """Test successful execution of feature"""
    # Arrange
    # Act
    # Assert
    pass

def test_feature_error_handling():
    """Test error handling in feature"""
    # Test error cases
    pass
```

## Documentation

- Update README.md for significant changes
- Add docstrings to new code
- Update relevant .rst files in docs/
- Include usage examples where appropriate

## Security Considerations

When contributing, consider:

- **Input Validation**: Always validate and sanitize inputs
- **Isolation**: Maintain sandbox isolation integrity
- **Permissions**: Use least privilege principle
- **Logging**: Include appropriate security logging
- **Secrets**: Never commit secrets or credentials
- **Dependencies**: Keep dependencies updated and secure

## Review Process

1. All PRs require review before merging
2. CI checks must pass
3. Code must follow style guidelines
4. Tests must maintain coverage
5. Documentation must be updated

## Questions?

- Open an issue for questions
- Review existing documentation
- Check closed issues for similar questions

## Recognition

Contributors will be acknowledged in:
- CHANGELOG.md
- Project documentation
- Release notes

Thank you for helping make ARSP better and more secure!
