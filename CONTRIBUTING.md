# Contributing to Agent-on-Call

Thank you for your interest in contributing to Agent-on-Call! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

1. **Check existing issues** to see if the bug has already been reported
2. **Create a new issue** with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Screenshots (if applicable)
   - Environment details (OS, Docker version, etc.)

### Suggesting Features

1. **Check existing feature requests** to avoid duplicates
2. **Create a new issue** with:
   - Clear description of the feature
   - Use cases and benefits
   - Potential implementation approach
   - Any relevant examples

### Code Contributions

#### Getting Started

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/agent-on-call.git
   cd agent-on-call
   ```

2. **Set up development environment**
   ```powershell
   .\setup.ps1
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

#### Development Workflow

1. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

2. **Test your changes**
   ```powershell
   # Run backend tests
   .\commands.ps1 test
   
   # Manual testing
   .\commands.ps1 start
   # Test in browser
   ```

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   # or
   git commit -m "fix: resolve bug"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

## 📝 Coding Standards

### Python (Backend)

```python
# Use type hints
def create_ticket(title: str, description: str) -> dict:
    """
    Create a new ticket.
    
    Args:
        title: Ticket title
        description: Ticket description
        
    Returns:
        Created ticket dictionary
    """
    pass

# Follow PEP 8
# Use meaningful variable names
# Keep functions focused and small
```

### JavaScript/React (Frontend)

```javascript
// Use functional components
function TicketCard({ ticket }) {
  // Props destructuring
  // Hooks at the top
  const [loading, setLoading] = useState(false);
  
  // Event handlers
  const handleClick = () => {
    // Implementation
  };
  
  // Return JSX
  return (
    <Card>
      {/* Component markup */}
    </Card>
  );
}

// Export at the bottom
export default TicketCard;
```

### Commit Messages

Follow conventional commits format:

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(triage): add confidence threshold setting
fix(api): resolve CORS issue with frontend
docs(readme): update setup instructions
test(tickets): add integration tests
```

## 🧪 Testing Guidelines

### Backend Tests

```python
# tests/test_feature.py
import pytest
from fastapi.testclient import TestClient

def test_feature():
    """Test description."""
    # Arrange
    setup_data = {...}
    
    # Act
    result = function_to_test(setup_data)
    
    # Assert
    assert result == expected_value
```

**Run tests:**
```powershell
.\commands.ps1 test
```

### Manual Testing Checklist

- [ ] Create ticket works
- [ ] List tickets works
- [ ] View ticket details works
- [ ] Update ticket works
- [ ] Delete ticket works
- [ ] AI triage works
- [ ] Edit reply draft works
- [ ] Activity log displays correctly
- [ ] Error handling works
- [ ] Loading states work
- [ ] Data persists after refresh

## 📚 Documentation

### Code Documentation

**Python:**
```python
def perform_triage(title: str, description: str) -> dict:
    """
    Perform AI triage on a ticket.
    
    Analyzes ticket content using Gemini AI to determine:
    - Priority level (P0-P3)
    - Suggested assignee
    - Confidence score
    - Reply draft
    
    Args:
        title: Ticket title
        description: Ticket description
        
    Returns:
        Dictionary containing triage results
        
    Raises:
        ValueError: If title or description is empty
        APIError: If Gemini API call fails
    """
```

**JavaScript:**
```javascript
/**
 * Create a new ticket
 * @param {Object} ticketData - Ticket information
 * @param {string} ticketData.title - Ticket title
 * @param {string} ticketData.description - Ticket description
 * @param {string} ticketData.category - Ticket category
 * @returns {Promise<Object>} Created ticket
 */
async function createTicket(ticketData) {
  // Implementation
}
```

### README Updates

When adding features, update:
- Feature list in README.md
- API endpoints table (if applicable)
- Configuration section (if adding env vars)
- Dependencies (if adding new packages)

## 🔍 Code Review Process

### What Reviewers Look For

1. **Functionality**: Does it work as intended?
2. **Code Quality**: Is it clean, readable, maintainable?
3. **Tests**: Are there tests? Do they pass?
4. **Documentation**: Is it documented?
5. **Performance**: Any performance concerns?
6. **Security**: Any security issues?

### Addressing Feedback

- Be open to suggestions
- Ask questions if unclear
- Make requested changes
- Update the PR description if needed
- Re-request review after changes

## 🎯 Areas for Contribution

### Good First Issues

- Add more sample tickets
- Improve error messages
- Add loading animations
- Enhance UI styling
- Fix typos in documentation
- Add more test cases

### Feature Enhancements

- User authentication
- Email notifications
- File attachments
- Advanced search/filters
- Export to CSV/PDF
- Real-time updates (WebSocket)
- SLA tracking
- Analytics dashboard

### Technical Improvements

- Performance optimization
- Better error handling
- Logging improvements
- Caching layer
- Rate limiting
- Database indexing
- Code refactoring

## 📋 Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] PR description explains changes
- [ ] Screenshots included (if UI changes)

## 🐛 Debugging Tips

### Backend Issues

```powershell
# View logs
.\commands.ps1 logs-backend

# Access backend shell
docker-compose exec backend /bin/sh

# Run single test
docker-compose exec backend pytest tests/test_file.py::test_function -v
```

### Frontend Issues

```powershell
# View logs
.\commands.ps1 logs-frontend

# Check browser console (F12)
# Network tab for API calls
# Console tab for errors
```

## 🌟 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (if we create one)
- Mentioned in release notes
- Credited in commit history

## 📧 Communication

- **Issues**: For bug reports and feature requests
- **Pull Requests**: For code contributions
- **Discussions**: For questions and ideas

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## 🙏 Thank You!

Your contributions help make Agent-on-Call better for everyone. We appreciate your time and effort!

---

**Questions?** Feel free to ask in the issues section or PR comments.

**Happy Contributing! 🚀**
