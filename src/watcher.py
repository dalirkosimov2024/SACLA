import sys
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import logging
import shutil
import os
import paramiko
from PIL import Image
from io import BytesIO
import numpy as np

# Monitors 'path', anything that is added there is copied to 'new_path'
def on_modified(event):

    new_path = f'{os.getcwd()}/NEW_PATH'
    for file_name in os.listdir(path):
        source = f'{path}/{file_name}'
        sink = f'{new_path}/{file_name}'
        
        if os.path.isfile(source):
            shutil.copy(source, sink)
            print(f"Copied {file_name}")

def watcher():
    print("Operation: watcher")

    # log the changes in terminal, save changes to dev.log file
    logging.basicConfig(filename = 'dev.log', filemode = 'a',
                        level=logging.INFO, 
                        format = '%(asctime)s -%(process)d - %(message)s',
                        datefmt = '%Y - %m - %d %H:%M:%S')


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

def connect_to_sftp():

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

    sftp_client = SSH_Client.open_sftp()
    print("Connection successfully established ... ")
    return sftp_client

def copy_from_sftp(sftp_client):


    tif_path = '/work/kmiyanishi/userdata/2024b/woolsey2024b/difras'
    new_path = f'{os.getcwd()}/NEW_PATH'

    file_name = '1479042_kame.tif'
    print("Fetching file ...")

    try:
      sftp_client.get(f'{tif_path}/{file_name}',f'{new_path}/{file_name}')
      print("File succesfully downloaded.")
    except FileNotFoundError as err:
      print(f"File: {file_name} was not found on the SFTP server")


       




if __name__ == "__main__":

    path = f'{os.getcwd()}/PATH'
    operation = 'stfp'

    if operation == 'watcher':

        print("Operation: watcher")
        watcher()

    elif operation == 'sftp':
        
        print("Operation: SFTP")
        sftp_client = connect_to_sftp()
        copy_from_sftp(sftp_client)

   
