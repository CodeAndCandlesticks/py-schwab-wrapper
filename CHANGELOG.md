# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2024-08-29
### Added
- Enhanced retry logic to avoid retrying on 401:Unauthorized errors.

### Fixed
- Bug #PBOT-218 was fixed to ensure token is valid prior to calling.

## [0.1.0] - 2024-08-27
### Added
- Initial release with support for get_price_history with automated retry function.
