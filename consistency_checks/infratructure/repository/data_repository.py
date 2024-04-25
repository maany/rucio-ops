import os
def list_files(directory):
    """
    Returns a list of files in the specified directory.

    Args:
        directory (str): The directory path.

    Returns:
        list: A list of file names in the directory.
    """
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
