# Release Notes Generator

A Python script that automatically generates release notes by comparing commits between the `develop` and `main` branches of a Git repository.

## Features

- Extracts commit messages between `develop` and `main` branches
- Excludes merge commits
- Clean, user-friendly output format focusing on commit messages
- Optional inclusion of commit dates and author information
- Supports both markdown and plaintext output formats
- Automatically saves output to the `outputs` directory
- Generates timestamped filenames for automatic outputs

## Requirements

- Python 3.x
- Git

## Usage

The script can be run from the command line with the following syntax:

```bash
python scripts/extract_release_notes.py <repo_path> [--format {markdown,plaintext}] [--output <filename>] [--include-date] [--include-author]
```

### Arguments

- `repo_path`: Path to your local Git repository (required)
- `--format`: Output format (optional, defaults to "markdown")
- `--output`: Output filename (optional, will be saved in outputs directory)
- `--include-date`: Include commit dates in the output (optional)
- `--include-author`: Include author names in the output (optional)

### Examples

1. Basic usage (generates timestamped file):
```bash
python scripts/extract_release_notes.py /path/to/your/repo
```

2. Specify custom filename:
```bash
python scripts/extract_release_notes.py /path/to/your/repo --output my_release_notes
```

3. Include dates and authors:
```bash
python scripts/extract_release_notes.py /path/to/your/repo --include-date --include-author
```

4. Generate plaintext output with dates:
```bash
python scripts/extract_release_notes.py /path/to/your/repo --format plaintext --include-date
```

## Output Format

The script generates release notes in the following format:

Basic output:
```markdown
- **Feature: Add new user authentication**
```

With dates and authors:
```markdown
- **Feature: Add new user authentication**
  - Date: 2024-03-28
  - Author: John Smith
```

## Output Location

- All output files are saved in the `outputs` directory
- If no filename is specified, a timestamped file is generated (e.g., `release_notes_20240328_143022.md`)
- The `.md` extension is automatically added if not provided
- The `outputs` directory is created automatically if it doesn't exist

## Notes

- The script compares commits between the `develop` and `main` branches
- Merge commits are automatically excluded
- If no new commits are found between the branches, a message will be displayed
- The script requires Git to be installed and accessible from the command line
