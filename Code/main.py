import os
import shutil
from pathlib import Path
from datetime import datetime


class FileOrganizer:
    """Organize files in a directory by type, date, or size."""
    
    # File type categories
    FILE_TYPES = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx', '.csv'],
        'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.m4a', '.wma'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.iso'],
        'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.rs', '.go'],
        'Data': ['.json', '.xml', '.sql', '.db', '.sqlite'],
    }
    
    def __init__(self, directory):
        """Initialize the organizer with a target directory."""
        self.directory = Path(directory)
        if not self.directory.exists():
            raise ValueError(f"Directory does not exist: {directory}")
        if not self.directory.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")
    
    def organize_by_type(self):
        """Organize files by file type/extension."""
        print(f"\n📁 Organizing files by type in: {self.directory}")
        files_moved = 0
        
        # Create category folders and move files
        for category, extensions in self.FILE_TYPES.items():
            category_path = self.directory / category
            category_path.mkdir(exist_ok=True)
            
            for file_path in self.directory.glob('*'):
                if file_path.is_file() and file_path.suffix.lower() in extensions:
                    try:
                        dest = category_path / file_path.name
                        shutil.move(str(file_path), str(dest))
                        print(f"  ✓ {file_path.name} → {category}/")
                        files_moved += 1
                    except Exception as e:
                        print(f"  ✗ Error moving {file_path.name}: {e}")
        
        # Move uncategorized files to "Other"
        other_path = self.directory / "Other"
        other_path.mkdir(exist_ok=True)
        
        for file_path in self.directory.glob('*'):
            if file_path.is_file():
                try:
                    dest = other_path / file_path.name
                    shutil.move(str(file_path), str(dest))
                    print(f"  ✓ {file_path.name} → Other/")
                    files_moved += 1
                except Exception as e:
                    print(f"  ✗ Error moving {file_path.name}: {e}")
        
        print(f"\n✅ Organized {files_moved} files by type!\n")
    
    def organize_by_date(self):
        """Organize files by creation/modification date."""
        print(f"\n📅 Organizing files by date in: {self.directory}")
        files_moved = 0
        
        for file_path in self.directory.glob('*'):
            if file_path.is_file():
                try:
                    # Get modification time
                    mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    year_month = mod_time.strftime("%Y-%m")
                    
                    # Create year/month folder
                    date_folder = self.directory / year_month
                    date_folder.mkdir(exist_ok=True)
                    
                    dest = date_folder / file_path.name
                    shutil.move(str(file_path), str(dest))
                    print(f"  ✓ {file_path.name} → {year_month}/")
                    files_moved += 1
                except Exception as e:
                    print(f"  ✗ Error moving {file_path.name}: {e}")
        
        print(f"\n✅ Organized {files_moved} files by date!\n")
    
    def organize_by_size(self):
        """Organize files by size categories."""
        print(f"\n📊 Organizing files by size in: {self.directory}")
        files_moved = 0
        
        # Size categories in bytes
        categories = {
            'Small (< 1MB)': 1024 * 1024,
            'Medium (1-10MB)': 10 * 1024 * 1024,
            'Large (10-100MB)': 100 * 1024 * 1024,
            'Very Large (> 100MB)': float('inf'),
        }
        
        for file_path in self.directory.glob('*'):
            if file_path.is_file():
                try:
                    size = file_path.stat().st_size
                    
                    # Determine category
                    category = 'Very Large (> 100MB)'
                    for cat, limit in categories.items():
                        if size < limit:
                            category = cat
                            break
                    
                    # Create folder and move file
                    size_folder = self.directory / category
                    size_folder.mkdir(exist_ok=True)
                    
                    dest = size_folder / file_path.name
                    shutil.move(str(file_path), str(dest))
                    size_mb = size / (1024 * 1024)
                    print(f"  ✓ {file_path.name} ({size_mb:.2f}MB) → {category}/")
                    files_moved += 1
                except Exception as e:
                    print(f"  ✗ Error moving {file_path.name}: {e}")
        
        print(f"\n✅ Organized {files_moved} files by size!\n")
    
    def show_stats(self):
        """Display statistics about files in the directory."""
        print(f"\n📊 File Statistics for: {self.directory}")
        print("-" * 50)
        
        total_files = 0
        total_size = 0
        extensions = {}
        
        for file_path in self.directory.rglob('*'):
            if file_path.is_file():
                total_files += 1
                total_size += file_path.stat().st_size
                ext = file_path.suffix.lower() or "no extension"
                extensions[ext] = extensions.get(ext, 0) + 1
        
        print(f"Total files: {total_files}")
        print(f"Total size: {total_size / (1024**2):.2f}MB")
        print(f"\nFile types:")
        for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
            print(f"  {ext}: {count}")
        print("-" * 50 + "\n")


def main():
    """Main menu interface."""
    print("=" * 50)
    print("  📁 FILE ORGANIZER")
    print("=" * 50)
    
    # Get directory from user
    directory = input("\nEnter directory path (or press Enter for current): ").strip()
    if not directory:
        directory = "."
    
    try:
        organizer = FileOrganizer(directory)
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    while True:
        print("\n--- OPTIONS ---")
        print("1. Organize by Type (Images, Documents, etc.)")
        print("2. Organize by Date (Year-Month)")
        print("3. Organize by Size")
        print("4. Show Statistics")
        print("5. Exit")
        
        choice = input("\nChoose an option (1-5): ").strip()
        
        if choice == '1':
            organizer.organize_by_type()
        elif choice == '2':
            organizer.organize_by_date()
        elif choice == '3':
            organizer.organize_by_size()
        elif choice == '4':
            organizer.show_stats()
        elif choice == '5':
            print("\n👋 Goodbye!\n")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
