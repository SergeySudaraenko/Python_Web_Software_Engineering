import os
import sys
import shutil
from concurrent.futures import ThreadPoolExecutor

def process_file(source_file, target_dir):
    file_extension = os.path.splitext(source_file)[1][1:].lower()
    destination_dir = os.path.join(target_dir, file_extension)
    os.makedirs(destination_dir, exist_ok=True)
    shutil.copy(source_file, destination_dir)

def process_directory(source_dir, target_dir='dist'):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_file = os.path.join(root, file)
            with ThreadPoolExecutor() as executor:
                executor.submit(process_file, source_file, target_dir)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py source_dir [target_dir]")
        sys.exit(1)

    source_dir = sys.argv[1]
    target_dir = sys.argv[2] if len(sys.argv) > 2 else 'dist'
    process_directory(source_dir, target_dir)








