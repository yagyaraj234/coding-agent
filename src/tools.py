import os
import json

def run_command(item:dict):
    """"Run commands in a shell."""
    command = item["command"]
  
    os.system(command)
    return command

def get_file_content(item:dict) -> str:
    """Get the content of a file."""
    file_name = item.get("path")
    
    # Check if the file exists
    file_path = check_file_exists(file_name)

    with open(file_path, "r") as file:
        content = file.read()
    return content

def get_temperature(city):

    return "34 c"

def edit_file(item:dict) -> str:
    """Edit a file with the given content."""
    file_name = item.get("file_name")
    updated_content = item.get("updated_content")

    with open(file_name, "w") as file:
        file.write(updated_content)
    return updated_content


def check_file_exists(file_path: str) -> str or bool:
    """
    Check if a file exists in the specified path, current directory, or subdirectories,
    excluding node_modules and __pycache__.
    
    Args:
        file_path: Path to file (can be just filename or path like server/server.js)
    
    Returns:
        The actual path to the file if found, False otherwise
    """
    # First check if the exact path exists
    if os.path.isfile(file_path):
        return file_path
    
    # Extract just the filename from the path
    file_name = os.path.basename(file_path)
    
    # Check if path components were given (like server/server.js)
    path_components = os.path.dirname(file_path)
    
    # If path components exist, check that specific path under current directory
    if path_components:
        local_path = os.path.join(".", file_path)
        if os.path.isfile(local_path):
            return local_path
    
    # If not found, search all subdirectories
    for root, dirs, files in os.walk("."):
        # Exclude node_modules and __pycache__ directories
        dirs[:] = [d for d in dirs if d not in ['node_modules', '__pycache__']]
        if file_name in files:
            return os.path.join(root, file_name)
            
    return False