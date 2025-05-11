import os
import shutil
import time
from datetime import datetime
import csv
import threading
from pydrive2.drive import GoogleDrive 
from pydrive2.auth import GoogleAuth 
from oauth2client.service_account import ServiceAccountCredentials
import paramiko
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from PIL import Image
import io


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
    print(f'"{file_name}" created in PATH ({current_date}, {current_time})\n')

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
                                print(f'--> Copied "{file}" to NEW_PATH\n')
                                cloud(file)

                                image = Image.open(f'{new_path}/{file}')
                                title = os.path.basename(file)
                                tiff_plotter(image, title=title)
                                cloud(f'{png_path}/{title}_EDIT.png')
                

                                


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

    f.SetContentFile(file)

    f.Upload()
    print(f"----> Uploaded {name} to cloud.\n" )

def connect_to_sftp():

    # Edit these details if neccessary
    hostname ='xhpcfep.hpc.spring8.or.jp' 
    username = 'dkosimov'
    password = 'mUYquZc8'
    port = 22

    SSH_Client = paramiko.SSHClient()
    SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SSH_Client.connect(hostname=hostname,
                       port=port,
                       username=username,
                       password=password,
                       look_for_keys=False)

    sftp = SSH_Client.open_sftp()
    print("Connection successfully established ... ")
    return sftp

def copy_from_sftp(sftp, file):

    print("Fetching file ...")
    sftp.get(f'{tif_path}/{file}',f'{path}/{file}')
    print("Copy successful.")

def tiff_plotter(image, title, colormap=None):

    plt.imshow(image, cmap="plasma")
    plt.colorbar()
    plt.savefig(f'{png_path}/{title}_EDIT.png')
    print(f"Saved {title} to PNG_PATH\n")
    plt.close()




if __name__ == "__main__":

    # 'path' and 'new_path' are used temporarily
    # we monitor changes in 'path' and move data to 'new_path'
    path = f'{os.getcwd()}/PATH'
    new_path = f'{os.getcwd()}/NEW_PATH'
    png_path = f'{os.getcwd()}/PNG_PATH'

    # This is the directory where we upload our data at SACLA, edit if neccessary
    tif_path = '/work/kmiyanishi/userdata/2024b/woolsey2024b/difras'


    if True:
        watcher_thread = threading.Thread(target=watcher)
        watcher_thread.start()
        csv_thread = threading.Thread(target = csv_reader)
        csv_thread.start()

    if False: 
        cloud('1478724-02-shot.tif')
