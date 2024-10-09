import os

from IPython.display import clear_output
from IPython.core.magic import Magics, magics_class, cell_magic


@magics_class
class ProperDisplayMagic(Magics):
    """
    Properly handle the toggling of Manim-generated frames within notebooks.
    """

    @cell_magic
    def handle_display(self, line: str, cell: str):
        # Try and get a defined `DISPLAY` constant
        should_display = os.getenv("MANIM_DISPLAY", "TRUE").upper() == "TRUE"

        # Run original cell
        exec_result = self.shell.run_cell(cell)

        # If should not display, clear the display
        if not should_display:
            clear_output()
            exec_result.raise_error()  # But if there was an error, make sure that the user sees it
            clear_output(wait=True)


def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension` can be loaded via
        %load_ext module.path
    or be configured to be autoloaded by IPython at startup time.
    """

    ipython.register_magics(ProperDisplayMagic)
    print("Loaded toggle display extension.")
