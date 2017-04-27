#!/usr/bin/python3

import subprocess
import sys
import os.path

def path_transform(p):
    if p[:5] == "/mnt/":
        return p[5] + ":" + p[6:].replace("/","\\")
    else:
        return "%LocalAppData%\\lxss" + p.replace("/","\\")

class linux_app:
    def __init__(self,app_name,app_ext):
        self.app_name = app_name
        self.app_ext = list(app_ext)

suppress_stderr = True
linux_app_list = [linux_app("evince",[".pdf",".eps"]),]

if len(sys.argv) == 2:
    arg = sys.argv[1]
else:
    print("Specify a valid file name.")
    print("")
    print("open for BoW")
    print("(c) route16 2017")
    sys.exit()  

fullpath = subprocess.run(["realpath",arg],stdout=subprocess.PIPE)
fullpath_str = fullpath.stdout.decode("utf-8").split("\n")[0]
#print("fullpath_str =",path_transform(fullpath_str))

temp = subprocess.run(["ls","-dp",fullpath_str],stdout=subprocess.PIPE).stdout.decode("utf-8")
try:
    lastletter = temp[-2]
except IndexError:
    sys.exit()
if lastletter == "/":
    output = subprocess.run(["cmd.exe","/c","\"explorer.exe",path_transform(fullpath_str),"\""],
            stderr=subprocess.PIPE)
    #subprocess.run(["explorer.exe",path_transform(fullpath_str)],stderr=subprocess.PIPE)
    if not suppress_stderr:
        print(output.stderr)
else:
    root, ext = os.path.splitext(path_transform(fullpath_str))
    for app in linux_app_list:
        if ext in app.app_ext:
            output = subprocess.run([app.app_name, fullpath_str])
            break
    else:
        output = subprocess.Popen(["cmd.exe","/c","\"" + path_transform(fullpath_str) + "\""],
            stderr=subprocess.PIPE)
    if not suppress_stderr:
        print(output.stderr)
