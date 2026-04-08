# Sortify

Sortify is a Python-based file organization tool that automatically sorts files into categorized folders based on file type. It includes both a command-line interface (CLI) and a desktop interface for safe and user-friendly operation.

---

## Features

- Automatic file sorting by type (Images, Documents, Audio, Video, Archives, Code, etc.)
- Dry Run mode (preview changes before moving files)
- Recursive mode (process files in subfolders)
- Duplicate file protection (auto-renames conflicting files)
- Logging system (records all actions to a log file)
- Summary report after execution
- Ignore rules for test/support files
- Desktop GUI with: Coming Soon!
  - Folder selection
  - Dry Run checkbox (enabled by default)
  - Recursive option
  - Confirmation warning before file movement
  - Open log file button

---

## Tech Stack

- Python
- pathlib (file system handling)
- shutil (file operations)
- argparse (CLI interface)
- logging
- collections.Counter
- Tkinter (GUI) - Coming Soon!

---

## CLI Usage

### Preview changes (recommended first)

```bash
python sortify.py "your-folder-path" --dry-run