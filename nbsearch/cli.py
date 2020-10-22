import click
import subprocess
import pkg_resources
from .nbsearch import index_notebooks_sqlite
from .nbsearch import _NBSEARCH_DB_PATH, _NB_SEARCH_PATH
from .nbwatchdog import monitor

@click.group()
def cli():
	pass

@cli.command()
@click.option('path', '-p', default='.', type=click.Path(exists=True))
def index(path):
    """Index path."""
    click.echo('Indexing file/directory: {}'.format(path))
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
            f"--template-dir={fpath}templates/",
            "--metadata",
            f"{fpath}metadata/metadata.json",
            "--static",
            f"static:{fpath}static/",
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
    monitor(searchpath)
    # nohup python nbsearch monitor &



