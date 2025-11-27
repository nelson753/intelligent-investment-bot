# Contributing to Intelligent Investment Bot

Thank you for your interest in contributing! This project welcomes contributions from the community.

## How to Contribute

### Reporting Bugs
1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Include:
   - Python version
   - OS (Windows/Mac/Linux)
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs

### Suggesting Features
1. Open an issue with "Feature Request" label
2. Describe the feature and use case
3. Explain why it would be valuable
4. Consider implementation complexity

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest -v`)
6. Run benchmark to verify no regressions
7. Update documentation if needed
8. Commit with clear messages
9. Push to your fork
10. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/intelligent-investment-bot.git
cd intelligent-investment-bot

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -v

# Run benchmark
python intelligent_bot_tier1_full_benchmark.py
```

## Code Style

- Follow PEP 8
- Use descriptive variable names
- Add docstrings to functions/classes
- Comment complex logic
- Keep functions focused and small

## Testing Requirements

All PRs must:
- ✅ Pass all existing tests (59/59)
- ✅ Add tests for new features
- ✅ Maintain benchmark score ≥ 580/600 (97%)
- ✅ Not break any INQUEBRANTABLES

## Areas for Contribution

### Easy (Good First Issues)
- Documentation improvements
- Additional test cases
- Code comments
- Bug fixes
- Performance optimizations

### Medium
- New technical indicators
- Additional exchanges support
- Notification systems (email/SMS)
- Dashboard/UI improvements
- Backtesting enhancements

### Advanced
- Machine learning model improvements
- High-frequency trading mode
- Advanced portfolio strategies
- Sentiment analysis integration
- Multi-timeframe analysis

## INQUEBRANTABLES™ - DO NOT BREAK

These 6 core features are sacred and must never be removed or weakened:

1. **Kill Switch** - Always active, never bypassable
2. **Auto-Retraining** - Must remain weekly
3. **Multi-Asset** - Keep portfolio diversification
4. **API Redundancy** - Maintain 3 data sources
5. **Black Swan Detector** - Critical safety feature
6. **Cross-Validation** - Prevents overfitting

Any PR that weakens these will be rejected.

## Questions?

- Open a discussion on GitHub
- Tag maintainers in issues
- Be respectful and patient

## License

By contributing, you agree that your contributions will be licensed under the same dual license (Personal/Commercial) as the project.

---

**Thank you for helping make this project better! 🚀**
