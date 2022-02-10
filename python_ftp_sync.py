import os
import os.path
from datetime import datetime

#fetching the last time tha ftp server was updated
with open("mtime.txt","r") as file:
    first_line = float(file.readline())
print(first_line)

#indicating the source folder
source = "structura_foldere"
#creating the list for the paths to the files and folders to be uploaded
list = []

#going trough the folder tree and scanning for files and forders to be updated
for path, subdirs, files in os.walk(source):
    for name in subdirs:
        dir = os.path.join(path, name)
        mtime = os.path.getmtime(dir)
        #comparing the last time a folder was modified with the last ftp upload time
        if(first_line < mtime):
            status = "OK"
        else:
            status = "to be updated"
            list.append(dir)
        print(dir, status)
    for name in files:
        file = os.path.join(path, name)
        mtime = os.path.getmtime(file)
        #comparing the last time the file was modified with the last ftp upload time
        if(first_line < mtime):
            status = "OK"
        else:
            status = "to be updated"
            list.append(file)
        print(file, status)

print(list)

#fetching current time to use it for the logfile name and for storring it into the mtime.txt file to be used for the next update cycle
now = datetime.now()
current_time = now.strftime("%Y%m%d_%H%M%S")
print(current_time)

#creating the log file
save_path = os.getcwd()+"\log"
log_file = (os.path.join(save_path, current_time))+".txt"
print(log_file)
outF = open(log_file, "w")
#writing to the log file
for line in list:
    outF.write(line)
    outF.write("\n")
outF.close()

