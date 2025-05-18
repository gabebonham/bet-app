import glob
import os
from datetime import datetime
import sys

from pathlib import Path
def get_base_path():
    """Get the correct base path for both dev and PyInstaller"""
    if getattr(sys, 'frozen', False):
        # Running in compiled mode
        return Path(sys.executable).parent
    else:
        # Running in development
        return Path(__file__).parent.parent  # Goes up from app/services

def get_generated_path():
    """Get the correct path to generated files"""
    base = get_base_path()
    path = os.path.join(base,'../generated')
    return path
BASE_DIR = get_base_path()
GENERATED_PATH = get_generated_path()


def get_most_recent_file(base_name, extension):
    """
    Finds the most recent file in the generated directory matching the pattern:
    base_name_DD-MM-YYYY_HH-MM-SS.extension
    
    Args:
        base_name (str): The base name of the file (e.g., "predictions")
        extension (str): File extension without dot (e.g., "csv")
    
    Returns:
        str: Full path to the most recent matching file
        None: If no matching file is found
    """
    # Determine the correct generated directory path
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        if hasattr(sys, '_MEIPASS'):
            # Try MEIPASS first
            gen_dir = Path(sys._MEIPASS) / 'generated'
        else:
            # Fallback to executable directory
            gen_dir = Path(sys.executable).parent / 'generated'
    else:
        # Running in development
        gen_dir = Path(__file__).parent.parent / 'generated'
    
    # Build search pattern
    pattern =  os.path.join(get_generated_path(),f"{base_name}_*.{extension}")
    
    # Find all matching files
    files = glob.glob(pattern)
    
    if not files:
        return None
    
    # Find the most recently created file
    most_recent = max(files, key=os.path.getctime)
    
    return most_recent
