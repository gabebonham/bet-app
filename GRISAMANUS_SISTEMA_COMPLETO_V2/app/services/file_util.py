import glob
import os
from datetime import datetime
import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GENERATED_PATH = os.path.join(BASE_DIR, 'generated')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))
def get_most_recent_file(name,directory="../"):
    """
    Finds the most recent prediction file based on timestamp in filename.
    Files should be in format: pred_%d-%m-%Y_%H-%M-%S.csv
    
    Args:
        directory (str): Directory to search in (defaults to current directory)
    
    Returns:
        str: Path to most recent matching file, or None if none found
    """
    # Find all matching files
    pattern = os.path.join(GENERATED_PATH, name+"_*.csv")
    files = glob.glob(pattern)
    
    if not files:
        return None
    
    # Extract dates from filenames and sort
    dated_files = []
    for file in files:
        try:
            # Extract the datetime part (between 'pred_' and '.csv')
            datetime_str = os.path.basename(file)[5:-4]
            dt = datetime.strptime(datetime_str, "%d-%m-%Y_%H-%M-%S")
            dated_files.append((dt, file))
        except ValueError:
            # Skip files that don't match our pattern
            continue
    
    if not dated_files:
        return None
    
    # Sort by datetime (most recent first)
    dated_files.sort(reverse=True, key=lambda x: x[0])
    
    # Return path of most recent file
    return dated_files[0][1]
def get_most_recent_file_prev(name, directory="."):
    """
    Finds the most recent file based on timestamp in filename.
    
    Args:
        name (str): Base name pattern to match (e.g., 'tabela' for 'tabela_*.csv')
        directory (str): Directory to search in (defaults to current directory)
    
    Returns:
        str: Path to most recent matching file
    Raises:
        FileNotFoundError: If no matching files are found
    """
    # Normalize directory path
    directoryy = os.path.normpath(__file__)
    directory = os.path.normpath(directory)
    directoryyy = os.path.join(directoryy, '..')
    directoryyy = os.path.join(directoryyy, directory)
    # Find all matching files
    pattern = os.path.join(directoryyy, f"{name}_*.csv")
    files = glob.glob(pattern)
    
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo encontrado com o padrão: {pattern}")
    
    # Extract dates from filenames
    dated_files = []
    for file in files:
        try:
            # Extract the datetime part (between 'name_' and '.csv')
            base_name = os.path.basename(file)
            datetime_str = base_name[len(name)+1:-4]  # +1 for the underscore
            dt = datetime.strptime(datetime_str, "%d-%m-%Y_%H-%M-%S")
            dated_files.append((dt, file))
        except ValueError:
            continue
    
    if not dated_files:
        raise FileNotFoundError(f"Nenhum arquivo válido encontrado com timestamp no padrão: {name}_DD-MM-YYYY_HH-MM-SS.csv")
    
    # Sort by datetime (most recent first)
    dated_files.sort(reverse=True, key=lambda x: x[0])
    
    return dated_files[0][1]


def get_most_recent_file_prev(name, directory="."):
    """
    Finds the most recent file based on timestamp in filename.
    
    Args:
        name (str): Base name pattern to match (e.g., 'tabela' for 'tabela_*.csv')
        directory (str): Directory to search in (defaults to current directory)
    
    Returns:
        str: Path to most recent matching file
    Raises:
        FileNotFoundError: If no matching files are found
    """
    
    # Find all matching files
    pattern = os.path.join(GENERATED_PATH, f"{name}_*.csv")
    files = glob.glob(pattern)
    
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo encontrado com o padrão: {pattern}")
    
    # Extract dates from filenames
    dated_files = []
    for file in files:
        try:
            # Extract the datetime part (between 'name_' and '.csv')
            base_name = os.path.basename(file)
            datetime_str = base_name[len(name)+1:-4]  # +1 for the underscore
            dt = datetime.strptime(datetime_str, "%d-%m-%Y_%H-%M-%S")
            dated_files.append((dt, file))
        except ValueError:
            continue
    
    if not dated_files:
        raise FileNotFoundError(f"Nenhum arquivo válido encontrado com timestamp no padrão: {name}_DD-MM-YYYY_HH-MM-SS.csv")
    
    # Sort by datetime (most recent first)
    dated_files.sort(reverse=True, key=lambda x: x[0])
    
    return dated_files[0][1]