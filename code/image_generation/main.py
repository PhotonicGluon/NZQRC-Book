import os
import shutil
import tempfile
from pathlib import Path
from typing import List, Optional

import typer
from rich import print
from typing_extensions import Annotated

from image_generation.cli.execute_notebooks import execute_notebooks
from image_generation.cli.transfer_images import transfer_images
from image_generation.cli.trim_images import trim_images

MEDIA_FOLDER = "media"
GENERATED_IMAGES_FOLDER = f"{MEDIA_FOLDER}/images"
BOOK_IMAGES_FOLDER = "../../book/images"

NOTEBOOKS_FOLDER = "notebooks"
ALL_NOTEBOOKS = [
    # Part 1
    "part-1/constructing-numbers.ipynb",
    "part-1/relations-1.ipynb",
    "part-1/functions.ipynb",
    "part-1/counting.ipynb",
    # Part 2
    "part-2/relations-2.ipynb",
]

app = typer.Typer(no_args_is_help=True)


@app.command(name="transfer")
def transfer_images_cmd(
    generated_images_folder: Annotated[
        Path,
        typer.Option(help="Folder containing the images to transfer.", exists=True, file_okay=False, dir_okay=True),
    ] = GENERATED_IMAGES_FOLDER,
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

    transfer_images(
        generated_images_folder,
        book_images_folder,
        copy_images=copy_images,
        dry_run=dry_run,
        silent=silent,
    )


@app.command(name="trim")
def trim_images_cmd(
    generated_images_folder: Annotated[
        Path,
        typer.Option(
            help="Folder containing the generated images to trim.", exists=True, file_okay=False, dir_okay=True
        ),
    ] = GENERATED_IMAGES_FOLDER,
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
        generated_images_folder,
        output_folder,
        throw_if_cannot_trim=throw_if_cannot_trim,
        add_excess_of=add_excess_of,
        silent=silent,
    )


@app.command("tat")
def trim_and_transfer_images_cmd(
    generated_images_folder: Annotated[
        Path,
        typer.Option(help="Folder containing the images to transfer.", exists=True, file_okay=False, dir_okay=True),
    ] = GENERATED_IMAGES_FOLDER,
    book_images_folder: Annotated[
        Path,
        typer.Option(help="Folder containing subfolders for the images.", exists=True, file_okay=False, dir_okay=True),
    ] = BOOK_IMAGES_FOLDER,
    temp_dir: Annotated[
        Optional[Path],
        typer.Option(
            help="Temporary directory to store the trimmed images. If `None` will generate a temporary directory automatically.",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ] = None,
    throw_if_cannot_trim: Annotated[
        bool, typer.Option("--throw", help="Whether to throw an error if we cannot trim image.")
    ] = False,
    add_excess_of: Annotated[int, typer.Option(help="Number of pixels to surround the main content.")] = 0,
    copy_images: Annotated[
        bool,
        typer.Option(help="Whether to copy the images. Otherwise will move the images instead."),
    ] = True,
    dry_run: Annotated[bool, typer.Option(help="Whether to dry run the moving of images.")] = False,
    silent: Annotated[bool, typer.Option(help="Whether to silence info.")] = False,
):
    """
    Performs trimming of the images, and then moves them to the book's image folder.
    """
    
    with tempfile.TemporaryDirectory() as tmpdir:
        if temp_dir:
            tmpdir = temp_dir

        # First trim the images using the temporary directory
        trim_images(
            generated_images_folder,
            tmpdir,
            throw_if_cannot_trim=throw_if_cannot_trim,
            add_excess_of=add_excess_of,
            silent=silent,
        )

        # Then transfer the images
        transfer_images(
            tmpdir,
            book_images_folder,
            copy_images=copy_images,
            dry_run=dry_run,
            silent=silent,
        )


@app.command("do-all")
def do_all_cmd(
    parts: Annotated[
        Optional[List[int]],
        typer.Option("--part", help="List of parts to generate. If not specified, will generate all parts."),
    ] = None,
    notebooks: Annotated[
        Optional[List[Path]],
        typer.Option(
            "--notebook",
            help="List of notebooks to generate. If not specified, will generate all notebooks. Overrides the `parts` option.",
            exists=True,
            dir_okay=False,
        ),
    ] = None,
    media_folder: Annotated[
        Path,
        typer.Option(help="Media folder.", dir_okay=True),
    ] = MEDIA_FOLDER,
    generated_images_folder: Annotated[
        Path,
        typer.Option(help="Folder that will contain the generated images.", dir_okay=True),
    ] = GENERATED_IMAGES_FOLDER,
    trimmed_images_folder: Annotated[
        Path,
        typer.Option(
            "--trimmed-images-folder",
            "-t",
            help="Folder to place the trimmed images.",
            dir_okay=True,
        ),
    ] = f"{MEDIA_FOLDER}/trimmed",
    book_images_folder: Annotated[
        Path,
        typer.Option(
            "--output-folder",
            "-o",
            help="Folder containing subfolders for the images.",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ] = BOOK_IMAGES_FOLDER,
):
    """
    A "do-all" command. Executes all notebooks, trims images, and then transfers images to the book
    folder.
    """

    # Clear the media folder
    if os.path.exists(media_folder):
        print(f"[yellow]Warning: this operation will delete the media folder '{media_folder}'[/yellow]")
        print("Press ENTER to proceed.", end="")
        input()

        shutil.rmtree(media_folder, ignore_errors=True)

    os.makedirs(media_folder, exist_ok=True)

    # Get the list of notebooks to execute
    if parts and notebooks:
        import warnings

        warnings.warn("Both parts and notebooks specified; will ignore parts.")
        parts = None

    if not parts and not notebooks:
        parts = range(0, 6)  # 0 to 5
    if notebooks:
        notebooks = [str(notebook) for notebook in notebooks]
    if parts:
        notebooks = []
        for part in parts:
            part_folder = f"{NOTEBOOKS_FOLDER}/part-{part}"
            if not os.path.isdir(part_folder):
                continue

            files_in_part_folder = os.listdir(part_folder)
            notebooks.extend([f"{part_folder}/{file}" for file in files_in_part_folder if file.endswith(".ipynb")])

    # Execute the notebooks
    if len(notebooks) == 0:
        print("[yellow]No notebooks to execute. Exiting.[/yellow]")
        exit(0)

    print("[cyan]Executing notebooks...[/cyan]")
    execute_notebooks(*notebooks)

    # Trim images
    print("[cyan]Trimming images...[/cyan]")
    trim_images(
        generated_images_folder,
        trimmed_images_folder,
        throw_if_cannot_trim=False,
        add_excess_of=0,
        silent=False,
    )

    # Transfer images
    print("[cyan]Transferring images...[/cyan]")
    transfer_images(
        trimmed_images_folder,
        book_images_folder,
        copy_images=True,
        dry_run=False,
        silent=False,
    )

    print("[b green]All done![/b green]")


if __name__ == "__main__":
    app()
