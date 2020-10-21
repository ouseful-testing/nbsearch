import os
import pkg_resources

def setup_nbsearch():
    fpath = pkg_resources.resource_filename('nbsearch', '/static/')
    return {
        "command": [
            "datasette",
            "serve",
            "notebooks.sqlite",
            f"--template-dir={fpath}templates/",
            "--metadata",
            f"{fpath}metadata/metadata.json",
            "--static",
            f"static:{fpath}static/",
            "-p",
            "{port}",
            "--config",
            "base_url:{base_url}nbsearch/",
            "-d",
            os.environ["HOME"]
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
