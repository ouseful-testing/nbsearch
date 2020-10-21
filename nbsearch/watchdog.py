#http://thepythoncorner.com/dev/how-to-create-a-watchdog-in-python-to-look-for-filesystem-changes/

from nbsearch.nbsearch import update_notebook 

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def on_created(event):
    #event.src_path
    pass

def on_deleted(event):
    #event.src_path
    pass

def on_modified(event):
    #event.src_path
    pass

def on_moved(event):
   #event.src_path, event.dest_path
    pass

patterns = ["*.py", "*.ipynb", "*.Rmd"]
ignore_patterns = "*/\.*" #Does this ignore all hidden things?
ignore_directories = False # Not sure I understand the semantics of this?
case_sensitive = True
event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
event_handler.on_created = on_created
event_handler.on_deleted = on_deleted
event_handler.on_modified = on_modified
event_handler.on_moved = on_moved

path = "."

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