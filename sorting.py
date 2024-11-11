import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define paths
downloads_folder = os.path.expanduser("~/Downloads")
desktop_folder = os.path.expanduser("~/Desktop")

# Define file categories with associated extensions
file_categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm"],
    "Documents": [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".txt", ".csv"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Programs": [".exe", ".msi", ".dmg", ".pkg", ".deb"],
    "Others": []
}

# Create folders on the Desktop if they don't exist
for category in file_categories.keys():
    os.makedirs(os.path.join(desktop_folder, category), exist_ok=True)

class DownloadsHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Check for new files in the Downloads folder
        for filename in os.listdir(downloads_folder):
            file_path = os.path.join(downloads_folder, filename)

            # Skip directories and temporary files
            if os.path.isdir(file_path) or filename.startswith('.'):
                continue

            # Get file extension
            _, file_extension = os.path.splitext(filename)
            file_moved = False

            # Move files based on their extension
            for category, extensions in file_categories.items():
                if file_extension.lower() in extensions:
                    shutil.move(file_path, os.path.join(desktop_folder, category, filename))
                    print(f"Moved {filename} to {category} folder on Desktop.")
                    file_moved = True
                    break

            # If no matching category, move to "Others"
            if not file_moved:
                shutil.move(file_path, os.path.join(desktop_folder, "Others", filename))
                print(f"Moved {filename} to Others folder on Desktop.")

# Set up the observer
event_handler = DownloadsHandler()
observer = Observer()
observer.schedule(event_handler, downloads_folder, recursive=False)

# Start the observer
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
