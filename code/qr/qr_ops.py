from itertools import product
from math import lcm
from typing import List, Optional, Tuple

import qrcode
from PIL import Image

from qr.qr_consts import VERSION_LENGTHS


def create_qr(text: str, version: Optional[int] = None, box_size: int = 10, border: int = 0) -> qrcode.QRCode:
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

    qr = qrcode.QRCode(version=version, box_size=box_size, error_correction=qrcode.ERROR_CORRECT_H, border=border)
    qr.add_data(text)
    qr.make(fit=version is None)
    return qr


def find_best_qr_version(
    split: Tuple[int, int], min_version: int = 1, version_penalty: float = 0.25
) -> Tuple[int, int]:
    """
    Finds the best QR version for the best looking QR code split.

    Args:
        split: splits along width and height respectively.
        min_version: minimum QR code version. Defaults to 1.
        version_penalty: penalty to apply for versions. Higher versions get penalised more. Defaults
            to 0.25.

    Returns:
        a tuple. First integer is the best QR code version, second integer is the ideal block length
            for that version.
    """

    split_lcm = lcm(*split)

    min_error = 1e6
    best_version = None
    best_ideal_length = None
    for version in range(min_version, 41):
        # Get the version's length in boxes
        length = VERSION_LENGTHS[version - 1]

        # Calculate the ideal length
        if length % split_lcm == 0:
            # This is the perfect version!
            return version

        ideal_length = length + (split_lcm - length % split_lcm)

        # Find each part's width and height
        part_width = ideal_length // split[0]
        part_height = ideal_length // split[1]

        # Find the ending part's width and height
        last_width = length % part_width
        last_height = length % part_height

        # Compute the total error
        error = (part_width - last_width) / part_width + (part_height - last_height) / part_height
        error *= 1 + version_penalty * version

        if error < min_error:
            min_error = error
            best_version = version
            best_ideal_length = ideal_length

    return best_version, best_ideal_length


def create_split_qr(
    text: str,
    split: Tuple[int, int],
    box_size: int = 10,
    version_penalty: float = 0.25,
    resize: bool = False,
) -> List[Image.Image]:
    """
    Generates a splitted QR code.

    Args:
        text: text to encode.
        split: splits along width and height respectively.
        box_size: side length of each 'box' in the QR code, in pixels. Defaults to 10.
        version_penalty: penalty to apply for versions. Higher versions get penalised more. Defaults
            to 0.25.
        resize: whether to resize smaller parts to be the same size as the bigger parts. Defaults to
            False.

    Returns:
        list of parts of the QR code.
    """

    # Find the minimum version needed
    qr = create_qr(text, version=None, box_size=1)
    min_version = qr.version

    # Find the best version
    version, ideal_length_in_boxes = find_best_qr_version(
        split, min_version=min_version, version_penalty=version_penalty
    )

    # Generate the actual QR code
    qr = create_qr(text, version=version, box_size=box_size, border=0)
    im: Image.Image = qr.make_image()
    orig_length = im.size[0]

    # Then get splitted images
    ideal_length = ideal_length_in_boxes * box_size
    part_width = ideal_length // split[0]
    part_height = ideal_length // split[1]

    grid = product(range(0, ideal_length, part_height), range(0, ideal_length, part_width))
    parts = []
    for y, x in grid:
        box = (x, y, min(x + part_width, orig_length), min(y + part_height, orig_length))
        im_part = im.crop(box)
        if resize:
            im_part = im_part.resize((part_width, part_height))
        parts.append(im_part)

    return parts
