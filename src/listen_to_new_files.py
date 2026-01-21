import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class NewFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.new_file = None

    def on_created(self, event):
        if not event.is_directory:
            print(f"New report file: {event.src_path}")
            self.new_file = event.src_path
        
def receive_new_report(path_to_reports, shutdown):
    if not os.path.exists(path_to_reports):
        print(f"Reports directory not found: {path_to_reports}")
        return None

    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_reports, recursive=False)
    observer.start()

    try:
        while not shutdown.is_set():
            if event_handler.new_file:
                result = event_handler.new_file
                #reset for next file
                event_handler.new_file = None  
                return result
            time.sleep(0.5) 
    finally:
        observer.stop()
        observer.join()
    
    return None
