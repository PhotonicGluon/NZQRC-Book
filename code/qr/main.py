from typing import Tuple

import typer
from rich import print
from typing_extensions import Annotated

from qr.src.ops import create_split_qr

MESSAGE_FILE = "Message.txt"
IMAGES_FOLDER = "images"


def main(
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
        message, split, box_size=box_size, version_penalty=version_penalty, resize=resize, invert=invert, verbose=verbose
    )

    # Save them
    for i, image in enumerate(images):
        image.save(f"{IMAGES_FOLDER}/{i}.png")

    print("[green]Done![/green]")


if __name__ == "__main__":
    typer.run(main)
