import json
import os
from pathlib import Path
import sys
import zipfile

main_dir = Path(__file__).parent.parent
out_dir = main_dir.joinpath('out')
src_dir = main_dir.joinpath('src')

if not main_dir.is_dir():
    print("Error: main directory not a valid folder")
    sys.exit()

if not src_dir.is_dir():
    print("Error: src directory doesn't exist")
    sys.exit

if not out_dir.is_dir():
    if out_dir.is_file():
        print("Error: output directory is already a file")
        sys.exit()
    else:
        out_dir.mkdir()

pack_version = None

try:
    with src_dir.joinpath('manifest.json').open('r') as f:
        manifest = json.load(f)
        version_vector = manifest['header']['version']
        pack_version = ".".join(str(x) for x in version_vector)

except FileNotFoundError:
    print("Error: manifest.json file not found")
    sys.exit()

except json.JSONDecodeError:
    print("Error: manifest.json is invalid")
    sys.exit()

if not isinstance(pack_version, str):
    print("Error: Can't parse version from manifest")
    sys.exit()

out_file_name = f"Server.Pack.{pack_version}.zip"
out_file = out_dir.joinpath(out_file_name)

with zipfile.ZipFile(out_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            file_path = os.path.join(root, file)
            archive_name = os.path.relpath(file_path, src_dir)
            zipf.write(file_path, archive_name)