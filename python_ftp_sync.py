import os
import os.path
from datetime import datetime
import time
from ftplib import FTP


# reading from credentials file and assigning to list
def ftp_cred():
    ftp_cred_list = []
    with open("login_data.txt") as f:
        lines = f.readlines()
    count = 0
    for line in lines:
        count += 1
        ftp_cred_list.append(line)
    server = ftp_cred_list[0].strip()
    user = ftp_cred_list[1].strip()
    password = ftp_cred_list[2].strip()
    return server, user, password


# function to login into server
def ftp_login():
    # login to ftp server
    ftp = FTP(ftp_cred()[0])
    ftp.login(user = ftp_cred()[1], passwd = ftp_cred()[2])
    print("FTP server connected")
    return ftp


# function to logout from server
def ftp_logout():
    # logout of ftp server
    ftp = ftp_login()
    ftp.quit()
    print("FTP server disconnected")


#fetching the last time the ftp server was updated
def last_time():
    with open("mtime.txt","r") as file:
        first_line = float(file.readline())
    return first_line


def list_dir_and_file():
    #indicating the source folder
    source = "structura_foldere"
    #creating the list for the paths to the files and folders to be uploaded
    list_dir = []
    list_file = []
    #going trough the folder tree and scanning for files and forders to be updated
    for path, subdirs, files in os.walk(source):
        for name in subdirs:
            dir = os.path.join(path, name)
            mtime = os.path.getmtime(dir)
            #comparing the last time a folder was modified with the last ftp upload time
            if(last_time() > mtime):
                status = "OK"
            else:
                status = "to be updated"
                list_dir.append(dir)
                #ftp.mkd(name)
                #print(name)

            print(dir, status)
        for name in files:
            file = os.path.join(path, name)
            mtime = os.path.getmtime(file)
            #comparing the last time the file was modified with the last ftp upload time
            if(last_time() > mtime):
                status = "OK"
            else:
                status = "to be updated"
                list_file.append(file)
            print(file, status)
    list_all = list_dir + list_file
    return list_dir, list_file, list_all


#fetching current time to use it for the logfile name
def time_name():
    now = datetime.now()
    current_time = now.strftime("%Y%m%d_%H%M%S")
    return current_time


#creating the log file
def create_log_file():
    list_all = list_dir_and_file()[2]
    save_path = os.getcwd()+"\log"
    log_file = (os.path.join(save_path, time_name()))+".txt"
    outF = open(log_file, "w")
    #writing to the log file
    if (len(list_all)) == 0:
        outF.write("no files and folders to update")
    else:
        for line in list_all:
            outF.write(line)
            outF.write("\n")
    outF.close()
    print(log_file + " log file has been created")


# create folders on ftp servers
def update_folders():
    list_dir = list_dir_and_file()[0]
    if len(list_dir) == 0:
        print("no new folders to create on server")
    else:
        ftp = ftp_login()
        i = 0
        while i < len(list_dir):
            update_list = list_dir[i].split("\\")
            for name in update_list:
                try:
                    ftp.mkd(name)
                except:
                    print("updating...")
                ftp.cwd(name)
            j = 0
            while j < len(update_list):
                ftp.cwd("..")
                j += 1
            j = 0
            i += 1

def update_files():
    list_file = list_dir_and_file()[1]
    if len(list_file) == 0:
        print("no files to update to server")
    else:
        ftp = ftp_login()
        i = 0
        while i < len(list_file):
            update_list = list_file[i].split("\\")
            for name in update_list:
                if name != update_list[(len(update_list)-1)]:
                    ftp.cwd(name)
                if name == update_list[(len(update_list)-1)]:
                    try:
                        with open(list_file[i], 'br') as my_file: ftp.storbinary('STOR ' + name, my_file)
                    except:
                        ftp.delete(name)
                    else:
                        with open(list_file[i], 'br') as my_file: ftp.storbinary('STOR ' + name, my_file)     
            j = 0
            while j < (len(update_list)-1):
                ftp.cwd("..")
                j += 1
            j = 0
            i += 1


# function to update time to storred last update time file "mtime.txt"
def update_time():
    timestamp = int(time.time())
    f = open("mtime.txt", "r+")
    f.truncate(0)
    f.write(str(timestamp))
    f.close()


def main():
    last_time()
    ftp_login()
    list_dir_and_file()
    create_log_file()
    update_folders()
    update_files()
    ftp_logout()  
    update_time()  

if __name__ == "__main__":
    main()