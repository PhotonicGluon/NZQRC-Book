import json
import re
from pathlib import Path

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

    kernel_id = re.search(r"kernel-(.*).json", ipykernel.connect.get_connection_file()).group(1)
    servers = list_running_servers()

    for ss in servers:
        response = requests.get(urljoin(ss["url"], "api/sessions"), params={"token": ss.get("token", "")})
        for nn in json.loads(response.text):
            if nn["kernel"]["id"] == kernel_id:
                relative_path = nn["notebook"]["path"]
                return Path(ss["root_dir"], relative_path)
