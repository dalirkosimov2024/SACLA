import sys
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import logging
import shutil
import os

# Monitors 'path', anything that is added there is copied to 'new_path'
def on_modified(event):
    new_path = f'{os.getcwd()}/NEW_PATH'
    for file_name in os.listdir(path):
        source = f'{path}/{file_name}'
        sink = f'{new_path}/{file_name}'
        
        if os.path.isfile(source):
            shutil.copy(source, sink)
            print(f"Copied {file_name}")


if __name__ == "__main__":

    # log the changes in terminal, save changes to dev.log file
    logging.basicConfig(filename = 'dev.log', filemode = 'a',
                        level=logging.INFO, 
                        format = '%(asctime)s -%(process)d - %(message)s',
                        datefmt = '%Y - %m - %d %H:%M:%S')

    path = sys.argv[1] if len(sys.argv)>1 else '.'

    # watch for changes in path
    watcher = Observer()
    handler = LoggingEventHandler()
    handler.on_modified = on_modified
    watcher.schedule(handler, path, recursive = True)
    watcher.start()

    # stop script if I use keyboard
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        watcher.stop()
        watcher.join()
   
