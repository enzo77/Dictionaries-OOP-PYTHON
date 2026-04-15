"""
Project: File organizer using pathlib.

This class provides a simple interface to explore a directory,
list files and directories, group files by extension, and show
basic information such as size and modification date.

https://docs.python.org/3/library/pathlib.html
https://docs.python.org/3/library/datetime.html
"""

from pathlib import Path
from datetime import datetime


class FileOrganizer:

    def __init__(self, directory):
        """Create a FileOrganizer for a given directory."""
        self.path = Path(directory)
        self.entries = []

        self.scan()

    def scan(self):
        """Scan the directory and store its entries."""
        self.entries = []

        if not self.path.exists() or not self.path.is_dir():
            return

        for item in self.path.iterdir():
            self.entries.append(item)

    def list_all_entries(self):
        """Return the names of all files and directories."""
        names = []

        for item in self.entries:
            names.append(item.name)

        return names

    def list_all_files(self):
        """Return the names of all files."""
        files = []

        for item in self.entries:
            if item.is_file():
                files.append(item.name)

        return files

    def list_all_directories(self):
        """Return the names of all directories."""
        directories = []

        for item in self.entries:
            if item.is_dir():
                directories.append(item.name)

        return directories

    def list_extensions(self):
        """Return all file extensions found in the directory."""
        extensions = []

        for item in self.entries:
            if item.is_file():
                extension = item.suffix.lower()
                if extension not in extensions:
                    extensions.append(extension)

        return extensions

    def list_files(self, extension):
        """Return the files with a given extension."""
        if not extension.startswith("."):
            extension = "." + extension

        extension = extension.lower()
        files = []

        for item in self.entries:
            if item.is_file() and item.suffix.lower() == extension:
                files.append(item.name)

        return files

    def count_by_extension(self):
        """Return the number of files for each extension."""
        counts = {}

        for item in self.entries:
            if item.is_file():
                extension = item.suffix.lower()

                if extension not in counts:
                    counts[extension] = 0

                counts[extension] += 1

        return counts

    def detailed_listing(self):
        """Return detailed information similar to a simple ls command."""
        details = []

        for item in self.entries:
            info = {}

            info["name"] = item.name
            info["type"] = "directory" if item.is_dir() else "file"
            info["size"] = item.stat().st_size

            modified_timestamp = item.stat().st_mtime
            modified_date = datetime.fromtimestamp(modified_timestamp)
            info["modified"] = modified_date.strftime("%Y-%m-%d %H:%M:%S")

            details.append(info)

        return details


if __name__ == "__main__":

    organizer = FileOrganizer(".")

    print("=== ALL ENTRIES ===")
    print(organizer.list_all_entries())
    print()

    print("=== FILES ===")
    print(organizer.list_all_files())
    print()

    print("=== DIRECTORIES ===")
    print(organizer.list_all_directories())
    print()

    print("=== EXTENSIONS ===")
    print(organizer.list_extensions())
    print()

    print("=== PY FILES ===")
    print(organizer.list_files("py"))
    print()

    print("=== COUNT BY EXTENSION ===")
    print(organizer.count_by_extension())
    print()

    print("=== DETAILED LISTING ===")
    for entry in organizer.detailed_listing():
        print(entry)