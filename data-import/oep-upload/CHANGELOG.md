# Changelog
All notable changes to this project will be documented in this file.

The format is inpired from [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and the versiong aim to respect [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

Here is a template for new release sections

```
Template:

## Current
### Added
- basic description
### Changed
- basic description
### Removed
- basic description

## [_._._] - 20XX-MM-DD

### Added
- basic description [#PR/#Issue/#Commit]
### Changed
- basic description [#PR/#Issue/#Commit]
### Removed
- basic description [#PR/#Issue/#Commit]
```
## Current

### Added
- Support to setup the OEP API-URL
- Metadata Up- and download are supported
- Save downloaded metadata to file
- Validate metadata using OMI parser v1.4.0

### Changed
- IMPORTANT: change functions names in #COMMIT


## [0.2.4] - 2020-06-02


## [0.2.3] - 2020-06-02

### Added
- provide a minimal working example as jupyter notebook tutorial
- New OEP-API related functions: Prepare the oemetadata string to send to api 
    Simple User Input function to set the OEP-API-Token

### Changed
- Update README
- include OEP public schema (whitelist) check
- Spatial types from Geoalchemy2 do not set a spatial_index anymore


## [0.2.2] - 2020-06-02

### Added
- new function: setting up a logger

### Changed
- add missing input parameter
- extended description in changelog
- Fix logging 


## [0.2.0] - 2020-05-27

### Added
- new function: delete tables from DB now possible
- new function: select the oem data folder 
- new function: tables are collected and ordered by fk (increase usability)

### Changed
- added docstrings 

### Removed
- the user is no longer required to use a for loop in the main function to collect tables




