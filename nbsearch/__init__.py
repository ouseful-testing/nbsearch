import os
import subprocess
import pkg_resources
from .nbsearch import _NBSEARCH_DB_PATH, create_init_db
import subprocess
from datasette import hookimpl

__version__="0.0.3"


@hookimpl
def extra_css_urls(database, table, columns, view_name, datasette):
    return [
        "https://cdnjs.cloudflare.com/ajax/libs/prism/1.22.0/themes/prism.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/prism/1.22.0/plugins/line-numbers/prism-line-numbers.min.css",
        #"/-/static-plugins/nbsearch/nbsearch.css",
    ]


@hookimpl
def extra_js_urls(database, table, columns, view_name, datasette):
    return [
        "https://cdn.jsdelivr.net/npm/prismjs@1.22.0/prism.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/prism/1.22.0/plugins/line-numbers/prism-line-numbers.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/prism/1.22.0/components/prism-python.min.js",
        "https://cdn.jsdelivr.net/npm/marked/marked.min.js",
        "https://cdn.jsdelivr.net/npm/clipboard@2.0.6/dist/clipboard.min.js",
    ]

def setup_nbsearch():
    # Spawn a process somewhere to initialise the indexing
    #subprocess.run(["nbsearch", "index"])
    # Make sure tables are created
    create_init_db()
    subprocess.run(["nbsearch", "index"])

    fpath = pkg_resources.resource_filename('nbsearch', '/static/')
    return {
        "command": [
            "datasette",
            "serve",
            f"{_NBSEARCH_DB_PATH}",
            #f"--template-dir={fpath}templates/",
            #"--metadata",
            #f"{fpath}metadata/metadata.json",
            #"--static",
            #f"static:{fpath}static/",
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
