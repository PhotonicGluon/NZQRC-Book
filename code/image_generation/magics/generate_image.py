import argparse
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional
import warnings

from IPython.core.magic import Magics, cell_magic, magics_class

from image_generation.magics.helpers import get_notebook_path

PACKAGE_DIR = Path(os.path.abspath(__file__)).parent.parent

DEFAULT_OUTPUT_DIR = f"{PACKAGE_DIR}/media/images"
DEFAULT_CONFIG_FILE = f"{PACKAGE_DIR}/manim.cfg"

the_notebook_path = None  # Will be updated once extension is loaded


def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension` can be loaded via
        %load_ext module.path
    or be configured to be autoloaded by IPython at startup time.
    """

    global the_notebook_path

    ipython.register_magics(GenerateImageMagic)
    the_notebook_path = get_notebook_path()
    print("Loaded extension.")


@magics_class
class GenerateImageMagic(Magics):
    """
    Helps generate the image using manim via a simplified interface.
    """

    # Helper methods
    @staticmethod
    def _parse_args(line: str, local_ns: Optional[Dict[str, Any]] = None) -> Optional[argparse.Namespace]:
        """
        Parses the command line arguments from a given line.

        Args:
            line: The input line containing the command and its arguments.
            local_ns: An optional namespace for argument parsing.

        Returns:
            The parsed arguments as a Namespace object, or None if parsing fails.
        """

        parser = argparse.ArgumentParser(prog="%%generate_image")

        # Mandatory arguments
        parser.add_argument("name", type=str, help="Image name. Separate words using '-'.")
        parser.add_argument("scene_name", type=str, help="Name of the scene class.")

        # Options
        parser.add_argument(
            "-C", "--config-file", type=str, default=DEFAULT_CONFIG_FILE, help="Path to the manim config file."
        )
        parser.add_argument(
            "-S", "--show-splash", action="store_true", help="Print splash message with version information."
        )
        parser.add_argument("-T", "--temp-dir", type=str, help="Temporary directory to store manim output.")
        parser.add_argument(
            "-O",
            "--output-dir",
            type=str,
            default=DEFAULT_OUTPUT_DIR,
            help=f"Directory to store the generated image. (Default = '{DEFAULT_OUTPUT_DIR}')",
        )

        # Parse the arguments
        try:
            return parser.parse_args(line.split(), namespace=local_ns)
        except SystemExit:
            return None

    # Main methods
    @cell_magic
    def generate_image(self, line: str, cell: str, local_ns: Optional[Dict[str, Any]] = None):
        """
        Generates an image using manim based on the provided scene and options.

        This cell magic command parses the input line to extract arguments and constructs
        a manim command to generate the specified scene image. The image is then saved
        to the specified output directory.

        Args:
            line: A string containing the command-line arguments specifying the part number, chapter
                ID, image name, and scene class name, along with optional flags.
            cell: The body of the cell containing the manim scene code to be executed.
            local_ns: An optional dictionary containing local namespace variables for argument
                parsing.
        """

        # Split the notebook's path into the part number and chapter ID
        notebook_file = the_notebook_path.name
        notebook_parent_folder = the_notebook_path.parent.name

        part_pattern = r"part-(?P<part>\d)"
        chapter_pattern = r"(?P<chapter>[\w-]+)\.ipynb"

        match = re.match(part_pattern, notebook_parent_folder)
        if not match:
            raise ValueError(
                f"Error: Improper notebook path '{the_notebook_path}'. Parent folder should be of the form 'part-X'."
            )
        part = int(match.group("part"))

        match = re.match(chapter_pattern, notebook_file)
        if not match:
            raise ValueError(f"Error: Improper notebook name '{notebook_file}'.")

        chapter = match.group("chapter")

        # Get the arguments provided
        args = self._parse_args(line, local_ns=local_ns)
        if not args:
            # Error message already printed out, so no need to do anything else
            return

        # Format the given arguments into the image path
        output_dir = f"{args.output_dir}/part-{part}/{chapter}"
        image_name = f"{args.name}.png"

        with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmpdir:
            # Form the manim command
            command = [f"%%manim"]
            command.append(f"--output_file={image_name}")
            command.append(f"--config_file={args.config_file}")

            if not args.show_splash:
                command.append("--hide-splash")

            if args.temp_dir:
                msg = f"Using user-defined temporary directory '{args.temp_dir}'"
                warnings.warn(msg)

                os.makedirs(args.temp_dir, exist_ok=True)
                tmpdir = args.temp_dir
            command.append(f"--media_dir={tmpdir}")

            command.append(args.scene_name)

            # Run cell with manim command
            cell = f"{' '.join(command)}\n{cell}"
            exec_result = self.shell.run_cell(cell)
            exec_result.raise_error()

            # Copy the image to the desired location
            os.makedirs(output_dir, exist_ok=True)
            shutil.copy(f"{tmpdir}/images/{notebook_parent_folder}/{image_name}", f"{output_dir}/{image_name}")
