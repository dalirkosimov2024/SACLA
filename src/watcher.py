import time
import os
import paramiko

# Monitors 'path', anything that is added there is copied to 'new_path'


def watcher(sftp):

    source = sftp.listdir(tif_path)

    existing_files = set(source)
    print(f'Existing files: {existing_files}')
    try:
        while True:
            current_files = set(source)
            new_files = current_files - existing_files
            for file in new_files:
                copy_from_sftp(sftp, file)

            existing_files = current_files
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Stopping...")

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

    sftp = SSH_Client.open_sftp()
    print("Connection successfully established ... ")
    return sftp

def copy_from_sftp(sftp, file):

    file_name = file
    print("Fetching file ...")
    sftp_client.get(f'{tif_path}/{file_name}',f'{new_path}/{file_name}')
   


if __name__ == "__main__":

    tif_path = '/work/kmiyanishi/userdata/2024b/woolsey2024b/difras'
    new_path = f'{os.getcwd()}/NEW_PATH'
    path = f'{os.getcwd()}/PATH'


    sftp = connect_to_sftp()
    watcher(sftp)




   
