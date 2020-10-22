# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # `nbsearch`
#
# Simple sqlite/datasette powered full text search engine for notebooks.
# Based on: Simon Willison's ["Fast Autocomplete Search for Your Website"](https://24ways.org/2018/fast-autocomplete-search-for-your-website/).
#
# This file provides tools for creating and updating the database.

# %%
# #%pip install --upgrade sqlite_utils
# #%pip install --upgrade git+https://github.com/innovationOUtside/nb_quality_profile.git           
import nbformat
import sqlite3
import jupytext
import sqlite_utils
import os
import hashlib
import uuid
#from tqdm import tqdm
from nb_quality_profile import nb_visualiser as nbv
from pathlib import Path

_NBSEARCH_USER_PATH = os.path.join(str(Path.home()), ".nbsearch") 
# The indexing should really take place over directories the notebook server sees, but:
# - we can't reliably see JUPYTER_ROOT_DIRECTORY ?
# - we can't access c.NotebookApp.notebook_dir ?
_NB_SEARCH_PATH = os.path.join(str(Path.home()))
_NBSEARCH_DB_FILE = "notebooks.sqlite"
_NBSEARCH_DB_PATH =  os.path.join(_NBSEARCH_USER_PATH, _NBSEARCH_DB_FILE)
_FILES_TABLE = "nbfiles"
_CONTENTS_TABLE = "nbcontents"

if not os.path.exists(_NBSEARCH_USER_PATH):
    os.makedirs(_NBSEARCH_USER_PATH)

def nbpathwalk(path, filetypes=None):
    ''' Walk down a directory path looking for ipynb notebook files… '''
    for path, _, files in os.walk(path):
        # Omit hidden directories
        if '/.' in path:
            continue
        # TO DO — allow other file types
        # that can be parsed with Jupytext
        if filetypes is None:
            filetypes = ('.ipynb')
        for f in [i for i in files if i.endswith(tuple(filetypes))]:
            yield os.path.join(path, f)

def get_nb(fn, text_formats=False):
    """Get notebook contents."""
    
    fmts = ['.ipynb']
    if text_formats:
        fmts = fmts + ['.md', '.Rmd', '.py']
    _fn, fn_ext = os.path.splitext(fn)

    if fn_ext not in fmts or not os.path.isfile(fn):
        # Better to return this as empty and check downstream?
        return {}

    if fn_ext=='.ipynb':
        with open(fn, 'r') as f:
            try:
                nb = nbformat.reads(f.read(), nbformat.NO_CONVERT)
            except:
                print(f"Couldn't process {fn}")
                return {}
    else:
        try:
            nb = jupytext.read(fn)
        except:
            print(f"Couldn't process {fn}")
            return {}
    return nb
    
def get_cell_contents(nb, cell_typ=None):
    ''' Extract the content of Jupyter notebook cells. '''
    
    if not nb or "cells" not in nb:
        return []

    if cell_typ is None:
        cell_typ = ['markdown', 'code', 'raw']
    
    cells = [i for i in nb.cells if i['cell_type'] in cell_typ]

    return cells


def index_notebook(nbid, nb, cell_typ=None, text_formats=False):
    """ Parse individual notebook."""
    
    docs = []
    cells = get_cell_contents(nb, cell_typ=cell_typ)
    cnt = {'all':0, 'md':0, 'code':0, 'raw':0}

    # TO DO - the plotter should have: plt.ioff() ?
    # Currently raising: ApplePersistenceIgnoreState: Existing state will not be touched.
    img = nbv.nb_vis_parse_nb(raw=nb, minimal=True, retval='img') if nb else None
    
    for cell in cells:
        
        if cell['cell_type'] in cnt:
            cnt[cell['cell_type']] += 1
            cell['cell_type_num'] = cnt[cell['cell_type']]
        else:
            cell['cell_type_num'] = 0
        cell['tags'] = cell['metadata']['tags'] if 'tags' in cell['metadata'] else ''
        cell['nbid'] = nbid
        cell['cell_num'] = cnt['all']
        
        cnt['all'] += 1
        docs.append({k: cell[k] for k in ('nbid', 'source', 'cell_type',
                                          'tags', 'cell_num', 'cell_type_num')})
    
    return docs, cnt, img


def create_tables(db, files_table=_FILES_TABLE, contents_table=_CONTENTS_TABLE):
    """Create database tables."""
    if files_table not in db.table_names():
        db[files_table].create({"nbid": str, "last_modified": int, 'cells': int,
                                "md_cells": int, "code_cells": int,
                                "name": str, "file_type": str,
                                "img": "BLOB"}, pk="nbid")

    if contents_table not in db.table_names():
        db[contents_table].create({"nbid": str, "tags": str,
                                   "source": str, "cell_type": str, "cell_num": int,
                                   "cell_type_num": int},
                                   pk=("nbid", "cell_num"),
                                   foreign_keys=[ ("nbid", files_table, "nbid")])


