# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2024-09-28
### Added
- Support for snake_case parameters for the get_price_history() method.
- Support to retrieve account information associated with the user.
- Support to place a orders: post_order (advanced), place_sigle_order, place_first_triggers_oco_order.

## [0.1.1] - 2024-08-29
### Added
- Enhanced retry logic to avoid retrying on 401:Unauthorized errors.

### Fixed
- Bug #PBOT-218 was fixed to ensure token is valid prior to calling.

## [0.1.0] - 2024-08-27
### Added
- Initial release with support for get_price_history with automated retry function.
