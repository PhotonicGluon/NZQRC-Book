from typing import Tuple


def hex_to_rgb(rgb_as_hex: str) -> Tuple[int, int, int]:
    """
    Convert a hex color code to an RGB tuple.

    Args:
        rgb_as_hex (str): The hex color code to convert to RGB.

    Returns:
        Tuple[int, int, int]: The RGB values as a tuple of integers.
    """

    rgb_as_hex = rgb_as_hex.lstrip("#")
    return tuple(int(rgb_as_hex[i : i + 2], 16) for i in (0, 2, 4))
