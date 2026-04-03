import argparse
import shutil
from pathlib import Path
import logging
from collections import Counter

# Define file categories
CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".tiff"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".md", ".odt"},
    "Spreadsheets": {".xls", ".xlsx", ".csv"},
    "Presentations": {".ppt", ".pptx", ".key"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".m4a", ".ogg"},
    "Video": {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".webm"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".ts", ".java", ".html", ".css", ".json", ".sql", ".cpp", ".c", ".cs", ".rb", ".php"},
}

IGNORE_FILES = {".keep", "README.md", "sortify.log"}

#Log the file operations
def setup_logging(folder_path):
    log_file = folder_path / "sortify.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s", #Format for log messages
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

# Determine the category of a file
def get_category(file):
    for category, extensions in CATEGORIES.items():
        if file.suffix.lower() in extensions:
            return category
    return "Other" # Other for unrecognized file types

# Organize files into categories
def organize(folder, dry_run=False, recursive=False):
    summary = Counter()

    folder_path = Path(folder)

    if not folder_path.exists() or not folder_path.is_dir():
        print("Error: Folder does not exist.")
        return
    
    setup_logging(folder_path)
     
    if recursive:
        files = folder_path.rglob("*")
    else:
        files = folder_path.iterdir()

    for file in files:
        if file.parent.name in CATEGORIES or file.parent.name == "Other":
          continue

        if file.is_file():
            
            if file.name in IGNORE_FILES: #Ignore specific files
                continue

            category = get_category(file)
            new_folder = folder_path / category
            new_folder.mkdir(exist_ok=True)

            new_location = new_folder / file.name
            
            counter = 1

            # Summary tracker
            summary[category] += 1
            summary["total"] += 1

            
            while new_location.exists():
                new_location = new_folder / f"{file.stem}_{counter}{file.suffix}"
                counter += 1
            
            if dry_run:
                print(f"[DRY RUN] {file.name} → {category}/")
                logging.info("[DRY RUN] %s -> %s", file.name, new_location)
            else:
                shutil.move(str(file), str(new_location))
                print(f"Moved {file.name} → {category}/")
                logging.info("Moved %s -> %s", file.name, new_location)
    
   
    
    #Summary Printing
    print("\n===== SUMMARY =====")

    for category, count in sorted(summary.items()):
        if category != "total":
            print(f"{category}: {count}")

    print(f"Total: {summary['total']} files processed")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Folder to organize")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--recursive", action="store_true", help="Organize files in subfolders too")

    args = parser.parse_args()

    organize(args.folder, args.dry_run)

if __name__ == "__main__":
    main()