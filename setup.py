import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "zip_include_packages": ["curses"],
    'include_files' : ["options.txt"]
}

# base="Win32GUI" should be used only for Windows GUI app
base = None if sys.platform == "win32" else None

setup(
    name="CGOL",
    version="2.0",
    author="Leo Aqua Felix",
    description="A command line application for conways game of life",
    options={"build_exe": build_exe_options},
    executables=[Executable("gameoflife.py", base=base)],
)