import os
import shutil
from pathlib import Path

from rich import print


def transfer_images(
    media_folder: str, book_image_folder: str, copy_images: bool = True, dry_run: bool = False, silent: bool = False
):
    """
    Transfers images from the media folder into the actual book's folder.

    Args:
        media_folder: media folder that contains all the images.
        book_image_folder: book's actual image folder.
        copy_images: whether to copy the images or just move them. Defaults to True.
        dry_run: whether to perform a dry run. Defaults to False.
        silent: whether extra output should be made. Defaults to False.
    """

    if dry_run:
        print("[yellow]Dry run mode.[/yellow]")

    # Get all images
    images = Path(media_folder).glob("**/*.png")

    for image in images:
        # Get components of the image
        part = image.parent.parent.name
        chapter = image.parent.name
        name = image.name

        # Create appropriate folder
        folder = os.path.join(book_image_folder, part, chapter)

        if not dry_run and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
            if not silent:
                print(f"Created folder [cyan]'{folder}'[/cyan]")

        # Transfer image
        dst = os.path.join(folder, name)
        if copy_images:
            if not dry_run:
                shutil.copy(image, dst)
            if not silent:
                print(f"Copied [cyan]'{image}'[/cyan] to [cyan]'{dst}'[/cyan]")
        else:
            if not dry_run:
                shutil.move(image, dst)
            if not silent:
                print(f"Moved [cyan]'{image}'[/cyan] to [cyan]'{dst}'[/cyan]")

    print("[green]Done![/green]")
