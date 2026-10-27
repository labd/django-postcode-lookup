# Changelog

All notable changes to this project are documented in this file.

## 3.0.0 - 2026-10-27

### Added

* Added support for Django 6.1

### Removed

* Removed support for Python 3.10, Python 3.11 or newer is now required

## 2.0.0 - 2026-10-12

### Added

* Added support for Django >= 5.2

### Changed

* Implemented changelog management via changie
* Replace setuptools for UV
* Replace flake8 for ruff

### Removed

* Removed support for Django < 5.2

## 1.0.1 - 2022-01-28

### Changed

* Set the current package version to 1.0.1.

## 1.0.0 - 2022-01-26

### Added

* Add Postcode API NU backend.

### Changed

* Major update of package.

## 0.4.0 - 2017-02-23

### Fixed

* Handle PostcodeLookupExceptions in the view.

## 0.3.0 - 2017-02-22

### Fixed

* Fix the apiwise backend.

## 0.2.0 - 2016-12-14

### Changed

* Publish a POST request instead of a GET request. This is also protected by a CSRF check.

## 0.1.0 - 2016-12-14

### Added

* Initial release.

