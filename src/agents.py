import os


def run_command(command: str) -> str:
    """"Run commands in a shell."""
    print(f"Running command: {command}")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(BASE_DIR, ".."))
    os.system(command)
    return command


def edit_file(item:dict) -> str:
    """Edit a file with the given content."""
    file_name = item.get("file_name")
    updated_content = item.get("updated_content")

    print(f"Editing file: {file_name}")
    with open(file_name, "w") as file:
        file.write(updated_content)
    return updated_content

def check_file_exists(file_name: str) -> bool:
    """Check if a file exists in the current directory or any subdirectories, excluding node_modules and __pycache__."""
    for root, dirs, files in os.walk("."):
        # Exclude node_modules and __pycache__ directories
        dirs[:] = [d for d in dirs if d not in ['node_modules', '__pycache__']]
        if file_name in files:
            return os.path.join(root, file_name)
    return False