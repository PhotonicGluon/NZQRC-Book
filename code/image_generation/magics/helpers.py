import json
import os
import re
from pathlib import Path
import warnings

import ipykernel
import requests
from jupyter_server.serverapp import list_running_servers
from requests.compat import urljoin


def get_notebook_path() -> Path:
    """
    Retrieves the file path of the currently executing Jupyter notebook.

    Returns:
        The absolute path to the currently executing notebook.

    Notes:
        Adapted from https://github.com/jupyter/notebook/issues/1000#issuecomment-359875246.
    """

    # Try and detect the kernel ID from the connection file
    kernel_match = re.search(r"kernel-(.*).json", ipykernel.connect.get_connection_file())
    if kernel_match is None:
        # We need to fall back on getting an environment variable
        warnings.warn("Can't detect kernel ID. Falling back on reading `NOTEBOOK_PATH` environment variable.")
        notebook_path = os.environ.get("NOTEBOOK_PATH", None)
        if notebook_path is None:
            raise ValueError("Can't detect notebook path. Please set `NOTEBOOK_PATH` environment variable.")

        return Path(notebook_path)

    kernel_id = kernel_match.group(1)

    # Find the server with the matching kernel ID
    servers = list_running_servers()
    for ss in servers:
        response = requests.get(urljoin(ss["url"], "api/sessions"), params={"token": ss.get("token", "")})
        for nn in json.loads(response.text):
            if nn["kernel"]["id"] == kernel_id:
                relative_path = nn["notebook"]["path"]
                return Path(ss["root_dir"], relative_path)
