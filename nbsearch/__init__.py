import os
import subprocess
import pkg_resources
from .nbsearch import _NBSEARCH_DB_PATH, create_tables

# Make sure tables are created
create_tables()

def setup_nbsearch():
    # Spawn a process somewhere to initialise the indexing
    #subprocess.run(["nbsearch", "index"])

    fpath = pkg_resources.resource_filename('nbsearch', '/static/')
    return {
        "command": [
            "datasette",
            "serve",
            f"{_NBSEARCH_DB_PATH}",
            f"--template-dir={fpath}templates/",
            "--metadata",
            f"{fpath}metadata/metadata.json",
            "--static",
            f"static:{fpath}static/",
            "-p",
            "{port}",
            "--config",
            "base_url:{base_url}nbsearch/"
        ],
        "absolute_url": True,
        # The following needs a the labextension installing.
        # eg in postBuild: jupyter labextension install jupyterlab-server-proxy
        "launcher_entry": {
            "enabled": True,
            #'icon_path': f'{fpath}/icons/nbsearch.svg',
            "title": "nbsearch",
        },
    }
