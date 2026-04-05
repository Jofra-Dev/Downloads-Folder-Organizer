import shutil
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

def move_file(file, base_path, category):
    """Move file to categorized folder, handling duplicates with timestamp"""
    try:
        target_dir = Path(base_path) / category
        target_dir.mkdir(exist_ok=True, parents=True)
        
        target_path = target_dir / file["name"]
        
        # Handle duplicate filenames
        if target_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name_parts = file["name"].rsplit(".", 1)
            if len(name_parts) == 2:
                new_name = f"{name_parts[0]}_{timestamp}.{name_parts[1]}"
            else:
                new_name = f"{file['name']}_{timestamp}"
            target_path = target_dir / new_name
            logger.info(f"File exists, renaming to: {new_name}")
        
        if not file["path"].exists():
            logger.warning(f"File {file['path']} no longer exists, skipping")
            return
        
        shutil.move(str(file["path"]), str(target_path))
        logger.info(f"Moved: {file['name']} -> {category}/{target_path.name}")
        
    except Exception as e:
        logger.error(f"Error moving file {file['name']}: {e}")