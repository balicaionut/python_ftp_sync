import os

with open('mtime.txt',"r") as file:
    first_line = file.readline()
print(first_line)

source = 'structura_foldere'

for path, subdirs, files in os.walk(source):
    for name in subdirs:
        dir = os.path.join(path, name)
        mtime = os.path.getmtime(dir)
        if(first_line < mtime):
            status = "ok"
        else:
            status = "to be uploaded"
        print(dir, status)
    for name in files:
        file = os.path.join(path, name)
        mtime = os.path.getmtime(file)
        print(file, mtime)