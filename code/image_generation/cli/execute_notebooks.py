import os

import papermill as pm
from tqdm import tqdm


def execute_notebooks(*notebooks: str):
    """
    Execute a series of Jupyter notebooks containing Manim code.

    Args:
        notebooks: the names of the notebooks to execute.
    """

    # Save the current working directory
    cwd = os.getcwd()

    # Update the notebook paths to be absolute
    notebooks = [os.path.abspath(notebook) for notebook in notebooks]

    # Execute notebooks
    for notebook in tqdm(notebooks, desc="Executing notebooks"):
        os.environ["NOTEBOOK_PATH"] = notebook
        os.chdir(os.path.dirname(notebook))
        pm.execute_notebook(os.path.basename(notebook), None, progress_bar=True)

    # Reset the CWD back to original
    os.chdir(cwd)
