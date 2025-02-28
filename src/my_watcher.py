import os
import shutil
import time
from datetime import datetime
import csv
import queue
import threading


def watcher():
    seen_files = set(os.listdir(path))
    try:
        while True:
            current_files = set(os.listdir(path))
            new_files = current_files - seen_files
            for file in sorted(new_files):
                print(file)
                appender(file)
            seen_files.update(new_files) 
    except KeyboardInterrupt:
        print("Stopping")



def appender(file_name):
    logger = 'logger.csv'
    current_time = datetime.now().strftime('%H:%M:%S')
    current_date = datetime.now().strftime('%d-%m-%Y')
    with open(logger, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_date,current_time, file_name])
    print(f"File created in PATH: {current_date}, {current_time}, {file_name}")


def csv_reader():
     with open('logger.csv', mode='r') as file:
        for lines in csv.reader(file):
            name = lines[2]
            for file in os.listdir(path):
                if os.path.exists(f'{new_path}/{file}'):
                    pass
                elif not os.path.exists(f'{new_path}/{file}'):
                    if file == name:
                        time.sleep(10)
                        shutil.copy(f'{path}/{file}', f'{new_path}/{file}')
                        print(f'Successfully copied {file} to NEW_PATH')
       



if __name__ == "__main__":
    path = f'{os.getcwd()}/PATH'
    new_path = f'{os.getcwd()}/NEW_PATH'

    watcher_thread = threading.Thread(target=watcher)
    watcher_thread.start()
    csv_thread = threading.Thread(target = csv_reader)
    csv_thread.start()

 
