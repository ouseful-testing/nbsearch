import click
import subprocess
import pkg_resources
from .nbsearch import index_notebooks_sqlite
from .nbsearch import _NBSEARCH_DB_PATH, _NB_SEARCH_PATH
from .nbwatchdog import dbmonitor
import os
from nbsearch.nbsearch import create_init_db
from nbsearch.nbsearch import _NBSEARCH_USER_PATH, _NBSEARCH_DB_PATH

@click.group()
def cli():
	pass

@cli.command()
def create():
    """Create inital empty db."""
    create_init_db(_NBSEARCH_DB_PATH)


@cli.command()
@click.option('path', '-p', default='.', type=click.Path(exists=True))
def index(path):
    """Index path."""
    click.echo('Indexing file/directory: {}'.format(path))
    # Create some useful paths
    if not os.path.exists(_NBSEARCH_USER_PATH):
        os.makedirs(_NBSEARCH_USER_PATH)
    # Would be useful to export these as persistent environment variables?
    create_init_db(_NBSEARCH_DB_PATH)
    index_notebooks_sqlite(path)

@cli.command()
@click.option('dbpath', '-p', default=_NBSEARCH_DB_PATH, type=click.Path(exists=True))
def serve(dbpath):
    """Run server path."""
    fpath = pkg_resources.resource_filename('nbsearch', '/static/') #static/
    command =  [
            "datasette",
            "serve",
            dbpath,
            #f"--template-dir={fpath}templates/",
            #"--metadata",
            #f"{fpath}metadata/metadata.json",
            #"--static",
            #f"static:{fpath}static/",
            "-p",
            "0", # pick a port for me...
            #"--config",
            #"base_url:{base_url}nbsearch/",
            #"-d",
            #os.environ["HOME"]
        ]
   
    subprocess.Popen(command)

# Not tested
@cli.command()
@click.option('searchpath', '-s', default=_NB_SEARCH_PATH, type=click.Path(exists=True))
def monitor(searchpath):
    """Monitor notebook path."""
    dbmonitor(searchpath)
    # nohup python nbsearch monitor &