def create_init_db(dbpath=_NBSEARCH_DB_PATH, clear=False):
    """Create and initialise database."""
    if clear and os.path.exists(dbpath):
        os.remove(dbpath)
    db = sqlite_utils.Database(dbpath)
    create_tables(db)


def remove_notebook(db, nbid=None, fn=None,
                    files_table=_FILES_TABLE, contents_table=_CONTENTS_TABLE):
    """Remove a notebook from the database."""
    # TO DO - do we also have to monitor this from file system? eg file deletions?
    # https://github.com/gorakhargosh/watchdog/ could be handy?
    # And s/thing like: nohup python /path/to/watchdog.py &
    nbid = get_nbid(nbid, fn, uid=False)
    db[contents_table].delete_where(f"nbid = '{nbid}'")
    db[files_table].delete_where(f"nbid = '{nbid}'")
    
def get_nbid(nbid=None, fn=None, uid=True):
    """Create notebook id."""
    # Create a uid, ideally based on the notebook name if not already provided
    if ((not nbid) and fn):
        nbid = hashlib.md5(fn.encode()).hexdigest()
    elif uid:
        nbid = str(uuid.uuid4())
    return nbid


def update_notebook(db, nbid=None, fn=None, nbcontent=None, 
                    files_table=_FILES_TABLE, contents_table=_CONTENTS_TABLE,
                    cell_typ=None, text_formats=None):
    """Update items relating to a notebook."""
    if not nbid and not fn and not nbcontent:
        return

    nbid = get_nbid(nbid, fn)

    remove_notebook(db, nbid, files_table, contents_table)
                    
    nb = nbcontent if nbcontent else get_nb(fn, text_formats=text_formats)
    if not nb:
        return
    docs, cnt, img = index_notebook(nbid, nb, cell_typ=cell_typ)
    db[contents_table].upsert_all(docs, pk=("nbid", "cell_num"))
    _fn, fn_ext = os.path.splitext(fn)
    f_details = {"nbid": nbid, "last_modified": os.path.getmtime(fn),
                 "cells": cnt['all'],
                 "md_cells": cnt['md'], "code_cells": cnt['code'],
                 "name": fn, "file_type": fn_ext,
                 "img": img}
    db[files_table].upsert(f_details, pk="nbid")


# TO DO - at the moment, if we delete a notebook
# it still exists in the search database
def index_notebooks_sqlite(nbpath='.', dbpath=_NBSEARCH_DB_PATH, cell_typ=None,
                           files_table=_FILES_TABLE,
                           contents_table=_CONTENTS_TABLE,
                           text_formats=None):
    ''' Get content from each notebook down a path and index it. '''
    
    db = sqlite_utils.Database(dbpath)
    create_tables(db, files_table, contents_table)
    for fn in nbpathwalk(nbpath):
        update_notebook(db, fn=fn, cell_typ=cell_typ, text_formats=text_formats)
    
    if not db[contents_table].detect_fts():
        db[contents_table].enable_fts(["source"])
    else:
        db[contents_table].populate_fts(["source"])
        
    # TO DO
    # Notebook should update record in db whe notebook saves
    # nbautoexport has a way of updating c.FileContentsManager.post_save_hook
    # in a way that does not break previously added hooks
    # (Is there no native safe Jupyter way of doing this? What does Jupytext do?)
    # https://github.com/drivendataorg/nbautoexport/blob/master/nbautoexport/jupyter_config.py

# %% tags=["active-ipynb"]
# #!rm notebooks.sqlite
# create_init_db(clear=True)

# %% tags=["active-ipynb"]
# path = '/Users/tonyhirst/Documents/GitHub/tm129-robotics2020/content/01. Introducing notebooks and the RoboLab environment'
# os.listdir(path)

# %% tags=["active-ipynb"]
# #index_notebooks_sqlite('01. Introducing notebooks and the RoboLab environment')
# index_notebooks_sqlite(path)

# %% tags=["active-ipynb"]
# db = sqlite_utils.Database('notebooks.sqlite')
# #list(db['nbcontents_fts'].rows)

# %%
# TO DO - make jupyter-server-proxy
# TO DO - make update index button
# TO DO - make updates only index changed things
# TO DO - delete items not in index and more


# %% tags=["active-ipynb"]
# #jupyter_notebook_config.py
# # Derived from: https://jupyter-notebook.readthedocs.io/en/stable/extending/savehooks.html
# import os
# from nbsearch.nbsearch import update_notebook
#
# _script_exporter = None
#
# def db_post_save(model, os_path, contents_manager, **kwargs):
#     """Update nbsearch db."""
#     from nbconvert.exporters.script import ScriptExporter
#
#     if model['type'] != 'notebook':
#         return
#
#     # Useful? contents_manager.root_dir
#
#     update_notebook(db, nbid=None, fn=os_path, nbcontent=model['content'])
#
# c.FileContentsManager.post_save_hook = db_post_save
