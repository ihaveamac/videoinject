# This is just for py2exe stuff.
# Put this script next to videoinject.py and extract.py.
from distutils.core import setup
import py2exe

# http://www.py2exe.org/index.cgi/ListOfOptions
setup(
    console=['videoinject.py', 'extract.py'],
    zipfile=None,  # add a # before zipfile to pack "library.zip" into the exe
    options={
        "py2exe":{
            "dll_excludes": ['w9xpopen.exe'],
            "bundle_files": 1
            # 3: no bundle
            # 2: bundle all but Python interpreter
            # 1: bundle all including Python interpreter
        }
    }
)
