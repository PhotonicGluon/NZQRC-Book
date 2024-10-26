import os
from typing import Optional

from PIL import Image, ImageChops
from rich import print


def trim(im: Image.Image, throw_if_cannot_trim: bool = False, add_excess_of: int = 0) -> Optional[Image.Image]:
    """
    Trims excess background from the image.

    Args:
        im: image to trim background from.
        throw_if_cannot_trim: whether to throw an error if we cannot trim image. Defaults to False.
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
            return None

    # Expand bounding box by `add_excess_of` pixels
    crop_to = (
        max(bbox[0] - add_excess_of, 0),
        max(bbox[1] - add_excess_of, 0),
        min(bbox[2] + add_excess_of, im.size[0]),
        min(bbox[3] + add_excess_of, im.size[1]),
    )
    return im.crop(crop_to)


def trim_images(
    media_folder: str,
    output_folder: str,
    throw_if_cannot_trim: bool = False,
    add_excess_of: int = 0,
    silent: bool = False,
):
    """
    Trims images in the media folder and places it in the output folder.

    Args:
        media_folder: media folder that contains all the images.
        output_folder: folder to place the trimmed images.
        throw_if_cannot_trim: whether to throw an error if we cannot trim image. Defaults to True.
        add_excess_of: number of pixels to surround the main content. Defaults to 0.
        silent: whether extra output should be made. Defaults to False.
    """
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    images = os.listdir(media_folder)

    for image in images:
        im = Image.open(os.path.join(media_folder, image))
        trimmed_im = trim(im, throw_if_cannot_trim=throw_if_cannot_trim, add_excess_of=add_excess_of)

        if trimmed_im:
            trimmed_im.save(os.path.join(output_folder, image))
            if not silent:
                print(f"Trimmed [cyan]'{image}'[/cyan].")
        else:
            if not silent:
                print(f"[yellow]No bounding box for '{image}'; cannot trim.[/yellow]")

    print("[green]Done![/green]")
