#http://thepythoncorner.com/dev/how-to-create-a-watchdog-in-python-to-look-for-filesystem-changes/

from .nbsearch import update_notebook, remove_notebook, _NBSEARCH_DB_PATH
from sqlite_utils import Database
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

db = Database(_NBSEARCH_DB_PATH)

def on_created(event):
    update_notebook(db, fn=event.src_path)

def on_deleted(event):
    remove_notebook(db, fn=event.src_path, uid=False)

def on_modified(event):
    update_notebook(db, fn=event.src_path)

def on_moved(event):
    remove_notebook(db, fn=event.src_path, uid=False)
    update_notebook(db, fn=event.dest_path)

patterns = ["*.py", "*.ipynb", "*.Rmd"]
ignore_patterns = r"*/\.*" #Does this ignore all hidden things?
ignore_directories = False # Not sure I understand the semantics of this?
case_sensitive = True
event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
event_handler.on_created = on_created
event_handler.on_deleted = on_deleted
event_handler.on_modified = on_modified
event_handler.on_moved = on_moved

def dbmonitor(path='.'):
    """Monitor a path."""
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    while True:
        observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            observer.stop()
    observer.join()