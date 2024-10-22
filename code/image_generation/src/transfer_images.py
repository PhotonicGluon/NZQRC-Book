import os
import re
import shutil

from rich import print

IMAGE_REGEX = r"(?P<part>\d)_(?P<chapter>[a-z\-]+)_(?P<name>[\w\-]+\.png)"


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
    images = os.listdir(media_folder)

    for image in images:
        match = re.match(IMAGE_REGEX, image)
        if not match:
            continue
        part, chapter, name = match.groups()

        # Create appropriate folder
        folder = os.path.join(book_image_folder, f"part-{part}", chapter)

        if not dry_run and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
            if not silent:
                print(f"Created folder [cyan]'{folder}'[/cyan]")

        # Transfer image
        src = os.path.join(media_folder, image)
        dst = os.path.join(folder, name)
        if copy_images:
            if not dry_run:
                shutil.copy(src, dst)
            if not silent:
                print(f"Copied [cyan]'{src}'[/cyan] to [cyan]'{dst}'[/cyan]")
        else:
            if not dry_run:
                shutil.move(src, dst)
            if not silent:
                print(f"Moved [cyan]'{src}'[/cyan] to [cyan]'{dst}'[/cyan]")

    print("[green]Done![/green]")
