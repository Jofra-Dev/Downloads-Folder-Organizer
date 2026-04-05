from config import RULES

def classify(file):
    """Determine file category based on extension"""
    for folder, extensions in RULES.items():
        if file["ext"] in extensions:
            return folder
    return "Others"