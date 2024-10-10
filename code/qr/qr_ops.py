from math import lcm
from typing import List, Optional, Tuple
import qrcode
from PIL import Image
from itertools import product


def create_qr(text: str, version: Optional[int] = None, box_size: int = 10, border: int = 0) -> Image.Image:
    """
    Generates a QR code for the specified text.

    Args:
        text: text to encode.
        version: QR code version. Defaults to automatically determining.
        box_size: side length of each 'box' in the QR code, in pixels. Defaults to 10.
        border: border around the QR code. Defaults to 0.

    Returns:
        QR code as a PIL image.
    """

    return qrcode.make(text, version=version, box_size=box_size, error_correction=qrcode.ERROR_CORRECT_H, border=border)


def create_split_qr(
    text: str, split: Tuple[int, int], version: Optional[int] = None, box_size: int = 10
) -> List[Image.Image]:
    # TODO: Add docs
    split_lcm = lcm(*split)

    # Generate the base QR code
    im_base = create_qr(text, version=version, box_size=1, border=0)
    length_in_boxes = im_base.size[0]

    # Ensure that the length in boxes are a multiple of the LCM
    if length_in_boxes % split_lcm == 0:
        ideal_length_in_boxes = length_in_boxes
    else:
        ideal_length_in_boxes = length_in_boxes + (split_lcm - length_in_boxes % split_lcm)

    ideal_length = ideal_length_in_boxes * box_size

    # Generate the actual QR code
    im = create_qr(text, version=version, box_size=box_size, border=0)
    orig_length = im.size[0]

    # Then get splitted images
    part_width = ideal_length // split[0]
    part_height = ideal_length // split[1]

    grid = product(range(0, ideal_length, part_height), range(0, ideal_length, part_width))
    parts = []
    for y, x in grid:
        box = (x, y, min(x + part_width, orig_length), min(y + part_height, orig_length))
        parts.append(im.crop(box))

    return parts
