def bytesToTB(bytes):
    """
    Converts bytes to terabytes.

    Args:
        bytes (int): The number of bytes to convert.

    Returns:
        float: The equivalent value in terabytes.
    """
    return round(bytes / 1024 / 1024 / 1024 / 1024, 3)