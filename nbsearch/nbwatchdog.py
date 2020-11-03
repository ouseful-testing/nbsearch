#http://thepythoncorner.com/dev/how-to-create-a-watchdog-in-python-to-look-for-filesystem-changes/

from .nbsearch import update_notebook, remove_notebook, _NBSEARCH_DB_PATH
import time
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

db = _NBSEARCH_DB_PATH

def on_created(event):
    #print(f'created {event.src_path}')
    update_notebook(db, fn=event.src_path)

def on_deleted(event):
    #print(f'deleted {event.src_path}')
    remove_notebook(db, fn=event.src_path)

def on_modified(event):
    #print(f'modified {event.src_path}')
    update_notebook(db, fn=event.src_path, fts_update=True)

def on_moved(event):
    #print(f'moved {event.src_path}, {event.dest_path}')
    remove_notebook(db, fn=event.src_path)
    update_notebook(db, fn=event.dest_path, fts_update=True)

regexes = [r".*\.py", r".*\.ipynb", r".*\.Rmd", r".*\.md"]
ignore_regexes = [r".*[/\\]\..*"]

ignore_directories = False # Not sure I understand the semantics of this?
case_sensitive = True
event_handler = RegexMatchingEventHandler(regexes, ignore_regexes, ignore_directories, case_sensitive)
event_handler.on_created = on_created
event_handler.on_deleted = on_deleted
event_handler.on_modified = on_modified
event_handler.on_moved = on_moved

def dbmonitor(path='.'):
    """Monitor a path."""
    #print(f"Starting to monitor {path}")
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