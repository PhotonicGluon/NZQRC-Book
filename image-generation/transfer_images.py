import os
import re
import shutil
from typing_extensions import Annotated

from rich import print
import typer


MEDIA_FOLDER = "media/images/image-generation"
BOOK_IMAGES_FOLDER = "../book/images"

IMAGE_REGEX = r"(?P<part>\d)-(?P<chapter>[a-z]+)-(?P<name>\w+\.png)"


def main(
    copy_images: Annotated[
        bool, typer.Option(help="If true, will make a copy of the images. If false, will move the images instead.")
    ] = True,
    dry_run: Annotated[bool, typer.Option(help="Whether to dry run the moving of images.")] = False,
    silent: Annotated[bool, typer.Option(help="Whether to silence info.")] = False
):
    """
    Transfers images from the media folder into the actual book's folder.
    """

    if dry_run:
        print("[yellow]Dry run mode.[/yellow]")

    # Get all images
    images = os.listdir(MEDIA_FOLDER)

    for image in images:
        match = re.match(IMAGE_REGEX, image)
        if not match:
            continue
        part, chapter, name = match.groups()

        # Create appropriate folder
        folder = os.path.join(BOOK_IMAGES_FOLDER, f"part-{part}", chapter)

        if not dry_run:
            os.makedirs(folder, exist_ok=True)
        if not silent:
            print(f"Created folder [cyan]'{folder}'[/cyan]")

        # Transfer image
        src = os.path.join(MEDIA_FOLDER, image)
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


if __name__ == "__main__":
    typer.run(main)
