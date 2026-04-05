import argparse
import logging
import sys
from pathlib import Path
from watchdog.observers import Observer
import time

from watcher import OrganizerHandler

def setup_logging(log_level=logging.INFO, log_file=None):
    """Configure logging to console and optionally to file"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(exist_ok=True, parents=True)
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=handlers
    )

def run_watcher(path, recursive=False, cooldown=5):
    """Start the file system watcher"""
    path = Path(path).expanduser().resolve()
    
    if not path.exists():
        logging.error(f"Path does not exist: {path}")
        return False
    
    if not path.is_dir():
        logging.error(f"Path is not a directory: {path}")
        return False
    
    event_handler = OrganizerHandler(path, cooldown_seconds=cooldown)
    observer = Observer()
    
    observer.schedule(event_handler, str(path), recursive=recursive)
    observer.start()
    
    logging.info(f"Started watching: {path}")
    logging.info(f"Recursive: {recursive}, Cooldown: {cooldown}s")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Received shutdown signal")
        observer.stop()
    
    observer.join()
    logging.info("Watcher stopped")
    return True

def main():
    parser = argparse.ArgumentParser(description="File Organizer Service - Automatically organize files by type")
    parser.add_argument("path", nargs="?", default="~/Downloads", 
                       help="Path to watch (default: ~/Downloads)")
    parser.add_argument("--recursive", "-r", action="store_true",
                       help="Watch subdirectories recursively")
    parser.add_argument("--cooldown", "-c", type=int, default=5,
                       help="Cooldown seconds between processing same file (default: 5)")
    parser.add_argument("--log-level", "-l", default="INFO",
                       choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       help="Logging level (default: INFO)")
    parser.add_argument("--log-file", "-f", default="/var/log/file-organizer/app.log",
                       help="Log file path (default: /var/log/file-organizer/app.log)")
    parser.add_argument("--config", default="config.json",
                       help="Configuration file path (default: config.json)")
    
    args = parser.parse_args()
    
    setup_logging(getattr(logging, args.log_level), args.log_file)
    
    import config
    config.load_config(args.config)
    
    success = run_watcher(args.path, args.recursive, args.cooldown)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()