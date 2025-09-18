import os

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def list_files(directory, extensions=None):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if not extensions or filename.endswith(tuple(extensions)):
                files.append(os.path.join(root, filename))
    return files
