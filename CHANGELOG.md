# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-06

### Added
- Initial release
- Standalone Windows EXE application
- Three operation modes:
  - Quick paste and split (fastest)
  - Select single image (interactive)
  - Batch process folder (multiple images)
- Auto-crop transparent edges using PIL/Pillow
- Element segmentation using SciPy connected components
- Preserve RGBA transparency in output
- Auto-open output folder
- GUI application with progress bar
- Complete documentation
- Python source code for modification

### Features
- Automatic transparent edge detection and removal
- Connected component labeling for element separation
- Support for PNG RGBA format preservation
- Game engine compatible output (Godot, Unity, Unreal, etc.)
- Fast processing (< 1 second per image)
- Batch processing with visual progress

### Technical
- Built with Python 3.8+
- Dependencies: Pillow, NumPy, SciPy
- Packaged with PyInstaller
- Cross-platform Python source
- Windows EXE application (~55 MB)

## [Unreleased]

### Planned
- Mac/Linux support
- Batch processing improvements
- Advanced filtering options
- Custom output formats
- Drag-and-drop support enhancement
