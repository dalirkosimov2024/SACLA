import os
import shutil
import time
from datetime import datetime
import csv
import queue
import threading
from pydrive2.drive import GoogleDrive 
from pydrive2.auth import GoogleAuth 
from oauth2client.service_account import ServiceAccountCredentials


def watcher():
# monitors 'path' and appends any new files to 'logger.csv'

    seen_files = set(os.listdir(path))
    try:
        while True:
            current_files = set(os.listdir(path))
            new_files = current_files - seen_files
            for file in sorted(new_files):
                appender(file)
            seen_files.update(new_files) 
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopping...")

def appender(file_name):
# appends file_name to a csv file

    logger = 'logger.csv'
    current_time = datetime.now().strftime('%H:%M:%S')
    current_date = datetime.now().strftime('%d-%m-%Y')
    with open(logger, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_date,current_time, file_name])
    print(f"File created in PATH: {file_name} ({current_date}, {current_time})")


def csv_reader():
# reads the csv file, and copies the contents in order to 'new_path'

    try:
        while True:
             with open('logger.csv', mode='r') as file:
                for lines in csv.reader(file):
                    name = lines[2]
                    for file in os.listdir(path):
                        if os.path.exists(f'{new_path}/{file}'):
                            pass
                        elif not os.path.exists(f'{new_path}/{file}'):
                            if file == name:
                                time.sleep(8)
                                shutil.copy(f'{path}/{file}', f'{new_path}/{file}')
                                print(f'Successfully copied {file} to NEW_PATH')
                                cloud(file)
             time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")

def cloud(file):
# Uploads a file unto a google drive

    # Google drive API scope
    scope = ['https://www.googleapis.com/auth/drive.file']

    # Uploads the file unto a google drive -- this was specifically focused on the "TEST" folder
    gauth = GoogleAuth()
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'client_secrets.json' , scope
)
    drive = GoogleDrive(gauth)
    name = os.path.basename(file)

    f = drive.CreateFile({
        'title': name,
        'parents': [{'id' : '1yU-FGzhTI4O-1gwBoZuPa75XvyvujYs-'}]
    })

    f.Upload()
    print(f"Uploaded {file} to cloud." )
        
  

if __name__ == "__main__":
    path = f'{os.getcwd()}/PATH'
    new_path = f'{os.getcwd()}/NEW_PATH'

    if True:

        watcher_thread = threading.Thread(target=watcher)
        watcher_thread.start()
        csv_thread = threading.Thread(target = csv_reader)
        csv_thread.start()

  

    elif False:

        cloud(new_path)
        print("File uploaded to cloud")
