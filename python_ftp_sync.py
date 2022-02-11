import os
import os.path
from datetime import datetime
import time
from ftplib import FTP


def last_update_time():
    timestamp = int(time.time())
    f = open("mtime.txt", "r+")
    f.truncate(0)
    f.write(str(timestamp))
    f.close()
last_update_time()




#def ftp_login()
#list to store credentials
ftp_cred = []
#reading from credentials file and assigning to list
with open("login_data.txt") as f:
    lines = f.readlines()
count = 0
for line in lines:
    count += 1
    ftp_cred.append(line)

#assigning credentials from list to credential variables
server = ftp_cred[0].strip()
user = ftp_cred[1].strip()
password = ftp_cred[2].strip()

#login to ftp server
ftp = FTP(server)
ftp.login(user = user, passwd = password)

# ftp.cwd("structura_foldere")

#fetching the last time tha ftp server was updated
with open("mtime.txt","r") as file:
    first_line = float(file.readline())
print(first_line)

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
        if(first_line > mtime):
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
        if(first_line > mtime):
            status = "OK"
        else:
            status = "to be updated"
            list_file.append(file)
        print(file, status)

print(len(list_dir))
print(list_dir)
print(list_file)

#fetching current time to use it for the logfile name and for storring it into the mtime.txt file to be used for the next update cycle
now = datetime.now()
current_time = now.strftime("%Y%m%d_%H%M%S")
print(now)
print(current_time)


#creating the log file
list_all = list_dir + list_file
save_path = os.getcwd()+"\log"
log_file = (os.path.join(save_path, current_time))+".txt"
print(log_file)
outF = open(log_file, "w")
#writing to the log file
for line in list_all:
    outF.write(line)
    outF.write("\n")
outF.close()


print(".....")


# TODO - create logic to write to FTP

# def placeFile(filename, localpath):
#     ftp.storbinary('STOR '+filename, open(localpath, 'rb'))
# placeFile()


# for path, subdirs, files in os.walk(source):
#     index=0
#     for name in subdirs:
#         dir = os.path.join(path, name)
#         mtime = os.path.getmtime(dir)
#         index = index+1
#         ftp.cwd(name)
#         if(first_line < mtime):
#             # ftp.mkd(name)
#             # ftp.retrlines('LIST')
#             print(name)
#     ftp.cwd("..")
#     print(index)
#     # ftp.cwd(name)
#     ftp.retrlines('LIST')


# create folders on ftp servers
i = 0
while i < len(list_dir):
    update_list = list_dir[i].split("\\")
    for name in update_list:
        print(name)
        print(i)
        try:
            ftp.mkd(name)
        except:
            print("Directory already exists")
        ftp.cwd(name)
    j = 0
    while j < len(update_list):
        ftp.cwd("..")
        j += 1
    j = 0
    i += 1


print(".....")


i = 0
while i < len(list_file):
    update_list = list_file[i].split("\\")
    for name in update_list:
        if name != update_list[(len(update_list)-1)]:
            print("fwd")
            ftp.cwd(name)
        if name == update_list[(len(update_list)-1)]:
            print(name)
            print(list_file[i])
            ftp.retrlines('LIST')
            try:
                print(name)
                print(list_file[i])
                with open(list_file[i], 'br') as my_file: ftp.storbinary('STOR ' + name, my_file)
            except:
                print(name)
                print(list_file[i])
                ftp.delete(name)
            else:
                print(name)
                print(list_file[i])
                with open(list_file[i], 'br') as my_file: ftp.storbinary('STOR ' + name, my_file)     
    j = 0
    while j < (len(update_list)-1):
        print("back")
        ftp.cwd("..")
        j += 1
    j = 0
    i += 1
    ftp.retrlines('LIST')
    print(i)


# print(list_dir[0])
# update_list = list_dir[0].split("\\")

#print(update_list)


print(".....")


#ftp.mkd("structura_foldere\\abc")
#ftp.cwd("structura_foldere")

# ftp.cwd("/")
ftp.retrlines('LIST')

ftp.quit()

