# Contributing to Hygieia

Thank you for your interest in contributing to Hygieia! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect differing viewpoints and experiences

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, browser, versions)
   - Screenshots if applicable

### Suggesting Features

1. Check if the feature has been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Potential implementation approach
   - Examples from other applications (if any)

### Pull Requests

1. **Fork the repository**

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow code style guidelines
   - Write tests for new features
   - Update documentation
   - Keep commits atomic and well-described

4. **Test your changes**
   ```bash
   # Backend tests
   cd backend && pytest

   # Frontend tests
   cd frontend && npm test
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add feature: description"
   ```

   Follow commit message conventions:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes
   - `refactor:` Code refactoring
   - `test:` Test additions/changes
   - `chore:` Build/tooling changes

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Provide clear description
   - Reference related issues
   - Describe what was changed and why
   - Include screenshots for UI changes

## Development Setup

See [GETTING_STARTED.md](docs/GETTING_STARTED.md) for detailed setup instructions.

Quick start:
```bash
# Clone
git clone <your-fork-url>
cd hygieia

# Start services
docker-compose up -d

# Or local development
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

## Code Style

### Python (Backend)

- Follow PEP 8
- Use type hints
- Use Black for formatting
- Maximum line length: 100 characters

```bash
# Format code
black backend/

# Check style
flake8 backend/

# Type checking
mypy backend/
```

### TypeScript (Frontend)

- Follow TypeScript best practices
- Use functional components
- Use hooks for state management
- Meaningful variable names

```bash
# Lint
npm run lint

# Format
npm run format
```

### SQL

- Use uppercase for keywords
- Meaningful table/column names
- Include comments for complex queries

## Testing

### Backend Tests

```bash
cd backend
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest --cov              # Coverage report
pytest tests/test_api.py  # Specific file
```

Write tests for:
- API endpoints
- Data processing functions
- Database models
- Utility functions

### Frontend Tests

```bash
cd frontend
npm test              # Run all tests
npm test -- --coverage  # Coverage report
```

Write tests for:
- Components
- Utilities
- API services
- State management

## Documentation

- Update README.md for major changes
- Update API documentation in code
- Update user documentation in `docs/`
- Include JSDoc/docstrings for functions
- Comment complex logic

## Database Changes

1. Create migration:
   ```bash
   cd backend
   alembic revision --autogenerate -m "description"
   ```

2. Review generated migration

3. Test migration:
   ```bash
   alembic upgrade head
   alembic downgrade -1
   ```

4. Include migration in PR

## Adding New Integrations

When adding a new data source integration:

1. Create integration module in `backend/ingestion/`
2. Implement client class with standard methods
3. Add data normalization functions
4. Create Celery task for syncing
5. Add OAuth flow in `api/routers/auth.py`
6. Update frontend Settings page
7. Add documentation
8. Write tests

## Project Structure

```
hygieia/
├── backend/           # Python backend
│   ├── api/          # FastAPI application
│   ├── ingestion/    # Data collection
│   ├── analytics/    # Analysis engine
│   └── tests/        # Tests
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── tests/
├── docs/            # Documentation
└── database/        # Database scripts
```

## Review Process

1. Automated checks must pass (tests, linting)
2. At least one maintainer review required
3. Address review comments
4. Keep PR updated with main branch
5. Squash commits before merge (if requested)

## Questions?

- Open a discussion in GitHub Discussions
- Ask in issues
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
