import patoolib
import subprocess
import os
import shutil
import sys

filename = 'update.zip'
dirname = 'update'

os.mkdir(dirname)
patoolib.extract_archive(filename, outdir=dirname)

files = [el for el in os.listdir(dirname) if os.path.isfile(el)]

for el in os.listdir(dirname):
    el = os.path.join(dirname, el)
    if os.path.isdir(el):
        files += [os.path.join(el, i) for i in os.listdir(el)]

for f in files:
    os.replace(os.path.join(dirname, f), f)

shutil.rmtree(dirname)

if not sys.platform.startswith("linux"):
    theproc = subprocess.Popen('main.exe')
else:
    theproc = subprocess.Popen('python3 main.py &', shell=True)
theproc.communicate()
