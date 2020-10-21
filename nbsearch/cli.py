import click
import subprocess
import pkg_resources
from .nbsearch import index_notebooks_sqlite

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
@click.option('dbpath', '-p', default='notebooks.sqlite', type=click.Path(exists=True))
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
            #"-p",
            #"{port}",
            #"--config",
            #"base_url:{base_url}nbsearch/",
            #"-d",
            #os.environ["HOME"]
        ]
   
    subprocess.Popen(command)   