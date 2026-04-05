from pathlib import Path

def scan_folder(path: str):
    """Scan directory and return list of files with metadata"""
    files = []
    for file in Path(path).iterdir():
        if file.is_file():
            files.append({
                "path": file,
                "name": file.name,
                "ext": file.suffix.lower(),
                "size": file.stat().st_size
            })
    return files