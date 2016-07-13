#!/usr/bin/env python2
import errno
import os
import random
import shutil
import subprocess
import sys

uid_blacklist = {  # list of unique IDs that will never be randomly picked
    0xc0d00,
    0xce1cc,
    0xd921e,
    0xda001,
    0xda002,
    0xda003,
    0xe7a5a,
    0xec100,
    0xed990,
    0xeffec,
    0xeffed
}

workdir = "tools/extcontents"
tmpdir = "tools/tmpdir"
#################
version = "1.0"

print("- videoinject {}".format(version))

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


def pause_exit(code=1):
    raw_input("# press enter to exit...")
    sys.exit(code)


def runcommand(cmdargs):
    proc = subprocess.Popen(cmdargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.wait()
    procoutput = proc.communicate()[0]
    if proc.returncode != 0:
        print("! {} had an error. ({})".format(cmdargs[0], proc.returncode))
        print("- full command: {}".format(" ".join(cmdargs)))
        print("- output:")
        print(procoutput)


def gencsv(title):
    base = list("#JP,#EN,#FR,#GE,#IT,#SP,#CH,#KO,#DU,#PO,#RU,#TW\r\n{}".format((title + ",") * 12)[:-1])
    result = "\xFF\xFE"
    for c in base:
        result += c + '\0'
    return result


def randn():
    n = random.randint(0xc0000, 0xeffff)
    if n in uid_blacklist:
        n = randn()
    return n


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


# taken from http://stackoverflow.com/questions/6159313/can-python-test-the-membership-of-multiple-values-in-a-list
# because i'm lazy :p
def all_in(candidates, sequence):
    for element in candidates:
        if element not in sequence:
            return False
    return True


# used from http://stackoverflow.com/questions/10840533/most-pythonic-way-to-delete-a-file-which-may-not-exist
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

mkdirs("output")
for root, dirs, files in os.walk("input"):
    for name in dirs:
        ifiles = os.listdir(os.path.join(root, name))
        if not all_in(["icon.png", "banner.png", "movie.moflex"], ifiles):
            print("! some files are missing from {}.".format(name))
            print("  make sure there is a movie.moflex, banner.png, and icon.png.")
            continue
        uid = randn()
        print("- injecting \"{0} [{1}]\"".format(name, format(uid, 'X')))
        rmdirs(tmpdir)
        mkdirs(tmpdir)
        runcommand(["./tools/binaries/{}/bannertool".format(plt), "makesmdh", "-i", os.path.join(root, name, "icon.png"), "-s", name, "-l", name, "-p", "Video", "-f", "visible,nosavebackups", "-o", tmpdir + "/icon.bin"])
        bannersnd = "tools/banner_def.wav"
        if "banner.wav" in ifiles:
            bannersnd = os.path.join(root, name, "banner.wav")
        runcommand(["./tools/binaries/{}/bannertool".format(plt), "makebanner", "-i", os.path.join(root, name, "banner.png"), "-a", bannersnd, "-o", tmpdir + "/banner.bin"])
        silentremove(workdir + "/romfs/movie/movie.moflex")
        shutil.copyfile(os.path.join(root, name, "movie.moflex"), workdir + "/romfs/movie/movie.moflex")
        with open(workdir + "/romfs/movie/movie_title.csv", "wb") as c:
            c.write(gencsv(name))
        os.chdir(workdir)
        runcommand(["../binaries/{}/makerom".format(plt), "-f", "cia", "-o", "../../output/{0} [{1}].cia".format(name, format(uid, 'X')), "-banner", "../tmpdir/banner.bin", "-icon", "../tmpdir/icon.bin", "-code", "exefs/code.bin", "-exheader", "exheader.bin", "-rsf", "../template.rsf", "-DAPP_UNIQUE_ID={}".format(uid)])
        os.chdir("../..")

print("* done injecting!")
pause_exit(0)
