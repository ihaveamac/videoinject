videoinject 1.0 ~ moflex video injection

Since we apparently can create our own moflex videos now, I made this
thing because I didn't like the existing methods.

videoinject.exe and extract.exe can be used on Windows without Python
installed. Other platforms need Python 2.7.

"videoinject.py" and "extract.py" can be replaced with the equivalent
exe if using Windows.

--------------------
1. Setup

-> You need to find that moflex encoder. The official one (and only so
   far) requires 64-bit Windows 7 or later. This is copyrighted so
   have fun getting it.

-> You need a decrypted video CIA. This has only been tested with
   "3D Visual Experience" USA/EUR. Others might work, no guarantees.
   Decrypt a CIA with this (use deep):
   https://github.com/ihaveamac/3DS-rom-tools/wiki/Decrypt-a-game-or-application-using-a-3DS

Put your decrypted CIA next to extract.py. Run extract.py and it will
search for CIAs in the directory. If there's more than one, it will
ask which one to extract. You only need to do this once unless you
clear the files in tools/extcontents.

--------------------
2. File layout

Make a folder in "input" for each video CIA you want to generate.
Name it after what you want the app-title to be.

Inside the folder should be:
  -> movie.moflex
     The encoded video.
  -> icon.png
     The icon that will be displayed at the Home Menu. 48x48 PNG.
  -> banner.png
     The banner that will be displayed at the Home Menu. 256x128 PNG.
  -> banner.wav (optional)
     The banner sound that will be played when the icon is selected.
     Must be 3 seconds or less. Default is one of the homebrew
     banner sounds.

--------------------
3. Generation

Use videoinject.py. CIAs will be generated based on all of the videos
in the input directory. If a folder is missing one of the three
required videos, it will be skipped and an error will be printed.

If there's an error generating the contents for a folder,
it will be skipped and the error will be printed.

CIAs will be in the "output" folder, with their titles and
unique IDs in the filename.

--------------------

ctrtool and makerom are built based on commit d24dda0:
https://github.com/profi200/Project_CTR/tree/d24dda0bc02a816887e2f34c3790d7a401f8bd98

bannertool is built based on commit 55f34cf:
https://github.com/Steveice10/bannertool/tree/55f34cfc5444bb23addab606255f3534f3c16cec
