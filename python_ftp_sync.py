import os

with open('mtime.txt',"r") as file:
    first_line = float(file.readline())
print(first_line)

source = 'structura_foldere'

for path, subdirs, files in os.walk(source):
    for name in subdirs:
        dir = os.path.join(path, name)
        mtime = os.path.getmtime(dir)
        if(first_line < mtime):
            status = "OK"
        else:
            status = "to be updated"
        print(dir, status)
    for name in files:
        file = os.path.join(path, name)
        mtime = os.path.getmtime(file)
        if(first_line < mtime):
            status = "OK"
        else:
            status = "to be updated"
        print(file, status)