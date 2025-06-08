# Contributing to Compounding Tracker Bot

Thank you for your interest in contributing to the Compounding Tracker Bot! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bug fix
4. Make your changes
5. Test your changes thoroughly
6. Submit a pull request

## Development Setup

1. **Clone the repository**:
```bash
git clone https://github.com/YOUR_USERNAME/Compounding_tracker.git
cd Compounding_tracker
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your bot token
```

## Code Style Guidelines

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused
- Use type hints where appropriate

## Testing

Before submitting a pull request:

1. Test all bot commands manually
2. Verify conversation flows work correctly
3. Test error handling scenarios
4. Ensure multi-language support works
5. Test with different user scenarios

## Pull Request Process

1. **Create a descriptive branch name**:
```bash
git checkout -b feature/add-new-calculation-method
git checkout -b fix/conversation-handler-bug
```

2. **Make your changes with clear commit messages**:
```bash
git commit -m "Add support for weekly compounding mode"
```

3. **Update documentation if needed**:
   - Update README.md for new features
   - Add comments for complex code
   - Update docstrings

4. **Push to your fork**:
```bash
git push origin feature/your-feature-name
```

5. **Create a pull request**:
   - Provide a clear title and description
   - Reference any related issues
   - Include screenshots for UI changes

## Reporting Issues

When reporting issues:

1. Use a clear, descriptive title
2. Provide steps to reproduce the issue
3. Include error messages and logs
4. Specify your environment (Python version, OS, etc.)
5. Include relevant code snippets

## Feature Requests

For new features:

1. Check if the feature already exists or is planned
2. Describe the use case and benefits
3. Provide examples of how it would work
4. Consider backward compatibility

## Code Review Process

All pull requests will be reviewed for:

- Code quality and style
- Functionality and correctness
- Security considerations
- Performance impact
- Documentation completeness

## Areas for Contribution

We welcome contributions in these areas:

- **New Features**: Additional calculation methods, new bot commands
- **Bug Fixes**: Error handling, conversation flow issues
- **Documentation**: README improvements, code comments
- **Testing**: Unit tests, integration tests
- **Localization**: Additional language support
- **Performance**: Optimization of calculations and data handling

## Questions?

If you have questions about contributing:

1. Check existing issues and discussions
2. Create a new issue with the "question" label
3. Reach out to maintainers

Thank you for contributing to make this bot better!