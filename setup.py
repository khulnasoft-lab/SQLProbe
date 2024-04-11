import argparse
import os
import sys
import stat
import subprocess
from shutil import copy2, rmtree
from distutils.dir_util import copy_tree

__author__ = "Ghost"
__email__ = "official.ghost@khulnasoft.com"
__license__ = "GPL"
__version__ = "2.0"

# Installation directory paths
if sys.platform.startswith("linux"):
    FILE_PATH = "/usr/share/sqlprobe"
    EXEC_PATH = "/usr/bin/sqlprobe"
elif sys.platform == "darwin":
    FILE_PATH = "/usr/local/share/sqlprobe"
    EXEC_PATH = "/usr/local/bin/sqlprobe"
else:
    print("Platform is not supported for installation.")
    sys.exit(1)

def metadata():
    print("SQLProbe (2.0) by {}".format(__author__))
    print("Massive SQL injection vulnerability scanner")

def dependencies(option):
    """Install script dependencies with pip"""
    try:
        subprocess.call([sys.executable, "-m", "pip", option, "-r", "requirements.txt"], check=True)
    except FileNotFoundError:
        print("pip is not installed. Please install pip.")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("Failed to install dependencies.")
        sys.exit(1)

def install():
    """Full installation of SQLProbe to the system"""

    # Create necessary directories
    os.makedirs(FILE_PATH, exist_ok=True)

    # Copy required files
    copy2("sqlprobe.py", FILE_PATH)
    copy2("requirements.txt", FILE_PATH)
    copy2("LICENSE", FILE_PATH)
    copy2("README.md", FILE_PATH)

    # Copy directories
    copy_tree("src", os.path.join(FILE_PATH, "src"))
    copy_tree("lib", os.path.join(FILE_PATH, "lib"))

    # Install Python dependencies with pip
    dependencies("install")

    # Create executable
    with open(EXEC_PATH, 'w') as installer:
        installer.write('#!/bin/bash\n')
        installer.write('python3 {}/sqlprobe.py "$@"\n'.format(FILE_PATH))

    # Set executable permissions
    os.chmod(EXEC_PATH, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

def uninstall():
    """Uninstall sqlprobe from the system"""
    if os.path.exists(FILE_PATH):
        rmtree(FILE_PATH)
        print("Removed " + FILE_PATH)

    if os.path.isfile(EXEC_PATH):
        os.remove(EXEC_PATH)
        print("Removed " + EXEC_PATH)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="Install sqlprobe in the system",  action='store_true')
    parser.add_argument("-u", "--uninstall", help="Uninstall sqlprobe from the system", action="store_true")
    args = parser.parse_args()

    if args.install:
        if os.getuid() != 0:
            print("Linux system requires root access for the installation.")
            sys.exit(1)

        if os.path.exists(FILE_PATH):
            print("SQLProbe is already installed under " + FILE_PATH)
            sys.exit(1)

        if os.path.isfile(EXEC_PATH):
            print("Executable file exists under " + EXEC_PATH)
            sys.exit(1)

        install()
        print("Installation finished.")
        print("Files are installed under " + FILE_PATH)
        print("Run: sqlprobe --help")

    elif args.uninstall:
        uninstall()
        option = input("Do you want to uninstall Python dependencies? [Y/N]: ").upper()
        while option not in ["Y", "N"]:
            option = input("Do you want to uninstall Python dependencies? [Y/N]: ").upper()

        if option == "Y":
            dependencies("uninstall")
            print("Python dependencies removed.")

        print("Uninstallation finished.")
    else:
        metadata()
        print("")
        parser.print_help()
