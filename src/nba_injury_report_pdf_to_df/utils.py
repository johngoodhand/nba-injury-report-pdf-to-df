from pathlib import Path


def path(folder, file_name, levels_up=1):
    """
    Generates a path to a file using pathlib, allowing customization of how many levels up 
    to navigate from the current script's directory.

    Parameters:
    folder (str): The folder name where the file is located.
    file_name (str): The name of the file.
    levels_up (int, optional): The number of directory levels to move up from 
                               the script's directory. Defaults to 1.

    Returns:
    Path: A pathlib Path object representing the full file path.
    """

    # Start with the current file's directory
    base_path = Path(__file__).parent

    # Move up 'levels_up' times
    for _ in range(levels_up):
        base_path = base_path.parent

    # Generate the full path
    file_path = base_path / folder / file_name

    return file_path