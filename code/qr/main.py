import os
from pathlib import Path
import re
import shutil
from typing import Tuple

import typer
from rich import print
from typing_extensions import Annotated

from qr.src.ops import create_split_qr

IMAGE_FILE_REGEX = r"(?P<part>\d).png"
MESSAGE_FILE = "Message.txt"

IMAGES_FOLDER = "images"
BOOK_IMAGES_FOLDER = "../../book/images"

app = typer.Typer()


@app.command(name="generate")
def generate(
    split: Annotated[Tuple[int, int], typer.Option(help="Number of splits along width and height respectively.")],
    box_size: Annotated[int, typer.Option(help="Side length of each 'box' in the QR code, in pixels.")] = 10,
    version_penalty: Annotated[
        float,
        typer.Option(
            "--version-penalty", "--penalty", help="penalty to apply for versions. Higher versions get penalised more."
        ),
    ] = 0.25,
    resize: Annotated[bool, typer.Option(help="Whether to resize the splitted images.")] = False,
    invert: Annotated[bool, typer.Option(help="Whether to invert the splitted images.")] = False,
    transparent: Annotated[bool, typer.Option(help="Whether to make the *white* parts of the image transparent.")] = True,
    verbose: Annotated[bool, typer.Option(help="Whether to output extra information.")] = False,
):
    """
    Generates the splitted QR code images based on the message.
    """

    # Load the message first
    # with open(MESSAGE_FILE) as f:
    #     message = f.read()
    message = """4ZZToscbkyzUCPSAlTguJdRJ0xTVRmJ8KCoSLJGSrzmeATkAIlehHEQjdt0ErpS8cOZ514vAvq6YUkdRVr9TJCGUaP2QaeXMtHFwRReHa6F65ETfzOefSNGxwlgbW4kqelUbsQAN0rXESN7PmQ84mblgQuLIfq4GybWk7iz9XFTAmD86F3rQxH3kkxmwkp7rB919sfOPwSz8qvzvRHIds2YuC44cR1FerCqUNEmYl13gIlcyLoQj9Sd1cFq8PUC3ad3SZqM1lHAEg7GOKEL3oE2fUyIjWFVwrViBHGzfjVtwMr4dHyUTBCj93y1MpKF4ZWPrgGTc37io14IRm6zRyCfZAVUwNOxj7KxhuIjQzUO6XOlZugxK"""  # TODO: Remove

    # Generate the splitted QR code
    images = create_split_qr(
        message,
        split,
        box_size=box_size,
        version_penalty=version_penalty,
        resize=resize,
        invert=invert,
        transparent=transparent,
        verbose=verbose,
    )

    # Save them
    for i, image in enumerate(images):
        image.save(f"{IMAGES_FOLDER}/{i}.png")

    print("[green]Done![/green]")


@app.command(name="transfer")
def transfer(
    images_folder: Annotated[
        Path,
        typer.Option(help="Folder containing the images to transfer.", exists=True, file_okay=False, dir_okay=True),
    ] = IMAGES_FOLDER,
    book_images_folder: Annotated[
        Path,
        typer.Option(help="Folder containing images for the book.", exists=True, file_okay=False, dir_okay=True),
    ] = BOOK_IMAGES_FOLDER,
    copy_images: Annotated[
        bool,
        typer.Option(help="Whether to copy the images. Otherwise will move the images instead."),
    ] = True,
    final_name: Annotated[str, typer.Option(help="Name that the files should have at the destination.")] = "qr.png",
    dry_run: Annotated[bool, typer.Option(help="Whether to dry run the moving of images.")] = False,
    silent: Annotated[bool, typer.Option(help="Whether to silence info.")] = False,
):
    if dry_run:
        print("[yellow]Dry run mode.[/yellow]")

    # Get all images
    files = os.listdir(images_folder)

    for file in files:
        match = re.match(IMAGE_FILE_REGEX, file)
        if not match:
            continue
        part = match.group("part")

        # Create appropriate folder
        folder = os.path.join(book_images_folder, f"part-{part}")

        if not dry_run and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
            if not silent:
                print(f"Created folder [cyan]'{folder}'[/cyan]")

        # Transfer image
        src = os.path.join(images_folder, file)
        dst = os.path.join(folder, final_name)
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
    app()
