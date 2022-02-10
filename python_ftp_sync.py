import os
import os.path
from datetime import datetime

with open("mtime.txt","r") as file:
    first_line = float(file.readline())
print(first_line)

source = "structura_foldere"
list = []

for path, subdirs, files in os.walk(source):
    for name in subdirs:
        dir = os.path.join(path, name)
        mtime = os.path.getmtime(dir)
        if(first_line < mtime):
            status = "OK"
        else:
            status = "to be updated"
            list.append(dir)
        print(dir, status)
    for name in files:
        file = os.path.join(path, name)
        mtime = os.path.getmtime(file)
        if(first_line < mtime):
            status = "OK"
        else:
            status = "to be updated"
            list.append(file)
        print(file, status)

print(list)

now = datetime.now()
current_time = now.strftime("%Y%m%d_%H%M%S")
print(current_time)
save_path = os.getcwd()+"\log"
log_file = (os.path.join(save_path, current_time))+".txt"
print(log_file)
outF = open(log_file, "w")

for line in list:
    outF.write(line)
    outF.write("\n")
outF.close()