from watchdog.events import FileSystemEventHandler
from pathlib import Path
import logging
import time

from classifier import classify
from move import move_file

logger = logging.getLogger(__name__)

def is_file_ready(path, max_wait=10):
    """Wait for file to finish downloading/copying by checking size stability"""
    try:
        if not path.exists():
            return False
            
        size1 = path.stat().st_size
        wait_time = 0
        
        while wait_time < max_wait:
            time.sleep(1)
            wait_time += 1
            
            if not path.exists():
                return False
                
            size2 = path.stat().st_size
            if size1 == size2:
                return True
            size1 = size2
        
        logger.warning(f"File {path.name} still changing after {max_wait}s, moving anyway")
        return True
    except Exception as e:
        logger.error(f"Error checking file readiness: {e}")
        return False

class OrganizerHandler(FileSystemEventHandler):
    
    def __init__(self, base_path, cooldown_seconds=5):
        self.base_path = Path(base_path)
        self.processed = set()
        self.last_processed = {}
        self.cooldown = cooldown_seconds
        logger.info(f"OrganizerHandler initialized for {self.base_path}")
    
    def should_process(self, file_path):
        """Check if file should be processed (not hidden, not temp, not in cooldown)"""
        if not file_path.exists():
            return False
        
        if file_path.name.startswith("."):
            return False
        
        # Skip temporary/downloading files
        skip_extensions = [".crdownload", ".part", ".tmp", ".download", ".opdownload"]
        if any(file_path.name.endswith(ext) for ext in skip_extensions):
            logger.debug(f"Skipping temporary file: {file_path.name}")
            return False
        
        # Prevent processing same file multiple times in quick succession
        current_time = time.time()
        if str(file_path) in self.last_processed:
            time_since_last = current_time - self.last_processed[str(file_path)]
            if time_since_last < self.cooldown:
                logger.debug(f"File {file_path.name} in cooldown ({time_since_last:.1f}s)")
                return False
        
        return True
    
    def process_file(self, file_path):
        try:
            if not self.should_process(file_path):
                return
            
            if not is_file_ready(file_path):
                logger.warning(f"File not ready: {file_path.name}")
                return
            
            self.processed.add(str(file_path))
            self.last_processed[str(file_path)] = time.time()
            
            # Skip files already in subdirectories
            if self.base_path in file_path.parents and file_path.parent != self.base_path:
                logger.debug(f"File already in subdirectory, skipping: {file_path}")
                return
            
            file = {
                "path": file_path,
                "name": file_path.name,
                "ext": file_path.suffix.lower(),
                "size": file_path.stat().st_size
            }
            
            category = classify(file)
            
            # Don't move if already in correct folder
            if file_path.parent.name == category:
                logger.debug(f"File already in correct category: {file_path}")
                return
            
            move_file(file, self.base_path, category)
            
            # Keep processed set manageable
            if len(self.processed) > 1000:
                self.processed = set(list(self.processed)[-500:])
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}", exc_info=True)
    
    def on_created(self, event):
        if not event.is_directory:
            logger.debug(f"File created: {event.src_path}")
            time.sleep(0.5)  # Brief delay for file system
            self.process_file(Path(event.src_path))
    
    def on_modified(self, event):
        if not event.is_directory:
            logger.debug(f"File modified: {event.src_path}")
            self.process_file(Path(event.src_path))
    
    def on_moved(self, event):
        if not event.is_directory:
            logger.debug(f"File moved to: {event.dest_path}")
            self.process_file(Path(event.dest_path))