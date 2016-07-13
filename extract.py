#!/usr/bin/env python2
import glob
import os
import shutil
import subprocess
import sys

workdir = "tools/extcontents"
#################
version = "1.0"

print("- videoinject {}".format(version))


def pause_exit(code=1):
    raw_input("# press enter to exit...")
    sys.exit(code)


def runcommand(cmdargs):
    proc = subprocess.Popen(cmdargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.stdout.close()
    proc.stderr.close()
    proc.wait()
    if proc.returncode != 0:
        print("! {} had an error. ({})".format(cmdargs[0], proc.returncode))
        print(procoutput)


def mkdirs(d):
    try:
        os.makedirs(d)
    except OSError:
        if not os.path.isdir(d):
            raise

def rmdirs(d):
    try:
        shutil.rmtree(d)
    except OSError:
        if os.path.isdir(d):
            raise

plt = ""
if sys.platform == "linux2":
    plt = "linux_x86"
elif sys.platform == "win32" or sys.platform == "cygwin":
    plt = "windows_x86"
elif sys.platform == "darwin":
    plt = "osx"
else:
    print("! unknown platform? ({})".format(sys.platform))
    pause_exit()

cias = []
for f in glob.glob("*.cia"):
    cias.append(f)

cia = ""
if len(cias) == 0:
    print("! no CIAs are in this folder.")
    pause_exit()
elif len(cias) > 1:
    print("! there are multiple CIAs in this folder.")
    print("  pick one to extract: \n")
    for k, c in enumerate(cias):
        print("  {}: {}".format(k, c))

    inp = raw_input("# input number: ")
    try:
        cia = cias[int(inp)]
    except IndexError:
        print("! invalid option")
        pause_exit()
else:
    cia = cias[0]

print("- extracting {}".format(cia))

rmdirs(workdir)
mkdirs(workdir)

runcommand(["./tools/binaries/{}/ctrtool".format(plt), "--contents={}/contents".format(workdir), cia])
c = glob.glob("{}/contents.0000*".format(workdir))[0]
runcommand(["./tools/binaries/{}/ctrtool".format(plt), "--exefsdir={}/exefs".format(workdir), "--romfsdir={}/romfs".format(workdir), "--exheader={}/exheader.bin".format(workdir), c])
if os.path.isdir(workdir + "/romfs/movie"):
    for f in glob.glob(workdir + "/romfs/movie/*"):
        os.remove(f)
else:
    print("! romfs:/movie not found. is this actually a video CIA, or is it encrypted?")
    pause_exit()

print("* done extracting!")
pause_exit(0)
