# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-01

### Added
- **Complete API redesign** - Clean, simple, and professional bot library
- **Event-driven architecture** - Intuitive decorator-based handlers
- **Single Bot class** - No more complex dispatcher/router/middleware layers
- **Professional naming** - Clean, intuitive method and class names
- **Modern tooling** - pytest, black, ruff, flake8 for quality assurance
- **Comprehensive testing** - Full test coverage with async support

### Removed
- ❌ Complex dispatcher/router system (like aiogram)
- ❌ Middleware layers and filters complexity
- ❌ Conversation state management overhead
- ❌ Unnecessary abstractions and layers
- ❌ Old documentation and examples

### Changed
- **Simplified API** - From complex multi-class system to single Bot class
- **Better performance** - Direct event handling without middleware overhead
- **Cleaner code** - Professional naming and modern Python practices
- **Improved documentation** - Clear, concise README with examples

## [0.2.0] - 2024-06-01

### Added
- Media handling utilities for downloading and uploading files
- Conversation state management for multi-step interactions
- Rate limiting middleware to prevent abuse
- Enhanced webhook support with custom routes
- Inline query handling with result builders
- Comprehensive documentation with Read the Docs support
- New example files demonstrating advanced features

### Changed
- Improved error handling in core components
- Enhanced type hints for better IDE support
- Updated dependencies for better compatibility

### Fixed
- Various bug fixes and performance improvements

## [0.1.0] - 2024-05-01

### Added
- Initial release
- Core Bot, Dispatcher, and Router classes
- Basic message handling with filters
- Callback query support
- Inline keyboard builder
- Reply keyboard builder
- Simple examples
