from pathlib import Path

import typer
from typing_extensions import Annotated

from image_generation.src.transfer_images import transfer_images
from image_generation.src.trim_images import trim_images


MEDIA_FOLDER = "media/images/image_generation"
BOOK_IMAGES_FOLDER = "../../book/images"

app = typer.Typer()


@app.command(name="transfer-images")
def transfer_images_cmd(
    media_folder: Annotated[
        Path,
        typer.Option(help="Folder containing the images to transfer.", exists=True, file_okay=False, dir_okay=True),
    ] = MEDIA_FOLDER,
    book_images_folder: Annotated[
        Path,
        typer.Option(help="Folder containing subfolders for the images.", exists=True, file_okay=False, dir_okay=True),
    ] = BOOK_IMAGES_FOLDER,
    copy_images: Annotated[
        bool,
        typer.Option(help="Whether to copy the images. Otherwise will move the images instead."),
    ] = True,
    dry_run: Annotated[bool, typer.Option(help="Whether to dry run the moving of images.")] = False,
    silent: Annotated[bool, typer.Option(help="Whether to silence info.")] = False,
):
    """
    Transfers images from the media folder into the actual book's folder.
    """

    transfer_images(media_folder, book_images_folder, copy_images, dry_run, silent)


@app.command(name="trim-images")
def trim_images_cmd(
    media_folder: Annotated[
        Path,
        typer.Option(help="Folder containing the images to trim.", exists=True, file_okay=False, dir_okay=True),
    ] = MEDIA_FOLDER,
    output_folder: Annotated[
        Path,
        typer.Option(
            "--output-folder",
            "-o",
            help="Folder to place the trimmed images.",
            dir_okay=True,
        ),
    ] = ...,
    throw_if_cannot_trim: Annotated[
        bool, typer.Option("--throw", help="Whether to throw an error if we cannot trim image.")
    ] = False,
    add_excess_of: Annotated[int, typer.Option(help="Number of pixels to surround the main content.")] = 0,
    silent: Annotated[bool, typer.Option(help="Whether to silence info.")] = False,
):
    """
    Trims images in the media folder and places it in the output folder.
    """

    trim_images(
        media_folder,
        output_folder,
        throw_if_cannot_trim=throw_if_cannot_trim,
        add_excess_of=add_excess_of,
        silent=silent,
    )


if __name__ == "__main__":
    app()
