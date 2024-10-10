from typing import Optional

from PIL import Image, ImageChops
from rich import print


def trim(im: Image.Image, throw_if_cannot_trim: bool = True, add_excess_of: int = 0) -> Optional[Image.Image]:
    """
    Trims excess background from the image.

    Args:
        im: image to trim background from.
        throw_if_cannot_trim: whether to throw an error if we cannot trim image. Defaults to True.
        add_excess_of: number of pixels to surround the main content. Defaults to 0.

    Raises:
        ValueError: if trimming is impossible and `throw_if_cannot_trim` is set.

    Returns:
        the trimmed image, or None if cannot trim.
    """

    # Ensure image is in RGB mode
    im = im.convert("RGB")  # RGBA will ruin things

    # Generate pure background based on top left-hand corner
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))

    # Get main 'content' image
    diff = ImageChops.difference(im, bg)

    # Bound to content
    bbox = diff.getbbox()
    if not bbox:
        if throw_if_cannot_trim:
            raise ValueError("No bounding box; cannot trim")
        else:
            print("[yellow]No bounding box; cannot trim[/yellow]")
            return None

    # Expand bounding box by `add_excess_of` pixels
    crop_to = (
        max(bbox[0] - add_excess_of, 0),
        max(bbox[1] - add_excess_of, 0),
        min(bbox[2] + add_excess_of, im.size[0]),
        min(bbox[3] + add_excess_of, im.size[1]),
    )
    return im.crop(crop_to)
