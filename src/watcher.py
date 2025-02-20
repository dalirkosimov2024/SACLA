import sys
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import logging

if __name__ == "__main__":

    # log the changes in terminal
    logging.basicConfig(level=logging.INFO, 
                        format = '%(asctime)s -%(process)d - %(message)s',
                        datefmt = '%Y - %m - %d %H:%M:%S')

    path = sys.argv[1] if len(sys.argv)>1 else '.'

    # watch for changes in path
    watcher = Observer()
    handler = LoggingEventHandler()
    watcher.schedule(handler, path, recursive = True)
    watcher.start()

    # stop script if I use keyboard
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        watcher.stop()
        watcher.join()
   
