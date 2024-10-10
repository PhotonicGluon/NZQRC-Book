from typing_extensions import Annotated

import typer

from src.transfer_images import transfer_images
from src.trim_images import trim_images


MEDIA_FOLDER = "media/images/image-generation"
BOOK_IMAGES_FOLDER = "../book/images"

IMAGE_REGEX = r"(?P<part>\d)-(?P<chapter>[a-z]+)-(?P<name>[\w\-]+\.png)"

app = typer.Typer()


@app.command(name="transfer-images")
def transfer_images_cmd(
    copy_images: Annotated[
        bool,
        typer.Option(
            help="If true, will make a copy of the images. If false, will move the images instead."
        ),
    ] = True,
    dry_run: Annotated[
        bool, typer.Option(help="Whether to dry run the moving of images.")
    ] = False,
    silent: Annotated[bool, typer.Option(help="Whether to silence info.")] = False,
):
    """
    Transfers images from the media folder into the actual book's folder.
    """

    transfer_images(MEDIA_FOLDER, BOOK_IMAGES_FOLDER, copy_images, dry_run, silent)


@app.command(name="trim-images")
def trim_images_cmd():
    # TODO: ADD
    trim_images()


if __name__ == "__main__":
    app()
