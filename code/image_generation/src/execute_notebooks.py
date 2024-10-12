import papermill as pm
from tqdm import tqdm


def execute_notebooks(*notebooks: str):
    """
    Execute a series of Jupyter notebooks containing Manim code.

    Args:
        notebooks: the names of the notebooks to execute.
    """

    for notebook in tqdm(notebooks, desc="Executing notebooks"):
        pm.execute_notebook(notebook, None, progress_bar=True)
