import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def load_config(config_path="config.json"):
    """Load configuration from JSON file with fallback defaults"""
    default_config = {
        "Images": [".jpg", ".png", ".jpeg", ".gif", ".bmp", ".svg"],
        "Docs": [".pdf", ".docx", ".txt", ".md", ".csv", ".xlsx", ".pptx"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
        "Audio": [".mp3", ".wav", ".flac", ".aac"],
        "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"]
    }
    
    try:
        config_path = Path(config_path)
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
                logger.info(f"Configuration loaded from {config_path}")
                return config
        else:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return default_config
    except Exception as e:
        logger.error(f"Error loading config: {e}, using defaults")
        return default_config

RULES = load_config()