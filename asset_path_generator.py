import os

def find_pngs(folder_path, found_files=None):
    if found_files is None:
        found_files = {}

    try:
        with os.scandir(folder_path) as it:
            for entry in it:
                if entry.is_file() and entry.name.lower().endswith('.png'):
                    found_files[os.path.basename(entry.path)] = entry.path
                elif entry.is_dir():
                    find_pngs(entry.path, found_files)
    except PermissionError as e:
        print(f"Permission denied: {folder_path} - skipping")

    return found_files

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        root_folder = sys.argv[1]
    else:
        root_folder = os.getcwd()

    png_files = find_pngs(root_folder)

    print(f"Found {len(png_files)} .png files:")
    for file in png_files:
        print(file)
